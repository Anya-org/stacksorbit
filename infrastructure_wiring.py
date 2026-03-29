import os
import requests
import json
from typing import Dict, List, Optional
from datetime import datetime

class InfrastructureWiring:
    """Handles integration with Supabase and Neon for StacksOrbit."""

    def __init__(self, config: Dict):
        self.config = config
        self.supabase_url = config.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
        self.supabase_key = config.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")
        self.neon_db_url = config.get("NEON_DB_URL")
        print(f"DEBUG: Supabase URL: {self.supabase_url}")

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
            print(f"DEBUG: Fetching runway from {url}")
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"DEBUG: Runway data: {data}")
                return data[0] if data else None
            else:
                print(f"DEBUG: Runway response error: {response.status_code} {response.text}")
        except Exception as e:
            print(f"DEBUG: Runway exception: {e}")
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
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return data[0] if data else None
        except Exception:
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
        try:
            url = f"{self.supabase_url}/rest/v1/deployment_efficiency"
            requests.post(url, headers=headers, json=payload, timeout=5)
        except Exception:
            pass

    def sync_to_neon(self):
        """Placeholder for Neon synchronization logic."""
        pass
