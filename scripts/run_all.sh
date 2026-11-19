#!/bin/bash
set -e
cd /workspace/south-carolina-elections
python3 scripts/pass_a.py
python3 scripts/pass_b.py > /dev/null
python3 scripts/compare_passes.py > /dev/null
python3 scripts/analysis.py > /dev/null
python3 scripts/charts.py
python3 scripts/build_wiki.py
python3 scripts/verify_wiki.py
python3 -c "import json;r=json.load(open('verification/compare_report.json'));print('compare:',r['total_comparisons'],'comparisons',r['matched'],'matched',r['mismatched'],'mismatched; analysis-figure mismatches:',len(r['mismatches_in_analysis_figures']))"
