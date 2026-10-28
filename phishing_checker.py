"""
EWB Cybersecurity Mini Project: Phishing URL Awareness Checker

A defensive, educational command-line tool that inspects URL text for visible
heuristic warning signs without making network requests or visiting websites.
"""

import re
from urllib.parse import urlparse

# Informational prefixes that do not represent suspicious security warnings
INFO_MESSAGES = (
    "No URL entered",
    "Could not identify",
    "This text is not a valid URL format",
    "No listed warning",
)


def inspect_url(raw_url: str) -> list[str]:
    """Check visible URL text for selected warning signs."""
    url = raw_url.strip()
    findings = []

    # Handle blank or whitespace-only input
    if not url:
        return ["No URL entered."]

    # If no scheme is present, prepend http:// so urlparse can reliably extract the host
    candidate = url if "://" in url else "http://" + url

    # Improvement C: Handle malformed input without crashing
    try:
        parsed = urlparse(candidate)
    except ValueError:
        return ["This text is not a valid URL format."]

    host = (parsed.hostname or "").lower()

    # Ensure a hostname could be parsed
    if not host:
        return ["Could not identify a hostname."]

    # Check 1: @ symbol in candidate URL
    if "@" in candidate:
        findings.append("Contains an @ symbol; inspect carefully.")

    # Check 2: Unusually long URL (over 100 characters)
    if len(url) > 100:
        findings.append("Unusually long URL (over 100 characters).")

    # Check 3: Raw IP address used as hostname instead of a domain name
    if re.fullmatch(r"(?:\d{1,3}\.){3}\d{1,3}", host):
        findings.append("Uses an IP address instead of a familiar domain.")

    # Check 4: Hostname contains 5 or more segments (subdomains)
    labels = [part for part in host.split(".") if part]
    if len(labels) >= 5:
        findings.append("Contains many hostname segments/subdomains.")

    # Check 5: Punycode marker (xn--) indicating internationalized look-alike characters
    if "xn--" in host:
        findings.append("Contains a punycode-style hostname.")

    # Check 6: Unencrypted HTTP scheme
    if parsed.scheme.lower() == "http":
        findings.append("Uses HTTP. HTTPS alone does not prove trust.")

    # Default result when none of the six specific warning signs were detected
    if not findings:
        findings.append("No listed warning signs found. This does NOT prove safety.")

    return findings


def has_warnings(findings: list[str]) -> bool:
    """Return True if findings contain genuine security warnings rather than info notices."""
    if not findings:
        return False
    return not findings[0].startswith(INFO_MESSAGES)


def main() -> None:
    """Run the interactive command-line interface."""
    print("=" * 50)
    print("EWB Phishing URL Awareness Checker")
    print("Text checks only - this program does not open URLs.")
    print("=" * 50)

    # Improvement A: Repeated checks in a loop with quit command
    while True:
        try:
            raw_url = input("\nEnter a sample URL (or type q to quit): ")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye! Stay alert online.")
            break

        # Check for quit signal
        if raw_url.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye! Stay alert online.")
            break

        findings = inspect_url(raw_url)

        print("\nResult:")
        for item in findings:
            print("- " + item)

        # Improvement B: Clear 'Review carefully' warning summary
        if has_warnings(findings):
            print(f"\nREVIEW CAREFULLY: {len(findings)} warning sign(s) found.")

        print("\nNever enter passwords from unexpected links.")


if __name__ == "__main__":
    main()
