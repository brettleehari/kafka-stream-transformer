#!/bin/bash
# Clean up unnecessary files and folders for production/deployment
rm -rf data/
rm -rf notebooks/
rm -rf .devcontainer/
rm -rf .vscode/
rm -rf app/__pycache__/
