# GAIA Ablations on Frozen v116

Both ablations use the frozen `v116` agent pool and GAIA `test_100`.

## 1. Without handoff rules

Pool: `pool_GAIA_ablation_wo_handoff_v116`

Family/template selection remains enabled. Handoff rules are not loaded into
the Runner context and are not available to agents.

## 2. Without templates and handoff rules

Pool: `pool_GAIA_ablation_wo_template_handoff_v116`

Family/template selection is disabled. The Chairman starts with the full
global agent pool and recruits directly. Handoff rules are also disabled.

These settings are consumed internally by the adapter and do not add new
agent-facing instructions or command-line flags.
