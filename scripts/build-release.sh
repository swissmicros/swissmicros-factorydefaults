#!/usr/bin/env bash
#
# Build the release artifacts consumed by the swissmicros-esp32s3-toolkit
# firmware (esp32_calculator_flasher/main/firmware_download.cpp):
#
#   dist/Voyager_Models.zip   all Voyager .hex files
#   dist/<model>.zip          one zip per Pioneer_Models subdirectory
#   dist/models.json          manifest listing the above
#
# Zip entries deliberately keep their top-level folder name (e.g.
# "Voyager_Models/DM11_34.hex", "DM32/HELP/dm32help.html"); the firmware
# strips exactly one leading path component on extraction, so files land in
# /data/Voyager_Models/ and /data/Pioneer_Models/<model>/ respectively.
#
# Loose top-level files in Pioneer_Models/ (e.g. DM42_qspi_3.x.bin) are NOT
# model directories and are intentionally ignored.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

DIST="$ROOT/dist"
rm -rf "$DIST"
mkdir -p "$DIST"

produced=0

dir_has_files() { find "$1" -type f -print -quit | grep -q .; }

# --- Voyager: one zip with every model file ---
voyager_zip=""
if [ -d Voyager_Models ] && dir_has_files Voyager_Models; then
  find Voyager_Models -type f | LC_ALL=C sort | zip -X -q "$DIST/Voyager_Models.zip" -@
  echo "built Voyager_Models.zip"
  voyager_zip="Voyager_Models.zip"
  produced=$((produced + 1))
fi

# --- Pioneer: one zip per model subdirectory ---
pioneer_names=()
if [ -d Pioneer_Models ]; then
  while IFS= read -r d; do
    name="$(basename "$d")"
    if dir_has_files "$d"; then
      ( cd Pioneer_Models && find "$name" -type f | LC_ALL=C sort | zip -X -q "$DIST/$name.zip" -@ )
      echo "built $name.zip"
      pioneer_names+=("$name")
      produced=$((produced + 1))
    fi
  done < <(find Pioneer_Models -mindepth 1 -maxdepth 1 -type d | LC_ALL=C sort)
fi

if [ "$produced" -eq 0 ]; then
  echo "error: no artifacts produced" >&2
  exit 1
fi

# --- models.json (model names are safe ASCII, so no JSON escaping needed) ---
{
  printf '{\n'
  printf '  "voyager_zip": "%s",\n' "$voyager_zip"
  printf '  "pioneer": [\n'
  for i in "${!pioneer_names[@]}"; do
    sep=","
    [ "$i" -eq $(( ${#pioneer_names[@]} - 1 )) ] && sep=""
    printf '    { "name": "%s", "zip": "%s.zip" }%s\n' "${pioneer_names[$i]}" "${pioneer_names[$i]}" "$sep"
  done
  printf '  ]\n'
  printf '}\n'
} > "$DIST/models.json"

echo "wrote models.json:"
cat "$DIST/models.json"
