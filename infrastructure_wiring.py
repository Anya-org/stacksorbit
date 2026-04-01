import os
import requests
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from stacksorbit_secrets import redact_recursive

# 🛡️ Sentinel: Setup infrastructure logger
logger = logging.getLogger("stacksorbit_infra")

class InfrastructureWiring:
    """Handles integration with Supabase and Neon for StacksOrbit."""

    def __init__(self, config: Dict):
        self.config = config
        self.supabase_url = config.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
        self.supabase_key = config.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")
        # 🛡️ Sentinel: Support NEON_DB_URL from environment for consistency
        self.neon_db_url = config.get("NEON_DB_URL") or os.environ.get("NEON_DB_URL")

        # 🛡️ Sentinel: Redact URLs in debug logs to prevent disclosure of project IDs or keys in URLs
        if self.supabase_url and logger.isEnabledFor(logging.DEBUG):
            logger.debug(
                "Supabase URL: %s",
                redact_recursive(self.supabase_url, parent_key="SUPABASE_URL"),
            )

    def get_runway_metrics(self) -> Optional[Dict]:
        """Fetch runway metrics from Supabase."""
        if not self.supabase_url or not self.supabase_key:
            return None

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}"
        }
        try:
            url = f"{self.supabase_url}/rest/v1/runway_metrics?select=*&order=timestamp.desc&limit=1"
            # 🛡️ Sentinel: Redact URL in logs
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "Fetching runway from %s",
                    redact_recursive(url, parent_key="SUPABASE_URL"),
                )
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # 🛡️ Sentinel: Redact data before logging
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(
                        "Runway data: %s",
                        redact_recursive(data, parent_key="SUPABASE_RESPONSE"),
                    )
                return data[0] if data else None
            else:
                # 🛡️ Sentinel: Use WARNING for non-200 responses as they indicate functional issues.
                redacted_body = redact_recursive(response.text, parent_key="SUPABASE_RESPONSE")
                logger.warning(
                    "Runway response error: %s %s",
                    response.status_code,
                    str(redacted_body)[:500],
                )
        except Exception as e:
            # 🛡️ Sentinel: Use ERROR for exceptions to ensure visibility in production logs.
            logger.error(
                "Runway exception: %s",
                redact_recursive(str(e), parent_key="INFRA_EXCEPTION"),
            )
            return None
        return None

    def get_exit_velocity(self) -> Optional[Dict]:
        """Fetch exit velocity metrics from Supabase."""
        if not self.supabase_url or not self.supabase_key:
            return None

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}"
        }
        try:
            url = f"{self.supabase_url}/rest/v1/exit_velocity?select=*&order=timestamp.desc&limit=1"
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "Fetching exit velocity from %s",
                    redact_recursive(url, parent_key="SUPABASE_URL"),
                )
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug(
                        "Exit velocity data: %s",
                        redact_recursive(data, parent_key="SUPABASE_RESPONSE"),
                    )
                return data[0] if data else None
            else:
                redacted_body = redact_recursive(response.text, parent_key="SUPABASE_RESPONSE")
                logger.warning(
                    "Exit velocity response error: %s %s",
                    response.status_code,
                    str(redacted_body)[:500],
                )
        except Exception as e:
            logger.error(
                "Exit velocity exception: %s",
                redact_recursive(str(e), parent_key="INFRA_EXCEPTION"),
            )
            return None
        return None

    def log_deployment(self, module_name: str, status: str, gas_usage: int = 0, execution_time: int = 0):
        """Log a deployment event to Supabase."""
        if not self.supabase_url or not self.supabase_key:
            return

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        payload = {
            "module_name": module_name,
            "status": status,
            "gas_usage": gas_usage,
            "execution_time_ms": execution_time,
            "timestamp": datetime.now().isoformat()
        }

        # 🛡️ Sentinel: Redact payload before sending to external service
        # This provides defense-in-depth in case module_name or other fields contain secrets.
        redacted_payload = redact_recursive(payload)

        try:
            url = f"{self.supabase_url}/rest/v1/deployment_efficiency"
            response = requests.post(url, headers=headers, json=redacted_payload, timeout=5)
            if response.status_code not in (200, 201):
                logger.warning(f"Deployment log response error: {response.status_code}")
        except Exception as e:
            logger.error(
                "Deployment log exception: %s",
                redact_recursive(str(e), parent_key="INFRA_EXCEPTION"),
            )

    def sync_to_neon(self):
        """Placeholder for Neon synchronization logic."""
        pass
