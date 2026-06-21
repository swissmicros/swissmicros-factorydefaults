# Zip-artifact release pipeline for swissmicros-factorydefaults

**Date:** 2026-06-20
**Status:** SUPERSEDED by `2026-06-21-raw-file-manifest-design.md`

> The firmware was refactored to download individual raw files (dropping
> on-device unzip), so the zip release pipeline described below is no longer
> used. It has been removed (`scripts/build-release.sh`,
> `.github/workflows/build-release.yml`). Kept for history.

## Background

The `swissmicros-esp32s3-toolkit` firmware was rewritten to download **zip
files** of calculator factory-default files instead of fetching individual
files. The firmware module `esp32_calculator_flasher/main/firmware_download.cpp`
fetches its inputs from this repository's GitHub releases:

```
https://github.com/swissmicros/swissmicros-factorydefaults/releases/latest/download/<asset>
```

It expects three kinds of assets on the **latest** release:

- `models.json` — a manifest
- `Voyager_Models.zip` — all Voyager `.hex` files
- one `<model>.zip` per Pioneer model

This repository currently has **no CI** and produces none of these assets. This
spec adds a pipeline that builds and publishes them.

## Goals

Produce, on every change to the model files, a rolling "latest" GitHub release
carrying the zip artifacts and manifest the firmware needs.

## Manifest format

`models.json` must match the keys read by `fwdl_parse_manifest_file`:

```json
{
  "voyager_zip": "Voyager_Models.zip",
  "voyager_version": "34",
  "pioneer": [
    { "name": "DM32", "zip": "DM32.zip" }
  ]
}
```

Constraints honored: ≤24 pioneer entries, `name` ≤24 chars, `zip` ≤48 chars,
`voyager_version` ≤24 chars (incl. NUL).

`voyager_version` is an opaque string the firmware compares against the
last-applied version stored on FAT; it re-downloads the Voyager zip when the
value differs (even if the files are already present). It is derived from the
shared version tag in the Voyager `.hex` filenames — the last
underscore-delimited token before `.hex` (`DM10_34.hex`, `DM15_M80_34.hex` →
`34`). If files disagree on the tag, the distinct tags are joined with `-` and a
warning is logged. Only Voyager is versioned; Pioneer entries stay `{name, zip}`
and are downloaded only when absent.

## Zip structure

The firmware strips exactly **one** leading path component when extracting, so
zip entries keep their top-level folder:

| Asset | Entry example | Lands at (on device) |
|-------|---------------|----------------------|
| `Voyager_Models.zip` | `Voyager_Models/DM11_34.hex` | `/data/Voyager_Models/DM11_34.hex` |
| `DM32.zip` | `DM32/HELP/dm32help.html` | `/data/Pioneer_Models/DM32/HELP/dm32help.html` |

Nested directories (`HELP/`, `OFFIMG/`) are preserved.

## Components

### `scripts/build-release.sh`
Builds `dist/`:
- `dist/Voyager_Models.zip` from the `Voyager_Models/` directory.
- `dist/<model>.zip` for **each subdirectory** of `Pioneer_Models/`.
- `dist/models.json` (hand-written JSON — model names are safe ASCII, no
  escaping needed; avoids a `jq` dependency). Includes `voyager_version` parsed
  from the `.hex` filenames when Voyager files are present.

Rules:
- Only subdirectories of `Pioneer_Models/` become models. Loose top-level files
  such as `DM42_qspi_3.x.bin` are ignored.
- Empty directories are skipped.
- Deterministic: file lists are `LC_ALL=C sort`ed and zipped with `zip -X`
  (drops extra metadata), so unchanged content yields identical archives.
- `set -euo pipefail`; fails if zero artifacts are produced.

### `.github/workflows/build-release.yml`
- **Triggers:** push to `main` touching `Pioneer_Models/**`, `Voyager_Models/**`,
  the build script, or the workflow itself; plus `workflow_dispatch`.
- **Permissions:** `contents: write`.
- **Concurrency:** single `factory-defaults-release` group, cancel-in-progress.
- **Publish:** `softprops/action-gh-release@v2` with `tag_name: latest`,
  `make_latest: true`, `files: dist/*`. Re-runs upsert assets so the single
  rolling release always reflects the newest files.

### `.gitignore`
Adds `/dist/` — generated artifacts are never committed.

## Decisions

- **Release strategy:** rolling `latest` release updated on every push to `main`
  (no manual tagging).
- **Loose top-level Pioneer files:** ignored.

## Testing

No test suite exists. Validation is by running `scripts/build-release.sh`
locally and confirming:
- `unzip -l` shows the correct one-level path prefixes.
- `DM42_qspi_3.x.bin` appears in no archive.
- `models.json` is valid JSON with the expected keys.
- A rebuild produces byte-identical zips (determinism).

All of the above were verified during implementation.
