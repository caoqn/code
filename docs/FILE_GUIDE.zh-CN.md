# 文件与目录说明

本页说明研究代码的主要文件。第三方 benchmark 内部文件按子目录说明；它们自身的 README 和许可证仍是权威来源。

## 根目录

- `main.py`：通用 Meta-Team 单任务入口，解析 `--team`、`--template`、`--evolve`、`--model`，并提供 history、replay、trace、audit。
- `pyproject.toml`：Python 包元数据和运行依赖的单一权威来源。
- `requirements.txt`：便于传统 pip 工作流安装的依赖镜像。
- `pytest.ini`：测试发现和 pytest 配置。
- `.env.example`：无真实凭据的环境变量模板。
- `.gitignore`：排除密钥、数据、运行产物、缓存与虚拟环境。

## `core/`

- `agent.py`：加载 Agent 的 config、prompt、patch、profile、skill，并执行模型/工具循环。
- `runner.py`：一题内的协作运行时；控制成员边界、招募、启动/停止、profile 可见性、handoff rule 注入、预算和结果元数据。
- `reflection_runner.py`：Runner 的 L1/L2 状态机、forced reflection、完成推进和反思工具处理。
- `team_selector.py`：family 复用判定、cold-start 组合、fallback 和结构校验。
- `team_reflector.py`：任务后 family/template 的 create/refine/retain/retire 决策。
- `handoff_reflector.py`：基于交互证据生成一条 handoff 决策。
- `template_registry.py`：加载、查询、更新和保存 family/template catalog。
- `handoff_registry.py`：family 绑定、规则生命周期、失败证据与版本历史的持久化。
- `evolution_models.py`：TeamTemplate、TemplateFamily、TeamSelection、SkillDecision、HandoffRule、HandoffDecision、TeamReflectionDecision 数据模型与验证。
- `reflection_persistence.py`：把 disposable runtime team 中允许的反思结果持久化到下一版本，并按 profile writer scope 过滤。
- `reflection_validator.py`：校验 prompt patch 与 skill 变更，限制无效或越界更新。
- `run_manager.py`：run 目录、case 目录、团队 vNN 版本和 summary 管理。
- `session.py`：会话目录、workspace、事件日志和生命周期。
- `message_store.py`：Agent 间消息队列、终止状态和通信关系。
- `execution_policy.py`：benchmark 原生执行策略、工具范围、fallback 与计分资格。
- `output_contract.py`：GAIA 短答案、LoCoBench solution summary、LOCA completion、BeyondSWE patch summary 等最终输出约束。
- `submission_bridge.py`：把 Chairman 的任务结果交给全局 AnswerAgent 按原生契约收口。
- `result_manifest.py`：记录每次 case attempt，聚合有效结果并标出基础设施待重跑项。
- `api_resilience.py`：识别 API/基础设施故障并记录可靠性事件。
- `api_circuit_breaker.py`：跨 case 的连续 API 故障熔断与冷却。
- `llm.py`：LiteLLM/Anthropic 调用、模型映射、重试、响应与 tool-call 解析。
- `tool_registry.py`：注册工具、发现 Agent skills、读取 skill 元数据与正文。
- `family_policy.py`：family/template 相关共享策略常量。
- `audit.py`：从事件日志生成审计摘要和 HTML 报告。
- `trace.py`：终端中的任务时序、消息流、治理和输出视图。
- `cost_tracker.py`：Agent token/费用统计 mixin。
- `sandbox.py`：把文件访问限制到当前任务 workspace。
- `types.py`：共享的轻量类型，如任务验证结果。
- `utils.py`：时间、截断、prompt 加载、session 数据读取和费用估计。
- `__init__.py`：包标记。

## `tools/`

- `messaging.py`：`send_message`、收件箱和消息等待；校验并记录 handoff rule ID。
- `reflection.py`：L1/L2 反思阶段可调用的 patch、skill、profile 和 skip 工具。
- `read_file.py` / `write_file.py`：workspace 内文件读取和写入。
- `bash.py`：本地隔离 workspace 命令执行。
- `docker_bash.py`：BeyondSWE 容器内命令执行。
- `docker_str_replace_editor.py`：容器内结构化文本替换编辑。
- `loca_mcp.py`：LOCA 任务动态 MCP 服务调用桥。
- `web_search.py` / `web_fetch.py`：GAIA 等任务使用的检索工具。
- `primitives.py`：工具实现共用的基础函数。
- `__init__.py`：工具包导出。

## `prompts/` 与 `evaluation/`

- `prompts/bootstrap_skills.md`：无现成 skill 时的基础能力提示。
- `prompts/reflection/overview.md`：反思阶段共同上下文说明。
- `prompts/reflection/l1_agent.md`：正常 L1 个体反思要求。
- `prompts/reflection/l1_forced.md`：超时/预算终止后的强制 L1 要求。
- `prompts/reflection/l2_communication.md`：旧式 L2 teammate profile 反思要求。
- `evaluation/base.py`：评估器通用接口。
- `evaluation/researchrubrics.py`：研究型任务 rubric 实现。

## `benchmarks/`

- `adapter.py`：共用 case 生命周期。负责临时团队、选择器、Runner、原生评分、L1/L2 后的 team/handoff reflection、版本保存和结果记录。
- `adapter_gaia.py`：GAIA 数据加载、附件复制、检索工具、短答案提取与 exact-match 评估。
- `adapter_locobench.py`：LoCoBench 场景加载、context/solution workspace、代码文件收集和 LCBS 原生指标。
- `adapter_locabench.py`：LOCA task-config 加载、MCP/local_db 环境、完成协议、原生 state evaluator 和受限 fallback。
- `adapter_beyondswe.py`：BeyondSWE JSONL、Docker case、patch 提取/应用、测试与 JUnit/pytest 解析。
- `LoCoBench/locobench/`：上游 LoCoBench 的分析、场景、指标和 evaluator 代码；数据目录被排除。
- `LOCA-bench/gem/`、`mcp_convert/`、`inference/`、`loca/`：LOCA 运行环境、MCP 服务代码和辅助工具；大型 assets、task-configs、运行数据库被排除。
- `BeyondSWE/README.md`：上游 benchmark 说明；数据 JSONL、测试套件和镜像不进入本仓库。

## `benchmarks/MIX-COOP/`

- `mix_coop_manifest.py`：typed manifest、字段解析、语义与隔离策略校验。
- `manifest.schema.json`：JSON Schema。
- `task_wrapper.py`：把 manifest 引用解析为原生 adapter/item，检查 immutable task ID，保持原生构造与评分边界。
- `mixed_scheduler.py`：按物化顺序运行一个共享团队版本谱系，支持 evolve/test/all、resume、dry-run。
- `randomize_manifest.py`：用固定 seed 物化随机顺序并写入 order hash。
- `validate_manifest.py`：结构校验；可在本地数据存在时解析原生引用。
- `build_four_way_full_manifest.py`：生成四 benchmark 正式组合清单。
- `build_gaia_locobench_manifest.py`：生成早期 GAIA–LoCoBench pilot。
- `make_four_way_evolve_smoke.py` / `make_gaia_locobench_smoke.py`：从大清单派生 smoke 清单。
- `manifests/mix_coop_official_116_seed20260828.json`：116 个演化样本和 8 个测试 smoke 样本的主清单。
- `manifests/*`：其他协议验证、消融或 smoke 清单；运行正式实验时应显式使用上面的主清单。

## `agents/`

每个 pool 根目录遵循相同约定：

- `pool.yaml`：Chairman、预算、选择器、profile 与 AnswerAgent 配置；
- `constitution.md`：全队共享约束；
- `templates.json`：family/template registry；冷启动池可省略，缺失等价于空 registry；
- `handoff_rules.json`：family-scoped handoff registry；冷启动池可省略，缺失等价于空 registry；
- `<agent>/config.yaml`：模型、描述、工具和 step 限制；
- `<agent>/prompt.md`：基础角色提示；
- `<agent>/evolution/prompt_patches.md`：L1 累积补丁；
- `<agent>/evolution/teammate_profiles.yaml`：启用 L2 时的已观察行为；
- `<agent>/skills/*/SKILL.md`：L1 产生或更新的可复用技能。

四个 `pool_<benchmark>` 是 v000 初始池；`pool_MIX_COOP` 是混合实验初始池；带日期/成绩的两个目录是冻结团队，不是新的初始池。

## `scripts/` 与 `tests/`

- `run_gaia_evolve_and_test.sh`：GAIA 20-train/100-test 流程。
- `run_locobench_paper_experiment.sh`：FI/CR 各自的 20-train/80-test 与 OOD 流程。
- `run_locabench_paper_experiment.sh`：96K 演化集、六档上下文评测和五 seed 流程。
- `run_beyondswe_paper_experiment.sh`：CrossRepo/DepMigrate 训练、冻结与 holdout。
- `freeze_evolved_team.sh`：把 run 中的 vNN 固化为 `agents/` 下独立团队。
- `preflight_*.py`：数据、依赖和运行环境预检。
- `run_parallel_experiments.sh`：独立 benchmark 进程启动样例；不要用它并行同一条演化谱系。
- `show_result_manifest.py`：展示结果 ledger 的有效/待重跑状态。
- `check_release.py`：离线核对 MIX 数量/seed、初始池冷启动状态、冻结团队统计和明显凭据泄露。
- `tests/`：输出契约、选择器、registry、反思持久化、MIX 隐私、adapter 可靠性等回归测试。`tests/experimental_variants/` 保存三个依赖已移除对照模块的历史测试，不参与默认收集。
