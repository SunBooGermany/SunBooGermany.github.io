# Verification

## MSE training checks (2026-10-11)

`mse_only_update.json` and `mse_only_tests.log` record nine passing tests of the
current code. They include numeric MSE verification, default MSE training with
4/16 successors, checkpoint reload, and rejection of unsupported loss settings.

## Numerical and integration checks

- Seven numerical/integration tests passed.
- All 1,600 cached source evaluation paths match the source generator.
- Four fixed PICNN policies were each replayed on all 400 original test paths with HiGHS.
- Eight SDDP reference cut banks were replayed on three representative paths each.
- Default 256/64-unit PICNN training, checkpoint selection, reload, and four-policy evaluation ran for both six and 24 stages.
- New eight- and 27-node SDDP training/evaluation ran in short six- and 24-stage checks.

See the JSON records for configurations and measured differences. Full 10,000-epoch retraining was not performed.
