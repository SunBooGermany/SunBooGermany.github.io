# Release verification

Validated with Python 3.12.14 and the versions in requirements.txt.

- All 11 selected numerical tests passed.
- All four full annual proposed-method runs reproduced the archived final generator arrays exactly and passed operating recovery.
- Reconstructed Figures 7 and 8 are byte-identical PNGs to the submitted manuscript figures.
- The optional cached Jeju 1% run converged and every stored vertex distance passed independent fresh-LP checks.
- Core model class and function bodies match the study implementation.
- Six original ERA5 input archives retain their exact hashes.

Details are in `release_validation.json`. Annual ORACLE/G-ORACLE measurements are archived under `reference_results/performance/`. The numerical tests cover small hourly ORACLE/G-ORACLE workflows.
