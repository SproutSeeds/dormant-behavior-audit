# Release Metadata Check

- Benchmark: `Dormant Behavior Audit`
- Release status: `public`
- Passed: `5`
- Warnings: `0`
- Failed: `0`

| Status | Check | Expected | Actual | Basis |
|---|---|---|---|---|
| PASS | Release metadata includes required fields | schema_version, benchmark_name, benchmark_version, release_status, repo_url, paper_url, homepage_url | all present |  |
| PASS | schema_version is release_metadata_v0 | release_metadata_v0 | release_metadata_v0 |  |
| PASS | release_status is allowed | internal_draft, public, ready_for_release | public |  |
| PASS | Public-facing release states do not use placeholder URLs | repo_url, paper_url, homepage_url should be finalized | none |  |
| PASS | Public release includes an announcement date | non-empty announcement_date | 2026-04-07 |  |

All release-metadata checks passed without failures.
