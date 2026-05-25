# Security Policy

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

Report vulnerabilities to **security@quantumworld.io** with the following:

- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Any proof-of-concept code

We will acknowledge receipt within 48 hours and provide a timeline for remediation.

## Security Response

1. Acknowledgment: 48 hours
2. Triage: 5 business days
3. Fix development: 14 business days
4. Release: Coordinated disclosure

## OWASP Top 10 Coverage

This project is tested against OWASP Top 10 (2021) using Robot Framework:

- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable & Outdated Components
- A07: Identification & Authentication Failures
- A08: Software & Data Integrity Failures
- A09: Security Logging & Monitoring Failures
- A10: Server-Side Request Forgery

## Secure Development

- All code is type-checked with mypy (strict mode)
- Linted with ruff (security rules enabled)
- Dependencies scanned with `safety`
- SAST scanning with `bandit`
- OWASP ZAP baseline scans run on every PR
