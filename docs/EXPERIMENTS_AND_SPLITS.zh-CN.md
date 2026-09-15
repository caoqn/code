# 实验设置与数据划分

本文固定“哪些样本用于演化、哪些样本只用于测试”。原始题目正文和附件未复制到发布目录。

## 共同实验协议

1. 每个 benchmark 从对应 `agents/pool_*` 的 v000 开始。
2. 演化样本严格串行；每个合格样本在上一版本基础上运行并形成下一版本。
3. 正常任务失败可以触发 team/handoff 反思；确认的基础设施失败不得更新团队版本，应修复上游后重跑。
4. 训练结束后将最终 vNN 复制为独立冻结团队。
5. 测试使用冻结团队、关闭 `--evolve`，不得把测试样本经验写回。
6. 并行只用于相互独立的实验或冻结后的测试 case；单条训练谱系不能并行更新。
7. 报告原生 benchmark 分数，同时单独报告基础设施失败数、有效样本数、模型、温度、超时、rollout、代码版本和团队快照。

## 四个 benchmark 的 standalone 划分

| Benchmark | 演化/训练 | 冻结测试 | 初始池 | 原生输出 |
|---|---:|---:|---|---|
| GAIA | `level_1/2/3_train_20.json`，6+9+5=20 题 | `level_1/2/3_test_100.json`，38+49+13=100 题 | `pool_GAIA_pool` | 严格短答案 |
| LoCoBench FI | Python FI，index `0–19`，20 题 | 同类别 index `20–99`，80 题 | `pool_LoCoBench` | solution 文件 + completion summary |
| LoCoBench CR | Python CR，index `0–19`，20 题 | 同类别 index `20–99`，80 题 | `pool_LoCoBench` | solution 文件 + completion summary |
| LOCA-Bench | `evolve_96k`，8 tasks × seeds `{101,102}` = 16 | 8 tasks × 5 seeds，在每个 context split 上 40 题 | `pool_LOCAbench` | 已验证环境状态 + completion summary |
| BeyondSWE CrossRepo | index `0–19`，20 题 | index `20–199`，180 题 | `pool_BeyondSWE` | repository patch + fix summary |
| BeyondSWE DepMigrate | index `0–19`，20 题 | index `20–177`，158 题 | `pool_BeyondSWE` | repository patch + fix summary |

LoCoBench 的 FI 和 CR 是同一 benchmark 的两个独立实验类别，不能把 FI 的测试集用于 FI 演化，也不应在报告单项结果时把二者混成一个分数。其额外 OOD 评测是 C/C++/Java 各 100 个样本，全部只测试、不演化。

LOCA-Bench 的正式测试上下文为 `8k`、`16k`、`32k`、`64k`、`128k`、`256k`；每档使用以下 8 个 task 与 seeds `{42,123,456,789,2024}`，因此每档 40 题、六档共 240 次：

- `WoocommerceNewWelcome`
- `WoocommerceStockAlert`
- `FilterLowSellingProducts`（脚本筛选别名为 `FilterLowSelling`）
- `ApplyPhDEmail`
- `SetConfCrDdl`
- `CourseAssistant`
- `CanvasArrangeExam`
- `CanvasListTest`

训练 seed `{101,102}` 与测试 seed `{42,123,456,789,2024}` 分离。

## MIX-COOP 正式训练划分

主清单：`benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json`

| 来源 | split/category | evolve 数量 |
|---|---|---:|
| GAIA | `train_20` | 20 |
| LoCoBench | Python / `feature_implementation` | 20 |
| LoCoBench | Python / `cross_file_refactoring` | 20 |
| LOCA-Bench | `evolve_96k` | 16 |
| BeyondSWE | `crossrepo` index 0–19 | 20 |
| BeyondSWE | `depmigrate` index 0–19 | 20 |
| **合计** |  | **116** |

这 116 个引用使用 seed `20260828` 做一次 `global_shuffle`，顺序已经写死在 JSON 中，`order_hash` 为：

```text
a1776e9e06961a3d545c9b628e9b2015acb701779367080bd2d8801e589adc15
```

复现时必须直接使用已物化清单，不能在运行过程中重新 shuffle。不同随机种子应生成独立清单、独立 run ID，并从独立 v000 开始。

## MIX-COOP 附带测试划分

主清单还锁定了 8 个协议 smoke 测试引用：

| 来源 | 测试引用 |
|---|---:|
| GAIA `test_100` | 2 |
| LoCoBench Python FI holdout | 2 |
| LOCA-Bench `128k` | 2 |
| BeyondSWE CrossRepo holdout | 2 |
| **合计** | **8** |

因此文件名中的“116”是演化集大小，不是 JSON 的总 task 数；JSON 实际包含 `116 evolve + 8 test = 124` 个引用。这 8 题适合端到端协议验证，不能替代四个 benchmark 的完整 standalone 测试集。

## MIX-COOP 的共享与隔离

四类 evolve 样本共同更新：

- `templates.json` 与 family/template 历史；
- `handoff_rules.json`；
- Agent prompt patches、skills，以及配置允许时的 profiles；
- `constitution.md` 与 pool 配置。

每题仍由原生 adapter 独立控制：

- task 构造与附件/context；
- workspace、MCP 服务或 Docker；
- 工具白名单；
- AnswerAgent 输出契约；
- 原生 evaluator 和原生 score。

共享 Agent 命名空间只能使用 `pool_MIX_COOP`。四个 standalone pool 的角色 ID 不一致，不能直接轮流指向它们来冒充共享演化。

## 关键默认设置

| Pool | Chairman | 时间/消息上限 | Team selector | Profile 模式 |
|---|---|---|---|---|
| GAIA | `plan_agent` | effective 900s；wall 3000s；300 messages | 开 | Chairman-only |
| LoCoBench | `planner` | 1200s；400 messages | 开 | 旧式全员 profile |
| LOCA-Bench | `planner` | 7200s；500 messages；reflection 900s | 开 | 默认关闭 |
| BeyondSWE | `planner` | 1800s；600 messages；reflection 600s | 开 | 关闭 |
| MIX-COOP | `planner` | effective 1200s；wall 3000s；500 messages；reflection 600s | 开 | Chairman-only |

Agent 级模型、温度、max tokens、工具和 max steps 以各 pool 中的 `config.yaml` 为准。为了公平比较，模型、API gateway、温度、rollout、超时和代码 commit 应在所有对照组固定并写入实验报告。

## 推荐运行顺序

```bash
# 1. 只检查清单结构和顺序
python benchmarks/MIX-COOP/validate_manifest.py \
  benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json
python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase evolve --dry-run

# 2. 正式串行演化
python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase evolve --team pool_MIX_COOP --run-id YOUR_RUN_ID

# 3. 中断恢复：相同清单、team、run-id
python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase evolve --team pool_MIX_COOP --run-id YOUR_RUN_ID --resume

# 4. 完成后用同一 run 的最新冻结版本做清单 smoke test
python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase test --team pool_MIX_COOP --run-id YOUR_RUN_ID --resume
```

正式发布结果前还应在四个 benchmark 的完整 holdout 上分别评测，而不是只报告 MIX 清单内 8 个 smoke case。
