---
name: git-commits
description: Generates descriptive commit messages from staged changes. Use when the user asks for help writing commit messages, wants to commit changes, or asks about git diff.
---

# Git Commit Messages

## Format

```
type(scope): brief description

- Detail about what changed
- Why it was changed (if not obvious)
```

## Types

- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring (no behavior change)
- `docs` - Documentation only
- `test` - Adding/updating tests
- `chore` - Maintenance (deps, config, build)
- `perf` - Performance improvement
- `style` - Formatting (no code change)

## Workflow

1. Run `git diff --staged` to see changes
2. Identify the primary change type
3. Determine scope (component/module affected)
4. Write brief description (imperative mood, no period)
5. Add bullet points for multiple changes

## Examples

**Single change:**
```
feat(auth): add JWT token refresh endpoint
```

**Multiple changes:**
```
refactor(api): restructure error handling

- Extract error codes to constants
- Add custom exception classes
- Standardize error response format
```

**Bug fix:**
```
fix(orders): prevent duplicate order creation

Race condition allowed double-submit. Added idempotency key check.
```
