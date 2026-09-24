#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"
mise trust
mise install
mise run catalog:install .
