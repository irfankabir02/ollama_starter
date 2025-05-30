#!/bin/bash
set -e

ROOT="$(pwd)"

echo "Cleaning nested tools folder..."
if [ -d "$ROOT/main/tools/tools" ]; then
  mv "$ROOT/main/tools/tools/"* "$ROOT/main/tools/"
  rmdir "$ROOT/main/tools/tools"
  echo "Flattened nested tools folder"
fi

echo "Removing unused TS frontend in web/src (optional)..."
if [ -d "$ROOT/web/src" ]; then
  rm -rf "$ROOT/web/src"
  echo "Removed web/src folder (React/TS frontend)"
fi

echo "Removing .ts init file in web/mcp..."
if [ -f "$ROOT/web/mcp/__init__.ts" ]; then
  rm "$ROOT/web/mcp/__init__.ts"
  echo "Removed TypeScript init file"
fi

echo "Ensuring __init__.py in main/tools and other modules..."
touch "$ROOT/main/__init__.py"
touch "$ROOT/main/tools/__init__.py"
touch "$ROOT/scripts/__init__.py"
touch "$ROOT/web/__init__.py"

echo "Done."
