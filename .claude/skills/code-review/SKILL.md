---
name: code-review
description: Reviews code for bugs, security issues, and improvements. Use when the user asks for code review, wants feedback on their code, or mentions reviewing a file or PR.
---

# Code Review

## Process

1. **Read the code** - Understand structure and purpose
2. **Check for bugs** - Logic errors, edge cases, null handling
3. **Security scan** - Injection, auth issues, data exposure
4. **Performance** - Inefficiencies, N+1 queries, memory leaks
5. **Readability** - Naming, complexity, documentation

## Output Format

```markdown
## Summary
[One-sentence overall assessment]

## Issues Found
### Critical
- [Issue with file:line reference]

### Warnings  
- [Potential problems]

### Suggestions
- [Improvements for readability/performance]

## What's Good
- [Highlight positive patterns]
```

## Guidelines

- Be specific: reference file and line numbers
- Explain why something is an issue, not just what
- Provide fix suggestions when possible
- Acknowledge good patterns to reinforce them
- Prioritize: critical > warnings > suggestions
