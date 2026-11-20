"""
CinemaNexus - Safety Filters & Regex Rules
==========================================
Deterministic injection patterns, PII detection expressions, and operational thresholds.
"""

import re

# Prompt injection detection patterns (deterministic, zero external deps)
INJECTION_PATTERNS: list[re.Pattern] = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|directives|prompts)",
        r"reveal\s+(your\s+)?(system|initial)\s+(prompt|instruction)",
        r"developer\s+mode",
        r"override\s+(safety)",
        r"act\s+as\s+(an?\s+)?(unrestricted|unfiltered|jailbroken)",
    ]
]

# Personally Identifiable Information (PII) redaction rules
PII_PATTERNS: dict[str, re.Pattern] = {
    "[EMAIL REDACTED]": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "[PHONE REDACTED]": re.compile(
        r"(?:\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    ),
    "[SSN REDACTED]": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
}

# Operational safety limits
MAX_WATCHLIST_SIZE = 50
MAX_TITLE_LENGTH = 200
