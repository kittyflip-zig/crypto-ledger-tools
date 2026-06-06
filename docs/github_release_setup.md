# GitHub Release Setup

## Purpose

This note explains the GitHub-side setup needed before publishing `crypto-ledger-tools`.

## 1. GitHub Issues

Use GitHub Issues as the primary contact channel for:

- Bug reports
- Feature requests
- CSV template change reports
- Documentation improvements
- Implementation suggestions

Do not use public Issues for:

- Real transaction CSV files
- Wallet address values
- API keys
- Personal data
- Security vulnerabilities

## 2. Issue Notifications

Recommended maintainer setup:

1. Open the GitHub repository page.
2. Click `Watch`.
3. Select `Custom`.
4. Enable `Issues` and any other events you want.
5. Open GitHub notification settings.
6. Enable web and/or email notifications.

If you only want direct mentions and conversations you join, use the lighter `Participating and @mentions` setting.

## 3. Sponsor Link

Recommended first support channel:

```text
GitHub Sponsors
```

Setup steps:

1. Enable GitHub Sponsors for the maintainer account or organization.
2. Create sponsorship tiers.
3. Complete required payout, bank, tax, and two-factor authentication settings.
4. Add `.github/FUNDING.yml` to the published repository.
5. Add the sponsor account name to `github:`.
6. Confirm the Sponsor button appears on the repository page.

Example `FUNDING.yml`:

```yaml
github: [YOUR_GITHUB_ACCOUNT_OR_ORG]
```

If GitHub Sponsors is not ready at first release, use the README text to ask for Stars, Issues, and CSV template reports first. Add the funding link after the sponsor account is ready.

## 4. README Support Text

Recommended Japanese README text:

```text
このOSSが役に立った場合は、GitHub Star、Issueでのフィードバック、CSVテンプレート変更情報の共有で応援していただけると助かります。

開発継続を支援いただける場合は、GitHub Sponsorsからの支援も歓迎します。
```

## 5. Release Gate

Before public release:

- [ ] Issues are enabled.
- [ ] Maintainer notification settings are checked.
- [ ] GitHub Sponsors account or alternative support page is decided.
- [ ] `.github/FUNDING.yml` is added only after the real sponsor account is confirmed.
- [ ] README support link is updated from placeholder to real URL.
