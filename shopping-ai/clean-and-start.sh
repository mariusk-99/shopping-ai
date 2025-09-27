#!/bin/bash
echo "Cleaning up build artifacts..."
rm -rf build/
rm -rf node_modules/.cache/

echo "Installing dependencies..."
pnpm install

echo "Starting development server..."
pnpm dev
