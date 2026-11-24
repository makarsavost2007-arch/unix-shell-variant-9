#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
for image in minimal files deep; do
  ./run.sh --vfs "examples/$image.json" --script examples/basic.txt
done
