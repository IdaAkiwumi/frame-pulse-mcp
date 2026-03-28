in progress

# 🎬 Frame Pulse MCP

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/IdaAkiwumi)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal)](https://www.paypal.com/paypalme/iakiwumi)
[![CI](https://github.com/idaakiwumi/frame-pulse-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/idaakiwumi/frame-pulse-mcp/actions)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-orange)](https://modelcontextprotocol.io/)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://frame-pulse.streamlit.app)

**AI-native telemetry for creative workstations.**  
Give your AI assistant (Claude, Hermes, Cursor) a "nervous system" to monitor and govern heavy creative workloads—Blender renders, Unreal builds, Houdini simulations—preventing thermal crashes and lost work during crunch.

![Mission Control Dashboard](https://raw.githubusercontent.com/idaakiwumi/frame-pulse-mcp/main/assets/dashboard-screenshot.png)

## 🎯 Why This Exists

**The Studio Problem:**  
Digital content creation tools are resource-heavy. During overnight renders or UE5 lighting builds, workstations overheat or hang, losing hours of work. Existing monitoring (Glances, htop) shows *data*, but they can’t *act*.

**The Solution:**  
Frame Pulse exposes **MCP Tools** that let an AI agent:
- **Monitor:** Real-time CPU/GPU thermals, RAM pressure, disk I/O
- **Govern:** Auto-throttle background apps when `blender.exe` hits 85°C
- **Guard:** Pause renders and notify you via Telegram/Discord if thermal limits exceed safe thresholds

Built for **Technical Directors**, **AI-savvy artists**, and **Pipeline Engineers** in film, gaming, and immersive media.

## 🚀 30-Second Start


### For the AI Agent (MCP Server)
```bash
# 1. Install
pip install frame-pulse-mcp

# 2. Run the MCP server (stdio transport for Claude Desktop)
python -m frame_pulse.server

# 3. Add to your Claude Desktop config
# Mac: ~/Library/Application Support/Claude/claude_desktop_config.json
# Win: %APPDATA%/Claude/claude_desktop_config.json

{
  "mcpServers": {
    "frame-pulse": {
      "command": "python",
      "args": ["-m", "frame_pulse.server"]
    }
  }
}
```



## ☕ Support the Mission

If this tool saved your render from thermal throttling, prevented a 3AM crash, or helped your AI agent make hardware-aware decisions—consider fueling continued development:

- [Sponsor on GitHub](https://github.com/sponsors/IdaAkiwumi)
- [Donate via PayPal](https://www.paypal.com/paypalme/iakiwumi)

---

## 👩🏽‍💻 Developed by Ida Akiwumi

**Lead Product Designer | Creative Technologist | Narrative Strategist**

*Translating user friction into product opportunities.*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/idaa11)
