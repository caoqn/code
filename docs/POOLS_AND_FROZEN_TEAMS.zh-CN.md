# 初始 Pool、MIX Pool 与冻结团队

## 四个 benchmark 初始 Pool

以下初始池都不附带 `templates.json` 或 `handoff_rules.json`：这是代码支持的空 registry 表示，确保首次任务走 cold start。首次产生 family/rule 后，运行版本会自动写出相应 JSON。

### `pool_GAIA_pool`

Chairman：`plan_agent`。

可用成员包括 `web_agent`、`reading_agent`、`file_agent`、`coding_agent`、`science_agent`、`verification_agent`；`answer_agent` 是全局服务。角色覆盖 Web 检索、档案/文档证据、附件处理、可复现计算、科学推理和独立核验。Team selector 开启，profile 为 Chairman-only。

### `pool_LoCoBench`

Chairman：`planner`。

可用成员包括 `reader-1`、`reader-2`、`dependency_architect`、`feature_integrator`、`developer`、`reviewer`、`solution_verifier`；另有全局 `answer_agent`。它面向长上下文代码理解、跨文件依赖、功能实现、代码审查和 solution artifact 检查。当前初始池保留旧式 `teammate_profiles_enabled: true`。

### `pool_LOCAbench`

Chairman：`planner`。

可用成员包括 `context_reader`、`data_analyst`、`cross_system_integrator`、`state_operator`、`artifact_specialist`、`verification_agent`；另有全局 `answer_agent`。角色把“读证据—分析—设计跨系统映射—执行受控状态修改—生成本地 artifact—独立核验”分开，适配多 MCP 服务和 local state 任务。profile 默认关闭。

### `pool_BeyondSWE`

Chairman：`planner`。

可用成员包括 `repo_analyst`、`domain_debugger`、`dependency_specialist`、`developer`、`test_engineer`、`reviewer`、`integration_verifier`；另有全局 `answer_agent`。它面向容器化仓库分析、根因定位、依赖迁移、最小 patch、回归测试和跨模块核验。profile 关闭。

## MIX-COOP 共享初始 Pool

`pool_MIX_COOP` 不是第五个 benchmark pool，而是四种任务共享长期记忆时使用的稳定角色命名空间。

- `planner`：Chairman；识别协作模式并招募最小有效成员集；
- `researcher`：外部权威证据检索；
- `context_analyst`：附件、结构和代码依赖分析；
- `implementer`：创建或修改原生 artifact；
- `verifier`：独立验证来源、计算、测试、artifact 或服务后置状态；
- `integrator`：整合分布式证据并解决跨 artifact 一致性；
- `answer_agent`：按当前原生 adapter 注入的输出契约收口。

共享 pool 的工具配置是能力并集，但每个 case 会被原生 adapter 的 `native_allowed_tools` 再过滤。例如 GAIA 可用 Web 工具，LOCA 可用 `loca_mcp`，BeyondSWE 使用 Docker 工具。`pool.yaml` 故意不写固定 `answer_protocol`，因为每题的原生 adapter 是该协议的唯一来源。

## 冻结团队 A：GAIA 81%

目录：`agents/pool_GAIA_81pct_20260902`

- 初始池：`pool_GAIA_pool`
- 训练 run：`20260902_gaia_chairman_profile_change_r1_evolve`
- 训练划分：GAIA `train_20`，20 题
- 最终版本：v020
- 训练记录：15/20，平均分 0.75
- 冻结测试 run：`20260902_gaia_chairman_profile_change_r1_v020_test`
- 测试划分：GAIA `test_100`，100 题
- 测试结果：81/100，accuracy 0.81
- 测试团队原名：`pool_GAIA_pool_chairman_profile_change_r1_v020_test`
- 快照内容：4 个 family、35 条 handoff rule

该目录已改用更清晰的发布名，内部演化 artifact 未重写。它代表“Chairman profile 语义改动”实验所得冻结团队，不是空白初始池。

## 冻结团队 B：LoCoBench FI

目录：`agents/pool_LoCoBench_FI_20260903_v020`

- 初始池：`pool_LoCoBench`
- 训练 run：`20260903_locobench_fi_final_train_evolve`
- 类别：Python Feature Implementation
- 训练划分：index 0–19，20 题
- 最终版本：v020
- 训练平均分：0.6734
- 原冻结名：`pool_LoCoBench_fi_final_20260903`
- 测试划分：index 20–99，80 题
- 快照内容：2 个 family、29 条 handoff rule

测试期间上游 API 曾发生问题，因此原始整轮结果不应直接作为最终干净分数。已采用第一次重跑的 index 20–62 与第二次重跑的 index 63–99 合并：80 题完整覆盖、没有标记的基础设施失败，合并平均 score 为 0.66322125。此数值用于来源审计，不改变冻结团队内容。

## 使用冻结团队的规则

1. 冻结目录只读，不原地继续 evolve。
2. 新实验先复制成新名称，并记录父快照、代码 commit、模型和数据 split。
3. 测试命令不得带 `--evolve`。
4. 不要仅复制 `templates.json`；prompt patches、skills、profiles、handoff rules、constitution 和 pool config 共同构成团队状态。
5. 比较初始池与冻结池时，应同时报告 family 数、handoff rules、skill/patch 写入量以及 profile 模式，避免只用最终分数解释机制变化。
