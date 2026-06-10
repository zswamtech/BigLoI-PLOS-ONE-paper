# Code package

This folder is reserved for the minimal code needed to reproduce the article outputs.

Recommended public contents:

- scripts that regenerate figure-ready CSV outputs;
- scripts that regenerate summary tables;
- documentation of required software and versions;
- exact commands used for figure export and conversion where relevant.

The goal is not to expose the entire monorepo here, but to isolate the minimum reproducible path for the paper.

Current status:

- source-data regeneration scripts are available in code/scripts/;
- exploratory simulation scripts are available in code/scripts/ for inventory-criticality analysis;
- environment notes still need to be finalized in code/environment/ before public release.

Additional exploratory script:

- code/scripts/simulate_inventory_soc.py runs a self-organized-criticality style simulation for pharmaceutical inventories under supplier concentration, stochastic demand, and cascading stockouts;
- code/scripts/run_inventory_soc_simulation.sh is the recommended entry point from the workspace root because it prefers the project virtual environment when available.
