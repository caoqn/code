# Meta-Team Evolution：可复用实验代码

本目录是从 `new code` 当前实现中整理出的 GitHub 发布版，保留多智能体执行、团队选择、分层反思、family/template 演化、handoff rule 演化、四个原生 benchmark 适配器和 MIX-COOP 调度逻辑。

为避免泄露和仓库膨胀，本目录不包含 API 密钥、原始数据集、运行日志、容器镜像、虚拟环境或历史 `runs/`。数据应按 [数据准备说明](data/README.md) 在本地补齐。

## 项目目标

系统从一个 benchmark 对应的初始 Agent Pool 出发，由 Chairman 针对任务选择或冷启动一个 team family，并从 family 允许的成员中招募实际执行者。任务完成和原生评测结束后，系统把可复用经验写入版本化团队：

- L1：各实际参与 Agent 反思自己的 prompt patch 与 skills；
- L2：可选的 teammate profile 观察；当前 GAIA 与 MIX 池采用 Chairman-only profile；
- Team reflection：创建、细化、保留或退役 family/template；
- Handoff reflection：按实际 Agent 交互逐条判断是否创建、细化、保留、退役或不更新规则；
- RunManager：每个有效训练样本形成新版本，测试阶段使用冻结快照只读评测。

handoff rule 是 family 级协作记忆。运行时只把当前 family 中、`from_agent` 等于接收者自身的出站规则作为软提示注入；发送方在正式交接时自行选择规则 ID，使用情况写入 handoff trace，供后续反思。正常任务失败仍可提供失败证据，已确认的基础设施失败不参与演化。

## 目录结构

```text
.
├── main.py                         # 通用单任务入口、历史、trace 与 audit
├── core/                           # Agent 运行时、选择器、反思器、注册表和版本管理
├── tools/                          # 消息、文件、Web、Docker、LOCA MCP 等工具
├── prompts/reflection/             # L1/L2 反思公共提示词
├── evaluation/                     # 评估接口与研究型 rubric
├── benchmarks/
│   ├── adapter.py                  # 四个 benchmark 共用生命周期
│   ├── adapter_{gaia,locobench,locabench,beyondswe}.py
│   ├── MIX-COOP/                   # 混合清单、校验、路由与顺序调度
│   ├── LoCoBench/                  # 轻量运行/评估代码；不含数据
│   ├── LOCA-bench/                 # 运行代码；不含 task-configs/assets
│   └── BeyondSWE/                  # 上游说明；不含 JSONL/测试套件
├── agents/
│   ├── pool_GAIA_pool              # 四个 benchmark 冷启动池之一
│   ├── pool_LoCoBench
│   ├── pool_LOCAbench
│   ├── pool_BeyondSWE
│   ├── pool_MIX_COOP               # MIX-COOP 冷启动公共角色命名空间
│   ├── pool_GAIA_81pct_20260902    # 标注后的 GAIA 81% 冻结团队
│   └── pool_LoCoBench_FI_20260903_v020 # 标注后的 FI v020 冻结团队
├── scripts/                         # 四 benchmark 实验与冻结脚本
├── tests/                           # 核心契约和适配器回归测试
├── data/README.md                   # 本地数据放置位置
└── docs/                            # 架构、文件、实验和团队说明
```

详细说明：

- [代码架构](docs/ARCHITECTURE.zh-CN.md)
- [文件与目录说明](docs/FILE_GUIDE.zh-CN.md)
- [实验设置、四 benchmark 与 MIX-COOP 划分](docs/EXPERIMENTS_AND_SPLITS.zh-CN.md)
- [GAIA 训练/测试具体文件清单](docs/GAIA_SPLIT.zh-CN.md)
- [四个初始池、MIX 池与冻结团队](docs/POOLS_AND_FROZEN_TEAMS.zh-CN.md)

## 快速开始

建议使用 Python 3.11；项目声明的最低版本为 Python 3.10。

```bash
python3.11 -m venv .venv311
source .venv311/bin/activate
pip install -e .
cp .env.example .env
```

在 `.env` 中填写兼容 OpenAI 或 Anthropic 的私有 API 配置，不要提交该文件。也可以把私有配置放在仓库外，并为单个进程指定：

```bash
export META_TEAM_ENV_FILE=/absolute/private/path/gaia.env
export META_TEAM_MODEL=gpt-5.6-luna
```

先进行不调用模型的基本检查：

```bash
python scripts/check_release.py

python benchmarks/MIX-COOP/validate_manifest.py \
  benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json

python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase all --dry-run
```

数据就绪后，单 benchmark 的典型训练—冻结—测试流程为：

```bash
# GAIA：20 题顺序演化
bash scripts/run_gaia_evolve_and_test.sh evolve

# 将指定 run 的最新团队冻结为新的只读测试池
bash scripts/freeze_evolved_team.sh RUN_ID latest NEW_POOL_NAME

# 使用冻结团队测试 100 道 holdout
bash scripts/run_gaia_evolve_and_test.sh test NEW_POOL_NAME
```

LoCoBench、LOCA-Bench 与 BeyondSWE 的完整命令见实验文档及各 `run_*_paper_experiment.sh` 的帮助信息。

## MIX-COOP

正式清单为：

```text
benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json
```

其中有 116 个 `evolve` 样本，使用随机种子 `20260828` 做一次物化的全局洗牌；同一个 `pool_MIX_COOP` 按清单顺序串行演化。清单还附带 8 个 `test` smoke 样本，因此 JSON 中任务总数是 124，而“116”专指训练/演化集大小。

五个初始池通过“不提供 `templates.json` / `handoff_rules.json`”表达真正冷启动；registry 首次加载时会把缺失文件解释为空状态，并在产生第一条 family/rule 后写出文件。冻结团队则显式包含这两个演化 artifact。

```bash
python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase evolve --team pool_MIX_COOP --run-id MIX_RUN_ID

python benchmarks/MIX-COOP/mixed_scheduler.py \
  --manifest benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json \
  --phase test --team pool_MIX_COOP --run-id MIX_RUN_ID --resume
```

训练阶段必须串行，因为第 `n+1` 个样本需要读取第 `n` 个样本产生的新团队版本；冻结后的测试可在 benchmark 自己的适配器入口按需并行。

## 已附冻结团队

- `pool_GAIA_81pct_20260902`：由 `train_20` 的 20 个样本演化到 v020；随后在独立 `test_100` 上获得 `81/100`，无已记录基础设施失败。详见团队目录内的 `PROVENANCE.zh-CN.md`。
- `pool_LoCoBench_FI_20260903_v020`：Feature Implementation 的 Python 样本 0–19 顺序演化所得 v020；测试使用 20–99。详见团队目录内的 `PROVENANCE.zh-CN.md`。

这些目录是结果快照。复现实验时应复制为新的池名再训练，不要原地修改。

## 发布前约束

- 不要提交 `.env`、`apiconfig/`、任何真实密钥或代理地址凭据。
- 不要提交 `data/`、benchmark 大型数据目录、`runs/`、结果目录、sessions 或虚拟环境。
- 上游 benchmark 代码保留其原许可证文件；发布前仍需确认整个仓库采用的顶层许可证与所有第三方数据/代码条款兼容。
- 清单保存的是划分与任务引用，不含任务正文；它用于固定实验顺序，不能替代原始数据。
