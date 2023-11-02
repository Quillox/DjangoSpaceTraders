#!/bin/bash

# List of apps
apps=("agents" "contracts" "factions" "fleet" "player" "systems")

# Loop over each app
for app in "${apps[@]}"; do
    # Navigate to the migrations directory of the app
    cd "${app}/migrations"

    # Remove all files except __init__.py
    find . ! -name '__init__.py' -type f -exec rm -f {} +
    # Trial run with ls
    # find . ! -name '__init__.py' -type f -exec ls {} +

    # Navigate back to the parent directory
    cd ../..
done