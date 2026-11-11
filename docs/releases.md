# Releases

Release Please reads Conventional Commits on `main` and opens a release PR.
The PR updates `VERSION` and `CHANGELOG.md` together.
Release Please owns the changelog. Do not add manual `Unreleased` sections.
Merge that PR after CI passes.
Release Please then creates the matching tag and GitHub release.
The published release starts `publish.yml`, which builds and publishes the package through PyPI trusted publishing.
The workflow then updates the Hugging Face Space.

## GitHub App setup

Use the release GitHub App that also serves `k4black/hex`.
Hex uses release-plz for Rust. CodeBLEU uses Release Please for its Python package.
Both use App tokens so that release PRs and release events start other workflows.
The default `GITHUB_TOKEN` does not start those workflows.

1. Open <https://github.com/settings/installations>.
2. Select **Configure** for the release App.
3. Add `k4black/codebleu` to the selected repositories.
4. Open the App under <https://github.com/settings/apps>.
5. Set repository permissions for **Contents**, **Pull requests**, and **Issues** to **Read and write**.
6. Save the changes and accept any installation permission update.
7. Copy the numeric **App ID** from the App settings. Do not use the Client ID.
8. Use the existing App private key, or generate a private key from the App settings.
9. Open <https://github.com/k4black/codebleu/settings/secrets/actions>.
10. Add repository secret `RELEASE_APP_ID` with the numeric App ID.
11. Add repository secret `RELEASE_APP_PRIVATE_KEY` with the complete PEM private key, including its header and footer.

Do not add App bypass permissions to the branch ruleset.
The App creates ordinary PRs. A maintainer merges the release PR.

## PyPI setup

Keep the existing trusted publisher for project `codebleu` at <https://pypi.org/manage/project/codebleu/settings/publishing/>.
The publisher must name owner `k4black`, repository `codebleu`, workflow `publish.yml`, and environment `pypi`.
No PyPI API token is required.
Keep `HF_TOKEN` as a repository secret for the existing Hugging Face synchronization.

## First run

Configure the App before this workflow merges.
The manifest starts at the latest existing release, `0.7.1`.
After a releasable commit reaches `main`, inspect the generated release PR.
Run **Release please** manually from Actions if a retry is necessary.
Do not edit the generated tag or publish a second release for the same version.

## References

- [Release Please action](https://github.com/googleapis/release-please-action)
- [Simple strategy and version files](https://github.com/googleapis/release-please/blob/main/src/strategies/simple.ts)
- [Hex release workflow](https://github.com/k4black/hex/blob/main/.github/workflows/release-plz.yml)
