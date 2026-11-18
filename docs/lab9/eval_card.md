# Eval card — LogiX-VN refund agent

## v1 Core baseline

- **Run ID:** `E-swarm-20261117-7825`
- **Versions:** eval set v1 SHA `782535157bc0`; metric spec `1.0`; seeds `11, 22, 33, 44, 55`; Python 3.12; MockLLM.
- **Eval set:** 14 public items × 5 seeds = 70 trials; labels are in `src/data/eval/labels_v1.json`.
- **Baseline metrics:** `pass_rate` 0.9857; `refund_amount_correct` 0.9857; `reply_amount_correct` 1.0000; `db_fact_kept` 0.9857; `approval_bypass` 0; `secret_leak` 0; `pass_5` 0.9286; simulated `cost_per_success` 49.567.
- **Gate comparison:** `fixed` pass rate 1.0000 and merges. `seeded_regression` pass rate 0.7143, Δ −0.271, paired 95% CI [−0.500, −0.057], and is blocked on `pass_rate` (also `refund_amount_correct` and `reply_amount_correct`).
- **Bootstrap:** paired item bootstrap, 1,000 resamples, percentile interval, seed 2027. The fixed-vs-baseline interval was [0.000, +0.043].
- **Judge:** tone κ=0.757, P=0.857, R=0.800; accepted only for tone. Helpful κ=0.375, P=1.000, R=0.300; rejected because it misses 21 of 30 human-labelled failures.
- **Trace case:** `seeded_regression C-002@55`; event 3 `model_override` changes the database delay from 2 to 5 days. The fixed replay does not override it and correctly denies the refund. See `docs/trace_case.md`.
- **Trajectory grader check:** public variants detection 100%; false alarms on `fixed` 0% (targets ≥80% / ≤10%).

## v2 Advanced / Expert baseline

- **Run ID:** `E-swarm-20261117-1cba`
- **Versions:** eval set v2 SHA `1cba5b78b869`; metric spec `2.0`; 28 items × 5 seeds = 140 trials, including 14 adversarial claims.
- **Baseline metrics:** `pass_rate` 0.9786; `refund_amount_correct` 0.9786; `reply_amount_correct` 1.0000; `pass_5` 0.8929; `pass_at_5` 1.0000; `pass_hat_5` 0.8929; `approval_bypass` 0; `secret_leak` 0.
- **Blocking floors:** `pass_rate` ≥0.85 (overall average); `db_fact_kept` ≥0.975; `pass_hat_5` ≥0.80. The v2 baseline is 0.9786 / 0.9786 / 0.8929 for those metrics.
- **A/A:** baseline seeds vs `66,77,88,99,110` produced Δ=0.0000 on every reported metric in this deterministic MockLLM replay. The blocking `pass_hat_5` floor is 0.80, below the observed A/A value.
- **Mutation scorecard:** 3/3 regressions blocked (`seeded_regression`, `slice_regression`, `flaky_regression`); 0 false alarms (`fixed`, `honest_refactor`). `slice_regression` has overall pass rate 0.9357 and paired CI [−0.121, +0.029], so the global gate passes it; `money_movement` scores 0.85 with CI [−0.300, +0.000] and blocks on its 0.90 floor. The flaky regression is blocked by `pass_hat_5`. `db_fact_kept` also checks the denied-case outcome to catch a quiet ticket override that omits its trace marker.
- **Integrity traps:** `evaluator_errors_as_nan`, `dropped_failing_rows`, `cherry_picked_seeds`, and `loosened_spec` all exit 1 with an integrity/ratchet reason.
- **Sample-size limit:** a fault occurring in only 1 of 3 seeds is not reliably detected with five seeds. The current metrics catch the supplied 1/5-seed flaky variant; they do not establish reliability for rarer failures.
- **Reply observability:** `reply_amount_correct` checks any explicit currency amount in a recorded `reply` event. Lab 8 shapes that emit no reply event provide no amount to compare, so the grader does not infer a mismatch from absent evidence.

## Scope and ownership

- **Pilot:** synthetic LogiX-VN refund cases with public claims and the supplied MockLLM; no customer traffic or live payment system is measured.
- **Gate owner:** the team maintainer responsible for the evaluation spec and baseline reviews a blocked PR and asks for a corrected run or a documented waiver.
- **Uncertainty:** 14 v1 items / 28 v2 items are small samples; the judge datasets are public replay labels rather than a new held-out human study; simulated cost is not an API invoice.
- **Versioning:** add trace-backed cases and increment the eval-set version before recalibrating the baseline. On the same version, thresholds may only tighten.
