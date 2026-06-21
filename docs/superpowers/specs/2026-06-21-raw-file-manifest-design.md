# Raw-file manifest for swissmicros-factorydefaults

**Date:** 2026-06-21
**Status:** Approved
**Supersedes:** `2026-06-20-zip-artifact-release-design.md`

## Background

The `swissmicros-esp32s3-toolkit` firmware was refactored (commit `2e48609`,
"download firmware files directly, drop on-device unzip") to fetch calculator
firmware as **individual raw files** rather than release zips. It reads:

```
https://raw.githubusercontent.com/swissmicros/swissmicros-factorydefaults/main/models.json
```

and then downloads each listed file from the same raw base
(`firmware_download.cpp`: `FWDL_MANIFEST_URL`, `fwdl_download_path`).

The previous zip pipeline published `models.json` (in a `voyager_zip` /
`pioneer[].zip` shape) as a *release asset only*, so the raw URL 404'd and the
device's model lists came up empty. This spec replaces that pipeline.

## Manifest format

`models.json` is **committed to the repo root on `main`** and matches the keys
read by `fwdl_parse_manifest_file` / `fwdl_load_manifest_json`:

```json
{
  "voyager_version": "34",
  "voyager": [ "Voyager_Models/DM10_34.hex", "..." ],
  "pioneer": [
    { "name": "DM32", "files": [ "Pioneer_Models/DM32/DMCP5_flash_3.56_DM32-2.11.bin", "..." ] }
  ]
}
```

- Paths are **repo-relative** and keep their top-level folder, so the device
  stores each at `/data/<path>` (`/data/Voyager_Models/…`,
  `/data/Pioneer_Models/<model>/…`).
- `voyager_version` is the shared tag from the `.hex` filenames (last
  underscore-delimited token before `.hex`: `DM15_M80_34.hex` → `34`). The
  firmware re-downloads the Voyager files when it changes.
- `base_url` is omitted; the firmware defaults to the raw `main` base.
- Loose top-level files in `Pioneer_Models/` (e.g. `DM42_qspi_3.x.bin`) are not
  model directories and are ignored.

Constraints: ≤24 pioneer entries, `name` ≤24 chars, `voyager_version` ≤24 chars,
and the whole file must stay under 32 KB (the firmware's parse buffer cap). The
current file is ~20 KB.

## Components

### `scripts/generate-manifest.py`
Walks `Voyager_Models/` and each `Pioneer_Models/` subdirectory, emits
`models.json` at the repo root (deterministic: directories and files sorted).
Fails if no model files are found. Python 3 stdlib only (`json` handles
escaping).

### `.github/workflows/update-manifest.yml`
On push to `main` touching the model dirs or the generator (plus
`workflow_dispatch`): regenerate `models.json` and, if it changed, commit it back
to `main` with `[skip ci]` (mirrors the org's existing auto-commit pattern).

### Removed
`scripts/build-release.sh`, `.github/workflows/build-release.yml`, and the
`/dist/` `.gitignore` entry — the zip pipeline is gone.

## Testing

No test suite. Verified by running the generator locally and confirming:
- `models.json` is valid JSON, < 32 KB, with the expected keys/paths.
- Sample raw URLs (`Voyager_Models/DM10_34.hex`,
  `Pioneer_Models/DM32/HELP/dm32help.html`) return HTTP 200 on `main`.

## Follow-up

The stale `latest` GitHub release (and its `tag`) from the old zip pipeline are
now misleading and should be deleted.
