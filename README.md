# EUDI Wallet MCP

> ## 🧱 Part of the MEOK A2A Substrate (£499/mo)
> See [meok.ai/a2a](https://meok.ai/a2a).

# EU Digital Identity Wallet bridge for AI agents

<!-- mcp-name: io.github.CSOAI-ORG/eudi-wallet-mcp -->

[![PyPI](https://img.shields.io/pypi/v/eudi-wallet-mcp)](https://pypi.org/project/eudi-wallet-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## What this covers

The **European Digital Identity Wallet (EUDI Wallet)** under eIDAS 2.0. EU member states are rolling out EUDI Wallets across 2026. Once live, EU AI agents will be authenticated via wallet-presented verifiable credentials — not API keys.

Standards covered: **ISO/IEC 18013-5 (mDoc)** · **W3C Verifiable Credentials 2.0** · **OpenID for Verifiable Credentials (OID4VC + OID4VP)** · **EUDI Architecture Reference Framework v1.7**.

## Why this matters NOW

EU regulators (and EU enterprise procurement) increasingly require **wallet-based agent identity** for 2026 deployments. API keys are not GDPR-Article-5 minimisation-compliant for high-trust decisions. Verifiable Credentials with selective disclosure are.

For UK / non-EU vendors: this MCP is your bridge into the EU agent-identity world without rebuilding your auth stack.

## Tools

| Tool | Purpose |
|---|---|
| `list_credential_types()` | EUDI ARF v1.7 credential taxonomy |
| `prepare_credential_offer(claims, recipient_did, type, validity_days)` | Build VC offer |
| `create_presentation_request(required_claims, purpose)` | OID4VP request with QR code |
| `verify_presented_credential(vp, expected_issuer_did?)` | Verify wallet response |
| `check_revocation_status(credential_id, status_list_url?)` | W3C Status List 2021 |
| `generate_selective_disclosure(credential, requested_attrs)` | GDPR Art 5 minimisation |
| `bridge_to_w3c_vc(eudi_credential)` | EUDI ARF → W3C VC 2.0 |
| `bridge_to_oid4vc(credential_offer)` | OID4VC issuance flow |

## Sister MCPs

Part of the MEOK **A2A** pack:

- `agent-identity-trust-mcp` — DID + trust scoring substrate
- `agent-data-residency-mcp` — GDPR Chapter V transfer-basis
- `agent-audit-logger-mcp` — VP-verification audit chain
- `agent-policy-enforcement-mcp` — gate on verified claims

Full catalogue: [meok.ai/anthropic-registry](https://meok.ai/anthropic-registry)

## Pricing

| Option | Price |
|---|---|
| Self-host MIT | £0 |
| Universal PAYG | £29/mo + £0.0002/call |
| A2A Substrate | £499/mo |
| Universe | £1,499/mo |
| Defence | £4,990/mo |

Buy: https://meok.ai/a2a

## Licence

MIT. By [MEOK AI Labs](https://meok.ai) (CSOAI LTD, UK Companies House 16939677).

<!-- BUY-LADDER:START -->

## 💸 Try MEOK in 30 seconds — instant buy ladder

| Tier | Price | What you get | Stripe |
|---|---|---|---|
| Smoke test | **£1** | Signed sample MCP-Hardening report + Article 50 PDF | <https://buy.stripe.com/dRmcN75ScdQS7oh1Uc8k90U> |
| Quick Kit | **£9** | EU AI Act Article 50 implementation guide (C2PA + EU-Icon) | <https://buy.stripe.com/cNi00la8s1460ZT0Q88k90V> |
| Founder Call | **£29** | 30-min 1-on-1 with the founder | <https://buy.stripe.com/8x228ta8s6oqbExaqI8k90W> |

> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->

