# MIX-COOP

MIX-COOP is a heterogeneous evaluation suite over LoCoBench, LOCA-Bench,
GAIA, and BeyondSWE. It shares one evolving collaboration memory while keeping
each benchmark's native task and evaluation semantics.

## Boundary contract

Shared across every task, in one sequential evolution lineage:

- the family catalog and current team templates (`templates.json`);
- family-scoped handoff rules (`handoff_rules.json`);
- Agent prompt patches, teammate profiles, and skills;
- team constitution and pool-level evolution state.

Kept native and isolated by the selected adapter:

- environment setup and teardown (workspace, MCP services, or Docker);
- full task construction and tool instructions;
- artifact collection and final-output contract;
- the native evaluator and native score.

The family selector receives the adapter's neutral task view and the current
family catalog. The neutral view removes adapter-authored collaboration priors;
route metadata such as source benchmark name, adapter name, evaluator, source
index, immutable task ID, and hidden annotations remains outside the selector
and evolution state. The task facts needed to infer collaboration can still be
present, so this boundary is route-identity privacy rather than content
anonymization.

### Runtime identity privacy

The scheduler assigns every case an opaque runtime ID such as
`case-evolve-003` or `case-test-017`. That ID is the only task identity passed
into `Session`, Chairman/Agent execution, team reflection, handoff reflection,
template evidence, and handoff evidence. The manifest's `mix_task_id`, native
benchmark name, native task ID, and source index remain in the outer result
envelope and cross-suite ledger for audit and per-benchmark aggregation; they
are never used as runtime or evolution task IDs. Controller-only progress logs
and `--dry-run` output may still show routing fields for operator diagnostics,
but those fields are not injected into prompts or persistent shared evolution
state.

## Policy injection

Benchmark-specific behavior is injected at runtime rather than stored in the
shared pool:

1. Each manifest binding locks an `execution_policy` name and
   `execution_policy_version`, together with the native output contract and
   allowed tool set.
2. The native adapter owns the canonical `ExecutionPolicy` and binds it after
   environment setup, adding the actual execution mode, available tools,
   workspace paths, runtime instructions, and fallback state.
3. `Runner` injects the bound Chairman rules into the one shared Chairman and
   injects role-specific rules only into recruited Agents for the current
   case. Explicit benchmark, adapter, policy, and output-contract names remain
   private routing metadata.
4. The adapter constructs the native task, filters the disposable case pool's
   tools, enforces the per-task AnswerAgent contract, collects artifacts, and
   delegates scoring to the native evaluator.

This gives every task four separate inputs: a neutral task view for choosing a
team family, the full execution task for the recruited team, a bound execution
policy for environment/tool/special rules, and an output contract for final
submission. Only the first input is visible to the family selector.

Manifest loading rejects policy name/version, tool-set, or output-contract
mismatches between a binding and its adapter. This prevents an old manifest
from silently running under changed benchmark semantics.

LOCA's declared fallback is an example of the same mechanism. A fatal MCP
setup/session failure may bind `local_db_fallback` only when every required
local path exists. Such a run is retained for diagnosis but is marked
`official_score_eligible=false` and `evolution_eligible=false`; it is excluded
from official aggregation, reflection, and shared version persistence. Normal
task or parameter errors do not trigger fallback.

## Files

- `mix_coop_manifest.py`: typed manifest model and semantic validation;
- `task_wrapper.py`: lazy native-adapter routing and prepare/evaluate boundary;
- `mixed_scheduler.py`: sequential round-robin scheduler with one RunManager,
  shared evolution lineage, and cross-suite result ledger;
- `build_gaia_locobench_manifest.py`: materializes the 10+10 evolve / 40+40
  test GAIA–LoCoBench split;
- `make_gaia_locobench_smoke.py`: derives the 2+2 evolve / 4+4 test protocol
  smoke split from the locked pilot;
- `randomize_manifest.py`: materializes a seed-specific stratified-random
  order, normally shuffling evolve tasks while keeping test order fixed;
- `gaia_locobench_pilot_lock_v1.json`: frozen model, split, ordering, and
  metric configuration;
- `manifest.schema.json`: machine-readable JSON Schema;
- `manifests/mix_coop_smoke_v1.json`: locked 4-way smoke manifest;
- `manifests/mix_coop_gaia_locobench_v1.json`: locked 100-task pilot manifest;
- `validate_manifest.py`: structural and native-reference checker.

## Native asset migration

The previously provisioned assets are now exposed under `native/` without
duplicating the large datasets or LoCoBench repository:

- `native/gaia` → the existing project GAIA corpus (`data/gaia`), including
  `train_20`, `test_100`, and attachment files;
- `native/locobench` → the existing `benchmarks/LoCoBench` checkout, including
  scenario data, generated context, and native validation code.

The GAIA and LoCoBench adapters resolve these MIX-COOP native paths first and
fall back to their original locations for standalone runs. This makes the
migration explicit while keeping one source of truth for the data and avoids
creating a second, divergent 1 GB LoCoBench copy.

Validate the manifest without starting environments or model calls:

```bash
.venv311/bin/python benchmarks/MIX-COOP/validate_manifest.py \
  benchmarks/MIX-COOP/manifests/mix_coop_smoke_v1.json \
  --resolve-native
```

`--resolve-native` loads each native dataset and verifies that both the source
index and immutable task ID still match. It does not create Docker/MCP
environments or execute tasks.

The GAIA–LoCoBench pilot is materialized with:

```bash
.venv311/bin/python benchmarks/MIX-COOP/build_gaia_locobench_manifest.py
.venv311/bin/python benchmarks/MIX-COOP/validate_manifest.py \
  benchmarks/MIX-COOP/manifests/mix_coop_gaia_locobench_v1.json \
  --resolve-native
```

It contains 10 GAIA + 10 LoCoBench evolve tasks and 40 GAIA + 40 LoCoBench
holdout tasks. LoCoBench uses five Feature Implementation and five Cross-file
Refactoring evolve items, with twenty holdout items from each category.

Generate the smaller protocol smoke set with:

```bash
.venv311/bin/python benchmarks/MIX-COOP/make_gaia_locobench_smoke.py
.venv311/bin/python benchmarks/MIX-COOP/validate_manifest.py \
  benchmarks/MIX-COOP/manifests/mix_coop_gaia_locobench_smoke_v1.json \
  --resolve-native
```

For a mixed-order seed, materialize a new manifest before launching any
baseline. Each round contains at most one task from each active benchmark, the
benchmark order within a round is randomized, and each benchmark's own queue
is independently shuffled:

```bash
.venv311/bin/python benchmarks/MIX-COOP/randomize_manifest.py \
  --input benchmarks/MIX-COOP/manifests/mix_coop_smoke_v1.json \
  --output benchmarks/MIX-COOP/manifests/mix_coop_smoke_v1_seed20260822.json \
  --seed 20260822
```

The materialized `order_hash` and full task sequence are stored in the output
manifest. Reuse that exact manifest for Meta-Team and every baseline in the
same seed. Use separate output files and independent `v000` lineages for other
seeds; do not resume one seed from another.

The scheduler's dry run is also side-effect free:

```bash
.venv311/bin/python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_smoke_v1.json \
  --phase all --dry-run
```

An actual run requires a configured API and the common pool. Run `--phase
evolve`, then `--phase test --resume` with the same `--run-id` so the frozen
latest version is reused; `--phase all` performs both phases in one RunManager
lineage. Use `--resume` with the same run ID after a recoverable infrastructure
interruption.

Configure the shared model endpoint before launching a run. The API files are
kept under `apiconfig/mix-coop/` for convenient, benchmark-specific inspection:

```bash
export META_TEAM_ENV_FILE=apiconfig/mix-coop/gaia.env
export META_TEAM_MODEL=gpt-5.6-luna
```

`locobench.env` contains the equivalent LoCoBench endpoint configuration. The
current scheduler uses one environment file per process; because both pilot
files point to the same model gateway, either file can be selected for the
mixed run. Keep the files local and do not commit their credentials.

## Important shared-pool requirement

The four current benchmark pools use different Agent IDs. A template containing
`web_agent` cannot be loaded by a pool that only knows `repo_analyst`, and vice
versa. Therefore MIX-COOP declares one common pool, `pool_MIX_COOP`, as the only
valid shared evolution namespace. That pool must be created before an executable
mixed run is added. It should contain stable cross-benchmark role IDs and the
union of runtime-gated tool capabilities. Native adapters still decide whether
GAIA attachments, LOCA MCP services, or BeyondSWE containers exist for a task.

The common pool exposes the union of tool declarations, but the scheduler
passes each binding's `native_allowed_tools` set to the base adapter. The
adapter filters every Agent's tool list in the disposable case copy before
loading the Runner. Shared prompts/templates persist in the RunManager
lineage, while tool availability remains native-case scoped.

The shared pool must not define `settings.answer_protocol`. Each native adapter
is the sole runtime source of its `OutputContract`; MIX-COOP injects that
contract's submission type, AnswerAgent instruction, and required response
prefix into the Chairman and global AnswerAgent for every task. The manifest
keeps an auditable declaration of the contract, and validation rejects a
binding whose declared contract does not match the adapter's canonical one.

The initial GAIA–LoCoBench pool uses five reusable candidate roles:
`researcher`, `context_analyst`, `implementer`, `verifier`, and `integrator`.
The Chairman and `answer_agent` are global services and are excluded from
family templates. Typical activation patterns are researcher + verifier +
integrator for GAIA, and context_analyst + implementer + verifier + integrator
for LoCoBench; the template layer may still select a smaller subset per task.

Using four existing pools sequentially would share filenames, but not genuine
Agent/template evolution, and is intentionally excluded by the manifest
contract.

## Execution lifecycle

For each `evolve` task in manifest order:

1. resolve the native item by `split + adapter_args + source_index + task_id`;
2. call the native adapter's `setup_environment`, bind its locked execution
   policy, and build the native task;
3. select a family from normalized evidence using the shared
   `pool_MIX_COOP` state;
4. inject current-case Chairman/Agent rules and execute with the task's native
   output contract;
5. call the native evaluator and save its unmodified score;
6. if the trajectory is evolution-eligible, apply Agent, handoff, and team
   reflection to the same team workspace;
7. advance to the next manifest task only after a usable evaluation result.

For `test`, freeze the final evolution snapshot and run without reflection.
Every record should retain both MIX-COOP routing fields and the full native
record. Cross-suite aggregation is a separate step; native scores are not
directly averaged by this wrapper.
