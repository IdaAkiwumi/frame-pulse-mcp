in progress

# 🎬 Frame Pulse MCP

[![GitHub Sponsor](https://img.shields.io/badge/Sponsor-GitHub-EA4AAA?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/IdaAkiwumi)
[![PayPal](https://img.shields.io/badge/Donate-PayPal-00457C?style=for-the-badge&logo=paypal)](https://www.paypal.com/paypalme/iakiwumi)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-orange)](https://modelcontextprotocol.io/)
[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://frame-pulse.streamlit.app)

**AI-native telemetry for creative workstations.**  
Give your AI assistant (Claude, Hermes, Cursor) a "nervous system" to monitor and govern heavy creative workloads—Blender renders, Unreal builds, Houdini simulations—preventing thermal crashes and lost work during crunch.

![Mission Control Dashboard](https://raw.githubusercontent.com/idaakiwumi/frame-pulse-mcp/main/assets/dashboard-screenshot.png)

---

## 🚀 Quick Start

### Option A: Claude Desktop (Recommended)
1. **Clone and install**
``` powershell
git clone [https://github.com/idaakiwumi/frame-pulse-mcp.git](https://github.com/idaakiwumi/frame-pulse-mcp.git)
cd frame-pulse-mcp
pip install -r requirements.txt
```

2. **Add to Claude Desktop config**
   * **Windows (MSIX/Store):** `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude\claude_desktop_config.json`
   * **Standard:** `%APPDATA%\Claude\claude_desktop_config.json`

``` json
{
  "mcpServers": {
    "frame-pulse": {
      "command": "py",
      "args": [
        "-3.14",
        "-u",
        "C:\\Users\\YOUR_PATH\\frame-pulse-mcp\\src\\frame_pulse\\server.py"
      ]
    }
  }
}
```
Then ask Claude: "Check my system status" or "Deprioritize my background apps"

### Option B: The "Hero Demo" (Streamlit)
I built a high-fidelity **Mission Control Dashboard** using Streamlit. While the MCP runs in the background, this dashboard serves as the visual command center for the project.
``` powershell
streamlit run streamlit_app/mission_control.py
```

---

## 📱 The "Digital Pager" Ecosystem (Telegram & Discord)

As a **Product Architect**, I designed Frame Pulse to be "Headless." Creative professionals don't want another window to monitor; they want an assistant that pings them when they are away from their desk.

* **Telegram Bot:** Acts as a private production pager. Get a message on your phone if your CPU hits 90°C while you're grabbing coffee.
* **Discord Webhooks:** Rich, color-coded embeds sent to your studio's Discord server for team-wide render farm monitoring.

**Setup:** Configure your `.env` file with your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

---

## 🛠️ MCP Tools for AI Agents

| Tool | Function | Use Case |
| :--- | :--- | :--- |
| `check_system_health()` | CPU, RAM, and Thermal scan | "Is it safe to start a 6-hour render?" |
| `scan_creative_apps()` | Identifies Blender, Unreal, Maya, etc. | "What's currently taxing the GPU?" |
| `emergency_throttle()` | Immediate CPU priority reduction | "CRITICAL: Throttle background apps now." |
| `get_thermal_status()` | Real-time temperature read | "Am I at risk of a thermal shutdown?" |

---

## 🤝 Community & Recognition
**Featured on Lobehub — AI tools discovery platform.

## 🛠️ Built With

- **[MCP](https://modelcontextprotocol.io/)** — Model Context Protocol for AI tool interoperability
- **[FastMCP](https://github.com/modelcontextprotocol/python-sdk)** — Python SDK for MCP servers
- **[psutil](https://github.com/giampaolo/psutil)** — Cross-platform system monitoring
- **[Streamlit](https://streamlit.io/)** — Rapid Python dashboarding

## 📸 Demo

[30-second GIF: Claude asking "Start my render?" → Frame Pulse responding "CAUTION: CPU 89%" → User clicking throttle → Success toast]

## 🤝 Who's Using This

> "Frame Pulse caught a thermal spike before our overnight farm render. Saved us 14 hours of redo work."  
> — Anonymous VFX Supervisor (via DM)


## ☕ Support the Mission

If this tool saved your render from thermal throttling, prevented a 3AM crash, or helped your AI agent make hardware-aware decisions—consider fueling continued development:

- [Sponsor on GitHub](https://github.com/sponsors/IdaAkiwumi)
- [Donate via PayPal](https://www.paypal.com/paypalme/iakiwumi)

---

## 👩🏽‍💻 Developed by Ida Akiwumi

**Lead Product Designer | Creative Technologist | Narrative Strategist**

*Translating user friction into product opportunities.*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat&logo=linkedin)](https://www.linkedin.com/in/idaa11)
