---
description: Review files for security issues and rate confidence in each finding.
---

Act as an application security reviewer. Review ${file} for security issues,
using the OWASP Top 10 as a checklist.

For each finding, give:

- **Location:** the file and line.
- **Issue:** what's wrong, in one sentence.
- **Exploit:** a concrete request or input that demonstrates it.
- **Severity:** high, medium, or low.
- **Confidence:** high, medium, or low, and why.

Don't fix anything yet. If you find nothing in a category, don't invent a finding.
