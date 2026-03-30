import os
import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime


class InfrastructureWiring:
    """Handles integration with Supabase and Neon for StacksOrbit."""

    def __init__(self, config: Dict):
        self.config = config
        self.supabase_url = config.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
        self.supabase_key = config.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")
        self.neon_db_url = config.get("NEON_DB_URL")
        # Bolt ⚡: Use a persistent session for connection pooling to Supabase.
        self.session = requests.Session()
        self._cache = {}
        self._cache_ttl = 300  # 5 minute cache
        print(f"DEBUG: Supabase URL: {self.supabase_url}")

    def get_runway_metrics(self, bypass_cache: bool = False) -> Optional[Dict]:
        """
        Fetch runway metrics from Supabase.
        Bolt ⚡: Implemented TTL caching and session-based requests.
        """
        if not self.supabase_url or not self.supabase_key:
            return None

        # Bolt ⚡: Check cache first.
        cache_key = "runway_metrics"
        now = time.time()
        if not bypass_cache and cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if now - cache_entry["timestamp"] < self._cache_ttl:
                return cache_entry["data"]

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
        }
        try:
            url = f"{self.supabase_url}/rest/v1/runway_metrics?select=*&order=timestamp.desc&limit=1"
            print(f"DEBUG: Fetching runway from {url}")
            response = self.session.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"DEBUG: Runway data: {data}")
                result = data[0] if data else None
                # Bolt ⚡: Update cache.
                self._cache[cache_key] = {"timestamp": now, "data": result}
                return result
            else:
                print(
                    f"DEBUG: Runway response error: {response.status_code} {response.text}"
                )
        except Exception as e:
            print(f"DEBUG: Runway exception: {e}")
            return None
        return None

    def get_exit_velocity(self, bypass_cache: bool = False) -> Optional[Dict]:
        """
        Fetch exit velocity metrics from Supabase.
        Bolt ⚡: Implemented TTL caching and session-based requests.
        """
        if not self.supabase_url or not self.supabase_key:
            return None

        # Bolt ⚡: Check cache first.
        cache_key = "exit_velocity"
        now = time.time()
        if not bypass_cache and cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if now - cache_entry["timestamp"] < self._cache_ttl:
                return cache_entry["data"]

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
        }
        try:
            url = f"{self.supabase_url}/rest/v1/exit_velocity?select=*&order=timestamp.desc&limit=1"
            response = self.session.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result = data[0] if data else None
                # Bolt ⚡: Update cache.
                self._cache[cache_key] = {"timestamp": now, "data": result}
                return result
        except Exception:
            return None
        return None

    def log_deployment(
        self, module_name: str, status: str, gas_usage: int = 0, execution_time: int = 0
    ):
        """Log a deployment event to Supabase."""
        if not self.supabase_url or not self.supabase_key:
            return

        headers = {
            "apikey": self.supabase_key,
            "Authorization": f"Bearer {self.supabase_key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal",
        }
        payload = {
            "module_name": module_name,
            "status": status,
            "gas_usage": gas_usage,
            "execution_time_ms": execution_time,
            "timestamp": datetime.now().isoformat(),
        }
        try:
            url = f"{self.supabase_url}/rest/v1/deployment_efficiency"
            requests.post(url, headers=headers, json=payload, timeout=5)
        except Exception:
            pass

    def sync_to_neon(self):
        """Placeholder for Neon synchronization logic."""
        pass
