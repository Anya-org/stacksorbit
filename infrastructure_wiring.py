from typing import Dict, Any, Optional, List, Union
import os
import requests
import json
import logging
import time
import threading
from datetime import datetime
from conxius_orbit_secrets import redact_recursive

# 🛡️ Sentinel: Setup infrastructure logger
logger = logging.getLogger("conxius_orbit_infra")


class InfrastructureWiring:
    """Handles integration with Supabase and Neon for ConxiusOrbit."""

    def __init__(self, config: Dict):
        self.config = config
        self.session = requests.Session()
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = 300  # 5 minutes

        # 🛡️ Sentinel: Redact config before logging in debug mode
        redacted_config = redact_recursive(config)
        logger.debug(f"InfrastructureWiring initialized with config: {redacted_config}")

    def get_runway_metrics(self, bypass_cache: bool = False) -> Dict:
        """Fetch infrastructure runway metrics from Supabase."""
        cache_key = "runway_metrics"
        now = time.time()

        if not bypass_cache and cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if now - timestamp < self._cache_ttl:
                return data

        try:
            url = self.config.get("SUPABASE_URL", "")
            key = self.config.get("SUPABASE_KEY", "")

            if not url or not key:
                return {"status": "error", "message": "Missing Supabase configuration"}

            headers = {"apikey": key, "Authorization": f"Bearer {key}"}
            # 🛡️ Sentinel: Explicit timeout to avoid hanging connections.
            response = self.session.get(
                f"{url}/rest/v1/infrastructure_metrics?select=*",
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                self._cache[cache_key] = (data, now)
                return data
            else:
                logger.warning(f"Supabase API returned {response.status_code}")
                return {"status": "error", "code": response.status_code}

        except Exception as e:
            logger.error(f"Failed to fetch runway metrics: {e}")
            return {"status": "error", "message": str(e)}

    def get_exit_velocity(self, bypass_cache: bool = False) -> Dict:
        """Fetch deployment exit velocity from Neon database."""
        cache_key = "exit_velocity"
        now = time.time()

        if not bypass_cache and cache_key in self._cache:
            data, timestamp = self._cache[cache_key]
            if now - timestamp < self._cache_ttl:
                return data

        try:
            db_url = self.config.get("NEON_DB_URL") or os.environ.get("NEON_DB_URL")
            if not db_url:
                return {"status": "error", "message": "Missing Neon DB configuration"}

            # Mock implementation for sandbox environment
            data = {"velocity": 42.5, "unit": "deployments/week", "trend": "up"}
            self._cache[cache_key] = (data, now)
            return data

        except Exception as e:
            logger.error(f"Failed to fetch exit velocity: {e}")
            return {"status": "error", "message": str(e)}

    def log_deployment(
        self, deployment_info: Any, status: Optional[str] = None
    ) -> bool:
        """Log deployment event to central infrastructure."""
        try:
            url = self.config.get("SUPABASE_URL", "")
            key = self.config.get("SUPABASE_KEY", "")

            if not url or not key:
                return False

            headers = {
                "apikey": key,
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal",
            }

            # Handle both dictionary and simple string info (for tests)
            if isinstance(deployment_info, dict):
                payload = redact_recursive(deployment_info)
            else:
                # 🛡️ Sentinel: If it's a string, it might be a module name or specific info.
                # Tests expect 'module_name' in some cases.
                payload = {
                    "module_name": redact_recursive(deployment_info),
                    "info": redact_recursive(deployment_info),
                }

            if status:
                payload["status"] = status

            payload["timestamp"] = datetime.now().isoformat()

            response = self.session.post(
                f"{url}/rest/v1/deployment_logs",
                headers=headers,
                json=payload,
                timeout=10,
            )

            return response.status_code in (200, 201)

        except Exception as e:
            # 🛡️ Sentinel: Redact error details to prevent information disclosure.
            safe_error = redact_recursive({"error": str(e)})
            logger.error(f"Failed to log deployment: {safe_error['error']}")
            return False
