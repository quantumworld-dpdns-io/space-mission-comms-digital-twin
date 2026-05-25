# Contributing

## Commit Convention

This project uses **Conventional Commits** enforced by semantic-release:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`, `revert`

Examples:
- `feat(qkd): add decoy-state BB84 protocol`
- `fix(link-budget): correct rain attenuation formula`
- `test(quantum): add QSVM unit tests`
- `ci(security): add OWASP ZAP baseline scan`

## Multi-Language Guidelines

### Python
- Type hints required (mypy strict mode)
- Format with ruff
- Test with pytest

### Go
- Follow standard Go conventions
- `go vet` and `golint` must pass
- Use `testing` package

### Rust
- Clippy must pass with no warnings
- Format with `rustfmt`
- Document all public APIs

### Julia
- Follow Julia `BlueStyle` conventions
- Document all exported functions
- Use `Test` package

### Qwik Frontend
- Follow Qwik conventions
- Test with Vitest
- TypeScript strict mode

### OpenQASM
- Version 3.0 format
- Include header comments with circuit description
- All files must validate with `qasm3` parser

## Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all CI checks pass (lint, typecheck, test, security)
4. Reference related TODOS.md item number
5. Request review from maintainers
