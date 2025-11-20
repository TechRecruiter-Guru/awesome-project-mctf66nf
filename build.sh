#!/bin/bash
set -o errexit

echo "Upgrading pip, setuptools, and wheel..."
pip install --upgrade pip setuptools wheel

echo "Installing requirements..."
pip install -r backend/requirements.txt

echo "Build complete!"
