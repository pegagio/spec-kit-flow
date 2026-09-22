#!/usr/bin/env bash
set -euo pipefail

# Proves that a clean consumer cannot claim success when a required component
# is unavailable. This fixture intentionally does not install any components.

specify_bin=${SPECIFY_BIN:?Set SPECIFY_BIN to the compatible specify executable.}
source_root=${SPEC_KIT_FLOW_ROOT:?Set SPEC_KIT_FLOW_ROOT to the Spec Kit Flow checkout.}
fixture_root=$(mktemp -d "${TMPDIR:-/tmp}/spec-kit-flow-missing.XXXXXX")
trap 'rm -rf "$fixture_root"' EXIT

cd "$fixture_root"
"$specify_bin" init --here --force --non-interactive --integration codex --integration-options="--skills" >/dev/null
if "$specify_bin" bundle install "$source_root/bundles/spec-kit-flow/bundle.yml" --offline; then
  echo "expected missing required components to reject installation" >&2
  exit 1
fi

if "$specify_bin" bundle list | grep -q "spec-kit-flow"; then
  echo "failed installation incorrectly recorded a compatible bundle" >&2
  exit 1
fi

echo "missing required components were explicit and no bundle was recorded"
