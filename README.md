<!-- mcp-name: io.github.CSOAI-ORG/eudi-wallet-mcp -->
[![MCP Scorecard: 88/100](https://img.shields.io/badge/proofof.ai-88%2F100-5b21b6)](https://proofof.ai/scorecard/eudi-wallet-mcp.html)

# Eudi Wallet MCP
mcp-name: io.github.CSOAI-ORG/eudi-wallet-mcp

# EUDI Wallet MCP

[![MEOK AI Labs](https://img.shields.io/badge/MEOK-AI%20Labs-667eea)](https://meok.ai)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-22c55e)](https://councilof.ai)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Install-3775a9)](https://pypi.org/project/eudi_wallet_mcp/)

> EUDI Wallet MCP - EU Digital Identity Wallet (eIDAS 2

EUDI Wallet MCP - EU Digital Identity Wallet (eIDAS 2.0) for AI agents. MIT. By MEOK AI Labs.

---

## 🚀 Quick Start

```bash
# Install via pip
pip install eudi_wallet_mcp

# Or install via Smithery
npx -y @smithery/cli@latest install eudi-wallet-mcp --client claude
```

## ✨ Features

- MCP protocol compliant
- Easy installation
- Well-documented API
- Production-ready
- Active maintenance

## 📖 Documentation

- [Full Documentation](https://docs.meok.ai/eudi-wallet-mcp)
- [API Reference](https://api.meok.ai)
- [EU AI Act Compliance Guide](https://councilof.ai/compliance)

## 🛡️ Compliance

This MCP server is built with **EU AI Act compliance** built-in:

- ✅ Article 9 — Risk Management System
- ✅ Article 13 — Transparency & Instructions for Use
- ✅ Article 15 — Bias Detection & Testing
- ✅ Article 26 — FRIA Support (where applicable)
- ✅ Article 50 — AI Content Watermarking (where applicable)

Need help getting compliant? **[Book a free 15-min diagnostic →](https://cal.com/csoai/august-audit)**

## 🏢 Enterprise

Need custom development, SLA guarantees, or white-label deployment?

- **Pro:** $99/mo — Full MCP suite + EU AI Act tracking
- **Enterprise:** $499/mo — Custom dev + SLA + Dedicated support

[View Pricing →](https://councilof.ai/pricing) | [Contact Sales →](mailto:sales@csoai.org)

## 🤝 Part of the MEOK Ecosystem

This server is part of the **[MEOK AI Labs](https://meok.ai)** ecosystem — 300+ MCP servers for sovereign AI governance.

| Domain | Purpose |
|--------|---------|
| [councilof.ai](https://councilof.ai) | EU AI Act compliance marketplace |
| [safetyof.ai](https://safetyof.ai) | AI safety & monitoring |
| [meok.ai](https://meok.ai) | Sovereign AI platform |
| [cobolbridge.ai](https://cobolbridge.ai) | Legacy modernization |

## 📜 License

MIT © [CSOAI-ORG](https://github.com/CSOAI-ORG)

---

<p align="center">
  <sub>Built with 💜 by <a href="https://meok.ai">MEOK AI Labs</a> · UK Companies House 16939677</sub>
</p>
> Refundable. UK Stripe — VAT-clean. Builds on the 81-MCP MEOK fleet.
> Verify any signed report at <https://meok.ai/verify>.

<!-- BUY-LADDER:END -->


## Configuration

Add to your `claude_desktop_config.json` (Claude Desktop) or your MCP client config:

```json
{
  "mcpServers": {
    "eudi-wallet-mcp": {
      "command": "uvx",
      "args": ["eudi-wallet-mcp"]
    }
  }
}
```

Or: `pip install eudi-wallet-mcp` then run the `eudi-wallet-mcp` command (stdio transport).

## Examples

Once configured, ask your assistant, for example:
- "Use `list_credential_types` to …"
- "Use `prepare_credential_offer` to …"
- "Use `create_presentation_request` to …"
