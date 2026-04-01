import unittest
from unittest.mock import patch

from infrastructure_wiring import InfrastructureWiring
from stacksorbit_secrets import is_sensitive_key

class TestSentinelInfraHardening(unittest.TestCase):
    def test_new_infra_keywords(self):
        """Verify that new infra keywords are identified as sensitive."""
        infra_keywords = [
            "SUPABASE_KEY", "NEON_DB_URL", "POSTGRES_PASSWORD",
            "MONGODB_URI", "REDIS_AUTH", "AWS_SECRET_ACCESS_KEY",
            "AZURE_STORAGE_KEY", "GCP_SERVICE_ACCOUNT", "DIGITALOCEAN_TOKEN"
        ]
        for kw in infra_keywords:
            self.assertTrue(is_sensitive_key(kw), f"Keyword '{kw}' should be sensitive")

    def test_infra_init_logs_redacted_urls(self):
        """Verify that InfrastructureWiring redacts sensitive fields in debug logs."""
        config = {
            "SUPABASE_URL": "https://xyz.supabase.co",
            "SUPABASE_KEY": "secret-supabase-key",
            "NEON_DB_URL": "postgres://user:pass@ep-lucky-smoke-123.us-east-2.aws.neon.tech/neondb"
        }
        with self.assertLogs("stacksorbit_infra", level="DEBUG") as cm:
            InfrastructureWiring(config)

        self.assertTrue(any("<redacted>" in m for m in cm.output), "Expected redacted debug log")
        self.assertFalse(any("xyz.supabase.co" in m for m in cm.output), "Supabase URL should be redacted")

    def test_log_deployment_redacts_outbound_payload(self):
        """Verify that InfrastructureWiring redacts sensitive data in outbound payloads."""
        config = {
            "SUPABASE_URL": "https://xyz.supabase.co",
            "SUPABASE_KEY": "secret-supabase-key",
        }
        infra = InfrastructureWiring(config)

        secret_module_name = "0123456789abcdef" * 4
        with patch("infrastructure_wiring.requests.post") as post:
            post.return_value.status_code = 201
            infra.log_deployment(secret_module_name, "success")
            sent = post.call_args.kwargs["json"]

        self.assertEqual(sent["module_name"], "<redacted>")

if __name__ == "__main__":
    unittest.main()
