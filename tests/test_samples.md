# Test Results

Python version used: 3.13.2 | Operating system: Windows (win32) | Date: 2026-10-28

| # | Input | Expected result | Actual result | Pass/Fail |
|---|-------|-----------------|---------------|-----------|
| 1 | `https://www.example.com/login` | No listed warning signs | `No listed warning signs found. This does NOT prove safety.` | PASS |
| 2 | `http://192.0.2.10/account` | IP address + HTTP | `Uses an IP address instead of a familiar domain.`<br>`Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 2 warning sign(s) found.` | PASS |
| 3 | `http://example.com@sample.invalid/login` | @ symbol + HTTP | `Contains an @ symbol; inspect carefully.`<br>`Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 2 warning sign(s) found.` | PASS |
| 4 | `https://a.b.c.d.e.example.invalid/path` | Many hostname segments | `Contains many hostname segments/subdomains.`<br>`REVIEW CAREFULLY: 1 warning sign(s) found.` | PASS |
| 5 | `https://xn--example.invalid/` | Punycode-style hostname | `Contains a punycode-style hostname.`<br>`REVIEW CAREFULLY: 1 warning sign(s) found.` | PASS |
| 6 | ` ` (blank / Enter) | Handles empty input gracefully | `No URL entered.` | PASS |
| 7 | `www.example.com` | Defaults missing scheme to HTTP; flags HTTP | `Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 1 warning sign(s) found.` | PASS |
| 8 | `https://secure-login.example.invalid` | No listed signs (illustrates heuristic limitation: clean deceptive domain) | `No listed warning signs found. This does NOT prove safety.` | PASS |
| 9 | `http://[bad` | Graceful error handling (Improvement C); avoids crash on malformed IPv6 | `This text is not a valid URL format.` | PASS |
| 10 | `https://www.example.com/` + 90 `a`s (114 chars) | Flags URL length exceeding 100 characters | `Unusually long URL (over 100 characters).`<br>`REVIEW CAREFULLY: 1 warning sign(s) found.` | PASS |
| 11 | `q` (or `quit`, `exit`) | Clean program termination (Improvement A) | `Goodbye! Stay alert online.` (clean exit code 0) | PASS |
| 12 | Multi-check session (consecutive URLs) | Evaluates multiple URLs without restart (Improvement A) | Evaluated both URLs consecutively with individual findings and reviews | PASS |
| 13 | `http://192.0.2.10:8080/account` | Flags IP address hostname with custom port and HTTP | `Uses an IP address instead of a familiar domain.`<br>`Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 2 warning sign(s) found.` | PASS |
| 14 | `http://user@bank.invalid/login` | Flags embedded @ credential symbol and HTTP | `Contains an @ symbol; inspect carefully.`<br>`Uses HTTP. HTTPS alone does not prove trust.`<br>`REVIEW CAREFULLY: 2 warning sign(s) found.` | PASS |

## Notes
- **What was learned**: Real-world URLs can disguise malicious destinations using browser specifications (such as the `@` credential delimiter) or internationalized domain names (punycode `xn--`). Heuristics are effective early indicators but must never be treated as definitive proof of safety.
- **What surprised me**: How easily Python's default `urllib.parse.urlparse` can crash with an unhandled `ValueError` when encountering malformed IPv6 brackets like `http://[bad`. Implementing the `try...except` block (Improvement C) made the tool much more resilient.
- **Verification status**: All 14 tests were executed directly in Python 3.13.2 on Windows and passed 100%.
