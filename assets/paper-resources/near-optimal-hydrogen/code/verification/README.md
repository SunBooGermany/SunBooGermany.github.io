# Release verification

Validated with Python 3.12.14 and the versions in requirements.txt.

- All 11 selected numerical tests passed.
- All four full annual proposed-method runs reproduced the archived final generator arrays exactly and passed operating recovery.
- Reconstructed Figures 7 and 8 are byte-identical PNGs to the submitted manuscript figures.
- The optional cached Jeju 1% run converged and every stored vertex distance passed independent fresh-LP checks.
- The extracted core model class/function bodies are structurally identical to the working study implementation. Imports were made package-relative and unrelated entry points were omitted.
- Six original ERA5 input archives retain their exact hashes.

The record is release_validation.json. This validation did not remeasure the hours-long full annual ORACLE/G-ORACLE runs; their original audited measurements are archived under reference_results/performance/. Small hourly ORACLE/G-ORACLE workflows are covered by the numerical tests.
