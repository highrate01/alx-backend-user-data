#!/usr/bin/env python3
"""Regex-ing"""
import re


def filter_datum(fields, redaction, message, separator):
    """Obfuscate specified fields in the log message."""
    pattern = rf'({"|".join(map(re.escape, fields))})\s*=\s*[^{separator}]*'
    return re.sub(pattern, rf'\1={redaction}', message)
