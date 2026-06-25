# Copyright (c) 2025 Conxian-Labs
# This software is released under the MIT License.

import pytest
from conxius_orbit_secrets import is_sensitive_value, redact_recursive


def test_international_mnemonic_detection():
    # Spanish mnemonic (contains 2-letter word 'as', all lowercase)
    spanish = "as abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    assert is_sensitive_value(spanish) is True

    # Chinese mnemonic (single characters, non-caseable)
    chinese = "的 一 是 在 不 了 有 人 这 中 大 来"
    assert is_sensitive_value(chinese) is True


def test_casing_requirements():
    # All lowercase English mnemonic
    lower = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    assert is_sensitive_value(lower) is True

    # All uppercase English mnemonic
    upper = "ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABANDON ABOUT"
    assert is_sensitive_value(upper) is True

    # Title Case English mnemonic (should NOT be detected to avoid false positives in sentences)
    title = "Abandon Abandon Abandon Abandon Abandon Abandon Abandon Abandon Abandon Abandon Abandon About"
    assert is_sensitive_value(title) is False

    # Mixed case English sentence
    sentence = "The quick brown fox jumps over the lazy dog and then runs away now"
    # This has 14 words, so it shouldn't match anyway.
    # Let's try a 12-word mixed case sentence.
    sentence12 = "The quick brown fox jumps over the lazy dog and then runs now"
    assert is_sensitive_value(sentence12) is False


def test_sensitive_key_redaction():
    # Fields that are NOT in PUBLIC_SUBSTRINGS should be redacted if they contain a mnemonic
    sensitive_fields = ["MEMO", "NOTE", "COMMENT", "MESSAGE"]
    mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"

    for field in sensitive_fields:
        data = {field: mnemonic}
        redacted = redact_recursive(data)
        assert redacted[field] == "<redacted>"


def test_non_public_redaction():
    # A generic key with a value that looks like a mnemonic should still be redacted
    mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
    data = {"some_generic_key": mnemonic}
    redacted = redact_recursive(data)
    assert redacted["some_generic_key"] == "<redacted>"
