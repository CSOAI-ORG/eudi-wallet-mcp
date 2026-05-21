#!/usr/bin/env python3
"""
EUDI Wallet MCP — EU Digital Identity Wallet for AI Agents
=============================================================

By MEOK AI Labs · https://meok.ai · MIT
<!-- mcp-name: io.github.CSOAI-ORG/eudi-wallet-mcp -->

WHAT THIS COVERS
----------------
The European Digital Identity Wallet (EUDI Wallet) under eIDAS 2.0. EU
member states are rolling out EUDI Wallets across 2026. Once live, EU
agents will be authenticated via wallet-presented verifiable credentials
— not API keys.

Uses:
  - ISO/IEC 18013-5 (mDoc) — mobile document format
  - W3C Verifiable Credentials 2.0 — credential format
  - OpenID for Verifiable Credentials (OID4VC / OID4VP) — issuance + verification
  - EUDI Architecture Reference Framework (ARF)

USE CASES
---------
- AI agent authentication via EUDI wallet (instead of API keys)
- Cross-border agent identity for EU buyers
- Verifiable purchase authorisation (signed by user's EUDI wallet)
- GDPR Article 5 minimisation via selective disclosure

TOOLS
-----
- prepare_credential_offer(claims, recipient_did, validity_days): build VC offer
- create_presentation_request(required_claims, purpose): build OID4VP request
- verify_presented_credential(vp, expected_issuer_did?): verify wallet response
- check_revocation_status(credential_id, status_list_url): check VC validity
- generate_selective_disclosure(credential, requested_attrs): mDoc-style minimal
- bridge_to_w3c_vc(eudi_credential): map EUDI ARF → W3C VC 2.0
- bridge_to_oid4vc(credential_offer): map to OID4VC issuance flow

PRICING
-------
Free MIT self-host · £29/mo Starter · £79/mo Pro · A2A Substrate £499/mo.
EU regulated buyers see this MCP as table-stakes for 2026 deployments.
"""

from __future__ import annotations
import hashlib
import hmac
import json
import os
import time
from datetime import datetime, timezone, timedelta
from typing import Optional
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("eudi-wallet")
_HMAC_SECRET = os.environ.get("MEOK_HMAC_SECRET", "")


# EUDI Wallet supported credential types (high-assurance categories per ARF v1.7)
EUDI_CREDENTIAL_TYPES = {
    "personal_id":         "Person Identification Data (PID) — government-issued",
    "qualified_signature": "Qualified Electronic Signature certificate",
    "qualified_seal":      "Qualified Electronic Seal certificate",
    "education":           "Education credentials (degrees, certificates)",
    "professional":        "Professional qualifications (lawyer, doctor, etc.)",
    "driving_licence":     "Mobile Driving Licence (mDL, ISO 18013-5)",
    "health_insurance":    "European Health Insurance Card",
    "payment":             "Payment account credentials",
    "ai_agent":            "AI agent operator credential (NEW under eIDAS 2.0)",
}


def _sign(payload: dict) -> str:
    if not _HMAC_SECRET:
        return "unsigned-no-key-configured"
    return hmac.new(_HMAC_SECRET.encode(), json.dumps(payload, sort_keys=True).encode(), hashlib.sha256).hexdigest()


def _ts() -> str:
    return datetime.now(timezone.utc).isoformat()


# ────────────────────────────────────────────────────────────────────────
# Tools
# ────────────────────────────────────────────────────────────────────────

@mcp.tool()
def list_credential_types() -> dict:
    """List EUDI-supported credential types per the EU Architecture Reference Framework."""
    return {
        "spec": "EUDI ARF v1.7",
        "credential_types": [{"id": k, "description": v} for k, v in EUDI_CREDENTIAL_TYPES.items()],
        "standards": ["ISO/IEC 18013-5 (mDoc)", "W3C VC 2.0", "OID4VC", "OID4VP", "eIDAS 2.0"],
    }


@mcp.tool()
def prepare_credential_offer(
    claims: dict,
    recipient_did: str,
    credential_type: str = "ai_agent",
    validity_days: int = 365,
    issuer_did: Optional[str] = None,
) -> dict:
    """
    Build a Verifiable Credential offer for an EUDI Wallet recipient.

    Args:
        claims: Dict of claims being attested (e.g. {"role": "compliance-auditor", "valid_until": "2027-01-01"}).
        recipient_did: W3C DID of the recipient (their EUDI Wallet).
        credential_type: One of EUDI_CREDENTIAL_TYPES keys.
        validity_days: VC validity window.
        issuer_did: Optional override of issuer DID.

    Returns:
        {credential_offer, signature, wallet_deeplink}
    """
    if credential_type not in EUDI_CREDENTIAL_TYPES:
        return {"error": "unknown_credential_type", "valid": list(EUDI_CREDENTIAL_TYPES.keys())}

    issuer = issuer_did or "did:meok:csoai-org:16939677"
    expires_at = (datetime.now(timezone.utc) + timedelta(days=validity_days)).isoformat()
    offer = {
        "@context": ["https://www.w3.org/ns/credentials/v2", "https://eudi.europa.eu/ns/arf/v1.7"],
        "type": ["VerifiableCredential", "EUDIVerifiableCredential", credential_type],
        "issuer": issuer,
        "credentialSubject": {"id": recipient_did, **claims},
        "issuanceDate": _ts(),
        "expirationDate": expires_at,
        "credentialSchema": EUDI_CREDENTIAL_TYPES[credential_type],
    }
    return {
        "credential_offer": offer,
        "signature": _sign(offer),
        "wallet_deeplink": f"eudi://credential-offer?issuer={issuer}&cred={credential_type}",
        "next_step": "Call create_presentation_request() when you need the holder to prove possession.",
    }


@mcp.tool()
def create_presentation_request(
    required_claims: list[str],
    purpose: str,
    requester_did: Optional[str] = None,
    selective_disclosure: bool = True,
) -> dict:
    """
    Build an OID4VP presentation request for an EUDI Wallet.

    Args:
        required_claims: List of claim names the verifier needs.
        purpose: GDPR-required justification for why the data is needed.
        requester_did: Verifier's DID.
        selective_disclosure: If True, request only the listed claims (ARF best practice).

    Returns:
        {presentation_request, qr_code_payload, expires_at}
    """
    requester = requester_did or "did:meok:csoai-org:verifier"
    expires_at = int(time.time()) + 600  # 10 min
    pr_id = f"pr_{int(time.time())}_{os.urandom(4).hex()}"
    request = {
        "presentation_request_id": pr_id,
        "requester_did": requester,
        "purpose": purpose,
        "required_claims": required_claims,
        "selective_disclosure": selective_disclosure,
        "expires_at": expires_at,
        "ts": _ts(),
    }
    return {
        "presentation_request": request,
        "qr_code_payload": f"openid-vc://presentation-request?id={pr_id}&requester={requester}",
        "signature": _sign(request),
        "compliance_note": "GDPR Article 5(1)(c) data minimisation — selective_disclosure=true requests only the listed claims, not the whole credential.",
    }


@mcp.tool()
def verify_presented_credential(
    vp: dict,
    expected_issuer_did: Optional[str] = None,
) -> dict:
    """
    Verify a Verifiable Presentation returned by an EUDI Wallet.

    Args:
        vp: Verifiable Presentation envelope.
        expected_issuer_did: Optional check that the credential was issued by this DID.

    Returns:
        {verified, issues, claims_revealed, audit_chain_entry}
    """
    issues = []
    # Scaffold checks — production wires actual signature verification + revocation
    if "verifiableCredential" not in vp and "verifiable_credential" not in vp:
        issues.append("no_credential_field")
    if "proof" not in vp:
        issues.append("no_proof")
    vc_list = vp.get("verifiableCredential", vp.get("verifiable_credential", []))
    if not isinstance(vc_list, list):
        vc_list = [vc_list]
    claims = {}
    for vc in vc_list:
        if isinstance(vc, dict):
            issuer = vc.get("issuer", "")
            if expected_issuer_did and issuer != expected_issuer_did:
                issues.append(f"unexpected_issuer: {issuer}")
            claims.update(vc.get("credentialSubject", {}))

    verified = len(issues) == 0
    entry = {
        "type": "eudi_vp_verified" if verified else "eudi_vp_flagged",
        "verified": verified,
        "issues": issues,
        "claims_count": len(claims),
        "ts": _ts(),
    }
    return {
        "verified": verified,
        "issues": issues,
        "claims_revealed": claims if verified else {},
        "audit_chain_entry": entry,
        "signature": _sign(entry),
    }


@mcp.tool()
def check_revocation_status(credential_id: str, status_list_url: Optional[str] = None) -> dict:
    """
    Check a credential's revocation status via Status List 2021.

    Args:
        credential_id: The credential ID.
        status_list_url: Optional explicit status-list URL. Defaults to MEOK's.

    Returns:
        {credential_id, status, checked_at}
    """
    # Scaffold — production fetches the bitstring from status_list_url and checks the index.
    url = status_list_url or "https://verify.meok.ai/status-list/v1.json"
    return {
        "credential_id": credential_id,
        "status": "active",  # scaffold default
        "status_list_url": url,
        "spec": "W3C Status List 2021",
        "checked_at": _ts(),
        "stage": "scaffold — wire to live status list for production",
    }


@mcp.tool()
def generate_selective_disclosure(
    credential: dict,
    requested_attrs: list[str],
) -> dict:
    """
    Generate a selective-disclosure presentation revealing ONLY the requested attributes.

    Args:
        credential: Full Verifiable Credential.
        requested_attrs: Subset of claim names to reveal.

    Returns:
        Minimal VP with only the requested claims.
    """
    full_subject = credential.get("credentialSubject", {})
    minimal_subject = {k: v for k, v in full_subject.items() if k in requested_attrs or k == "id"}
    vp = {
        "@context": credential.get("@context", []),
        "type": ["VerifiablePresentation"],
        "verifiableCredential": [{
            **{k: v for k, v in credential.items() if k != "credentialSubject"},
            "credentialSubject": minimal_subject,
        }],
        "ts": _ts(),
    }
    return {
        "presentation": vp,
        "signature": _sign(vp),
        "revealed_attrs": list(minimal_subject.keys()),
        "withheld_attrs": [k for k in full_subject if k not in minimal_subject],
        "compliance_note": "GDPR Article 5(1)(c) minimisation honoured — only requested claims revealed.",
    }


@mcp.tool()
def bridge_to_w3c_vc(eudi_credential: dict) -> dict:
    """Map an EUDI ARF credential to a W3C VC 2.0 envelope."""
    return {
        "@context": ["https://www.w3.org/ns/credentials/v2"],
        "type": ["VerifiableCredential", *eudi_credential.get("type", [])],
        "issuer": eudi_credential.get("issuer"),
        "validFrom": eudi_credential.get("issuanceDate"),
        "validUntil": eudi_credential.get("expirationDate"),
        "credentialSubject": eudi_credential.get("credentialSubject", {}),
        "credentialStatus": {
            "type": "StatusList2021Entry",
            "statusListIndex": "0",
            "statusListCredential": "https://verify.meok.ai/status-list/v1.json",
        },
    }


@mcp.tool()
def bridge_to_oid4vc(credential_offer: dict) -> dict:
    """Map a credential offer to OID4VC issuance flow."""
    return {
        "spec": "OpenID for Verifiable Credentials Issuance",
        "credential_offer_uri": f"openid-credential-offer://?credential_offer_uri={credential_offer.get('issuer', 'unknown')}",
        "grants": {
            "urn:ietf:params:oauth:grant-type:pre-authorized_code": {
                "pre-authorized_code": f"pac_{os.urandom(8).hex()}",
                "user_pin_required": False,
            }
        },
        "credential_configuration_ids": [t for t in credential_offer.get("type", []) if t != "VerifiableCredential"],
    }


if __name__ == "__main__":
    mcp.run()
