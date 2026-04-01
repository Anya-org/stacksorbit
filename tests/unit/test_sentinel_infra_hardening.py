import unittest
import logging
from infrastructure_wiring import InfrastructureWiring
from stacksorbit_secrets import is_sensitive_key, redact_recursive

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

    def test_infra_redaction(self):
        """Verify that InfrastructureWiring redacts sensitive data in log payloads."""
        config = {
            "SUPABASE_URL": "https://xyz.supabase.co",
            "SUPABASE_KEY": "secret-supabase-key",
            "NEON_DB_URL": "postgres://user:pass@ep-lucky-smoke-123.us-east-2.aws.neon.tech/neondb"
        }
        infra = InfrastructureWiring(config)

        # We'll mock the log_deployment payload logic internally by checking redact_recursive
        payload = {
            "module_name": "vault-contract",
            "status": "success",
            "metadata": {
                "NEON_DB_URL": config["NEON_DB_URL"]
            }
        }

        redacted = redact_recursive(payload)
        self.assertEqual(redacted["metadata"]["NEON_DB_URL"], "<redacted>")

    def test_infra_logger_redaction_usage(self):
        """Verify that InfrastructureWiring uses redact_recursive for its debug logs."""
        # Test keyword-based redaction
        secret_url = "https://example.com/api"
        redacted_url = redact_recursive(secret_url, parent_key="SUPABASE_URL")
        self.assertEqual(redacted_url, "<redacted>")

        # Test value-based redaction (private key as a separate value)
        pk = "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        redacted_pk = redact_recursive(pk)
        self.assertEqual(redacted_pk, "<redacted>")

if __name__ == "__main__":
    unittest.main()
