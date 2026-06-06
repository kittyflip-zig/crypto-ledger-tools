# Contributing

Thank you for considering a contribution.

## Ground Rules

- Keep sample data fictional.
- Do not add real transaction records.
- Do not add credentials, cookies, tokens, or personal data.
- Do not present outputs as tax, accounting, investment, legal, or trading advice.
- Keep changes small and covered by tests.

## Development

```powershell
cd software/oss_candidates/crypto-ledger-tools
python -m pip install -e ".[dev]"
python -m pytest
```

## Pull Request Checklist

- [ ] Tests pass.
- [ ] New behavior is documented.
- [ ] Sample data is fictional.
- [ ] No sensitive or personal data is included.
- [ ] Calculations are described as tooling checks, not advice.
