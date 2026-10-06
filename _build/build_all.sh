#!/bin/sh
# Rebuild every generated page, in dependency order. The OG step must be last:
# the other builders rewrite pages without og:image tags.
set -e
cd "$(dirname "$0")/.."
python3 _build/build_beer.py
python3 _build/build_usecases.py
python3 _build/business_cases.py > /dev/null
python3 _build/build_whitepapers.py
python3 _build/build_articles.py
python3 _build/build_credits.py
python3 _build/build_og.py
