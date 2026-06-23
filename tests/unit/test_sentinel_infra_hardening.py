import unittest
from unittest.mock import patch

from infrastructure_wiring import InfrastructureWiring, logger as infra_logger
from conxius_orbit_secrets import is_sensitive_key, redact_recursive


class TestSentinelInfraHardening(unittest.TestCase):
    def test_new_infra_keywords(self):
        """Verify that new infra keywords are identified as sensitive."""
        infra_keywords = [
            "SUPABASE_KEY",
            "NEON_DB_URL",
            "POSTGRES_PASSWORD",
            "MONGODB_URI",
            "REDIS_AUTH",
            "AWS_SECRET_ACCESS_KEY",
            "AZURE_STORAGE_KEY",
            "GCP_SERVICE_ACCOUNT",
            "DIGITALOCEAN_TOKEN",
        ]
        for kw in infra_keywords:
            self.assertTrue(is_sensitive_key(kw), f"Keyword '{kw}' should be sensitive")

    def test_infra_init_logs_redacted_urls(self):
        """Verify that InfrastructureWiring redacts sensitive fields in debug logs."""
        config = {
            "SUPABASE_URL": "https://xyz.supabase.co",
            "SUPABASE_KEY": "secret-supabase-key",
            "NEON_DB_URL": "postgres://user:pass@ep-lucky-smoke-123.us-east-2.aws.neon.tech/neondb",
        }
        with self.assertLogs(infra_logger, level="DEBUG") as cm:
            InfrastructureWiring(config)

        self.assertTrue(
            any("<redacted>" in m for m in cm.output), "Expected redacted debug log"
        )
        self.assertFalse(
            any("xyz.supabase.co" in m for m in cm.output),
            "Supabase URL should be redacted",
        )

    def test_log_deployment_redacts_outbound_payload(self):
        """Verify that InfrastructureWiring redacts sensitive data in outbound payloads."""
        config = {
            "SUPABASE_URL": "https://xyz.supabase.co",
            "SUPABASE_KEY": "secret-supabase-key",
        }
        infra = InfrastructureWiring(config)

        secret_module_name = "0123456789abcdef" * 4
        # Bolt ⚡: Mock the session.post instead of requests.post
        with patch.object(infra.session, "post") as post:
            post.return_value.status_code = 201
            infra.log_deployment(secret_module_name, "success")
            sent = post.call_args.kwargs["json"]

        self.assertNotEqual(sent["module_name"], secret_module_name)
        self.assertNotIn(secret_module_name, str(sent))

    def test_redact_recursive_masks_neon_db_url(self):
        """Verify nested infra keys remain redacted by redact_recursive."""
        payload = {
            "metadata": {
                "NEON_DB_URL": "postgres://user:pass@ep-lucky-smoke-123.us-east-2.aws.neon.tech/neondb"
            }
        }
        redacted = redact_recursive(payload)
        self.assertEqual(redacted["metadata"]["NEON_DB_URL"], "<redacted>")


if __name__ == "__main__":
    unittest.main()
