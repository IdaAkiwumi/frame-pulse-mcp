"""
Discord and Telegram alert integrations for Frame Pulse MCP.
"""

import os
import asyncio
import time
import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class AlertConfig:
    discord_webhook: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    thermal_threshold: float = 85.0


class AlertManager:
    def __init__(self, config: Optional[AlertConfig] = None):
        self.config = config or self._load_from_env()
        self._last_alert_time = 0
        self._cooldown_seconds = 300  # 5 min between alerts
    
    def _load_from_env(self) -> AlertConfig:
        """Load credentials from environment variables."""
        return AlertConfig(
            discord_webhook=os.getenv("DISCORD_WEBHOOK_URL"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
            thermal_threshold=float(os.getenv("THERMAL_THRESHOLD", "85.0"))
        )
    
    async def send_discord(self, message: str, status: str = "info") -> str:
        """Send alert to Discord webhook."""
        if not self.config.discord_webhook:
            return "Discord not configured"
        
        color_map = {
            "info": 0x3498db,
            "warning": 0xf39c12,
            "critical": 0xe74c3c,
            "success": 0x2ecc71
        }
        
        emoji_map = {
            "info": "ℹ️",
            "warning": "⚠️",
            "critical": "🔥",
            "success": "✅"
        }
        
        payload = {
            "username": "Frame Pulse",
            "embeds": [{
                "title": f"{emoji_map.get(status, 'ℹ️')} Frame Pulse Alert",
                "description": message,
                "color": color_map.get(status, 0x3498db),
                "footer": {"text": "frame-pulse-mcp · AI-native workstation telemetry"}
            }]
        }
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.config.discord_webhook,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as resp:
                    if resp.status == 204:
                        return "✅ Discord alert sent"
                    return f"❌ Discord error {resp.status}"
        except Exception as e:
            return f"❌ Discord failed: {e}"
    
    async def send_telegram(self, message: str) -> str:
        """Send alert via Telegram Bot API."""
        if not self.config.telegram_bot_token or not self.config.telegram_chat_id:
            return "Telegram not configured"
        
        url = f"https://api.telegram.org/bot{self.config.telegram_bot_token}/sendMessage"
        
        # Escape for MarkdownV2
        escape_chars = r'_*[]()~`>#+-=|{}.!'
        escaped_msg = re.sub(f'([{re.escape(escape_chars)}])', r'\\\\\\1', message)
        
        payload = {
            "chat_id": self.config.telegram_chat_id,
            "text": f"🎬 *Frame Pulse*\\n\\n{escaped_msg}",
            "parse_mode": "MarkdownV2",
            "disable_web_page_preview": True
        }
        
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    result = await resp.json()
                    if result.get("ok"):
                        return "✅ Telegram alert sent"
                    return f"❌ Telegram error: {result}"
        except Exception as e:
            return f"❌ Telegram failed: {e}"
    
    async def check_and_alert(self, thermal_status: str) -> Optional[str]:
        """Smart alerting with cooldown to both Discord and Telegram."""
        
        is_critical = "CRITICAL" in thermal_status
        is_caution = "CAUTION" in thermal_status
        
        if not (is_critical or is_caution):
            return None  # Safe state, no alert
        
        current_time = time.time()
        if current_time - self._last_alert_time < self._cooldown_seconds:
            return "⏳ Alert on cooldown (5 min)"
        
        self._last_alert_time = current_time
        status = "critical" if is_critical else "warning"
        
        results = []
        
        if self.config.discord_webhook:
            results.append(await self.send_discord(thermal_status, status))
        
        if self.config.telegram_bot_token:
            results.append(await self.send_telegram(thermal_status))
        
        return " | ".join(results) if results else "ℹ️ No alerts configured"


def send_discord_sync(message: str, status: str = "info") -> str:
    """Synchronous wrapper for non-async contexts."""
    manager = AlertManager()
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            asyncio.create_task(manager.send_discord(message, status))
            return "⏳ Alert queued"
        return asyncio.run(manager.send_discord(message, status))
    except Exception as e:
        return f"❌ Failed: {e}"


_default_manager: Optional[AlertManager] = None

def get_alert_manager() -> AlertManager:
    global _default_manager
    if _default_manager is None:
        _default_manager = AlertManager()
    return _default_manager