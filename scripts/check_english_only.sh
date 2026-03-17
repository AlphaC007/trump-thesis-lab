#!/usr/bin/env bash
set -euo pipefail

files=$(git ls-files | grep -Ev "\\.(png|jpg|jpeg|webp|gif|ico|pdf|zip|gz|tgz|woff2?)$" || true)

if [ -z "${files}" ]; then
  echo "No files to scan."
  exit 0
fi

if echo "${files}" | xargs -r grep -nP "[\x{4E00}-\x{9FFF}]" -- >/dev/null; then
  echo "CJK characters detected in tracked files. Public repo must be English-only." >&2
  echo
  echo "Matches:" >&2
  echo "${files}" | xargs -r grep -nP "[\x{4E00}-\x{9FFF}]" -- || true
  exit 1
fi

echo "OK: no CJK characters found in tracked files."
