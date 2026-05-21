"""Smoke tests for eudi-wallet-mcp."""
import sys, os, inspect, traceback
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server import (
    list_credential_types,
    prepare_credential_offer,
    create_presentation_request,
    verify_presented_credential,
    check_revocation_status,
    generate_selective_disclosure,
    bridge_to_w3c_vc,
    bridge_to_oid4vc,
)


def test_list_types_includes_ai_agent():
    r = list_credential_types()
    types = [t["id"] for t in r["credential_types"]]
    assert "ai_agent" in types
    assert "personal_id" in types


def test_offer_unknown_type_errors():
    r = prepare_credential_offer({"x": "y"}, "did:user:1", "made_up_type")
    assert "error" in r


def test_offer_returns_signed_vc():
    r = prepare_credential_offer({"role": "auditor"}, "did:user:1", "ai_agent")
    assert "signature" in r
    assert "VerifiableCredential" in r["credential_offer"]["type"]


def test_presentation_request_has_qr():
    r = create_presentation_request(["role"], "GDPR Article 27 compliance evidence")
    assert "qr_code_payload" in r
    assert r["presentation_request"]["selective_disclosure"] is True


def test_verify_flags_missing_proof():
    r = verify_presented_credential({"verifiableCredential": []})
    assert r["verified"] is False
    assert any("proof" in i for i in r["issues"])


def test_verify_passes_with_proof():
    vp = {
        "verifiableCredential": [{
            "issuer": "did:meok:csoai-org:16939677",
            "credentialSubject": {"id": "did:user:1", "role": "auditor"},
        }],
        "proof": {"type": "Ed25519Signature2020"},
    }
    r = verify_presented_credential(vp, expected_issuer_did="did:meok:csoai-org:16939677")
    assert r["verified"] is True
    assert r["claims_revealed"]["role"] == "auditor"


def test_revocation_status_scaffold():
    r = check_revocation_status("vc_12345")
    assert r["status"] == "active"
    assert "Status List 2021" in r["spec"]


def test_selective_disclosure_minimises():
    cred = {
        "@context": ["v2"],
        "type": ["VerifiableCredential"],
        "credentialSubject": {"id": "did:u:1", "name": "Alice", "address": "...", "age": 30, "role": "auditor"},
    }
    r = generate_selective_disclosure(cred, requested_attrs=["role"])
    subject = r["presentation"]["verifiableCredential"][0]["credentialSubject"]
    assert "role" in subject
    assert "address" not in subject
    assert "name" not in subject


def test_bridge_w3c_envelope():
    eudi = {
        "type": ["EUDIVerifiableCredential", "ai_agent"],
        "issuer": "did:meok:1",
        "issuanceDate": "2026-05-21",
        "expirationDate": "2027-05-21",
        "credentialSubject": {"x": "y"},
    }
    r = bridge_to_w3c_vc(eudi)
    assert "validFrom" in r
    assert "validUntil" in r
    assert "VerifiableCredential" in r["type"]


def test_bridge_oid4vc():
    offer = {"issuer": "did:meok:1", "type": ["VerifiableCredential", "ai_agent"]}
    r = bridge_to_oid4vc(offer)
    assert "credential_offer_uri" in r
    assert "pre-authorized_code" in str(r["grants"])


if __name__ == "__main__":
    g = dict(globals())
    fns = [v for k, v in g.items() if k.startswith("test_") and inspect.isfunction(v)]
    p = f = 0
    for fn in fns:
        try:
            fn(); print(f"✓ {fn.__name__}"); p += 1
        except Exception as e:
            print(f"✗ {fn.__name__}: {type(e).__name__}: {e}"); traceback.print_exc(); f += 1
    print(f"\n{p} passed, {f} failed")
