# Verification records

## MSE training (2026-10-11)

[`mse_only_update.json`](mse_only_update.json) and [`mse_only_tests.log`](mse_only_tests.log)
record nine passing tests covering MSE values, six-epoch training with 4/16 successor
samples, checkpoint reload, and rejection of unsupported loss settings.

## Model and policy checks

[`release_checks.json`](release_checks.json), [`solver_migration.json`](solver_migration.json),
and [`cli_execution_checks.json`](cli_execution_checks.json) record the earlier checks:

- Seven numerical and integration tests passed.
- All 1,600 cached evaluation paths matched the source generator.
- Four fixed PICNN policies were each replayed on 400 test paths with HiGHS.
- Eight SDDP cut banks were each replayed on three representative paths.
- Six- and 24-stage PICNN training used the default 256/64-unit network, followed
  by checkpoint selection, reload, and four-policy evaluation.
- Short six- and 24-stage runs covered eight- and 27-node SDDP training and evaluation.

Full 10,000-epoch retraining was outside the scope of these checks.
