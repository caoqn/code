# 代码架构与运行机制

## 1. 总体数据流

```text
原生数据集
   │
   ▼
Benchmark Adapter ──准备原生环境、构造任务、限制工具、定义输出契约
   │
   ▼
Team Selector ──复用 family 或冷启动；得到冻结的可招募成员集合
   │
   ▼
Runner + Chairman ──Chairman 招募实际成员、消息交接、AnswerAgent 收口
   │
   ├── Session/EventLog：完整执行与 handoff trace
   └── 原生 evaluator：返回 success/score/基础设施状态
   │
   ▼（仅 evolve 且样本允许演化）
L1 / 可选 L2 / Team Reflector / Handoff Reflector
   │
   ▼
RunManager：v000 → v001 → … → vNN；冻结后只读测试
```

MIX-COOP 不创建第五套 evaluator。它只读取固定清单，把每个样本路由回 GAIA、LoCoBench、LOCA-Bench 或 BeyondSWE 的原生适配器，同时让四类任务共享同一个团队版本谱系。

## 2. 任务选择与执行边界

`TemplateRegistry` 保存多个 family，每个 family 有稳定 ID、描述、当前 template 版本、可招募成员集合和证据历史。

`LLMTeamSelector` 先比较完整任务的协作需求与 family catalog：

- `reuse`：直接使用已有 family 的当前成员集合；
- `cold_start`：在公共 Agent catalog 上组合临时成员集合，任务结束后再由 Team Reflector 形成可复用 family；
- 选择器输出无效时：进入有记录的 cold-start fallback，保证任务仍可执行。

一旦选择完成，`allowed_agent_ids` 在本任务中被冻结。Chairman 只能从该集合招募成员；`answer_agent` 是全局收口服务，不属于 family 成员。

## 3. Chairman、成员与 profile

配置支持三种 profile 模式：

- 全关闭：Chairman 与成员都不读取/反思 teammate profile；
- 旧式对称模式：`teammate_profiles_enabled: true`，所有参与者可进入 L2；
- Chairman-only：`chairman_teammate_profiles_enabled: true` 且 `member_teammate_profiles_enabled: false`。

GAIA 与 MIX 初始池采用 Chairman-only。Chairman 只读取所选 family 内成员的既有观察，并且只为本题实际招募的成员写入新观察。执行成员不读取或反思 profile，而依赖自身 prompt/skill 和自己的出站 handoff rules。profile 的语义是“历史上已观察到的行为”，不是招募优先级指令。

LoCoBench 初始池和所附 FI 冻结团队仍保留旧式 `teammate_profiles_enabled: true`，这是冻结结果的一部分，不应在复现该结果时静默改写。

## 4. Handoff rule 的生成与使用

`HandoffRegistry` 把 team family 映射到 handoff family，并保存带稳定 `rule_id` 的规则。规则包含发送方、接收方、适用描述、交接要求、状态、证据和版本历史。

执行时：

1. Adapter 读取当前 family 的 active rules；
2. Runner 对每个 Agent 只展示 `from_agent == 自身` 的规则；
3. 发送方调用 `send_message` 时选择 `handoff_rule_id`，没有适用规则时使用 `NONE`；
4. 工具校验规则 ID、发送方与接收方是否一致；
5. 消息、所用规则 ID 和方向进入 `handoff_trace` / `handoff_rule_usage`。

反思时，Adapter 从完整执行轨迹筛出参与者之间的每个真实交互，并按“一条交互一个 evidence batch”调用一次 Handoff Reflector。因此 `n` 条交互最多给出 `n` 个 handoff 决策，但每个决策仍可以是 `no_update`。Reflector 能看到当前 family 规则、该交互、任务结果以及相应的使用 trace，可输出 `create`、`refine`、`retain`、`retire` 或 `no_update`。

正常评测失败仍允许 handoff 反思并记录紧凑失败证据；确认的 API、容器、MCP 等基础设施失败会跳过这一步，避免污染长期协作记忆。本实现不单设“负向规则”类型，失败经验仍通过普通规则的 refine/retire/no-update 语义处理。

## 5. 分层演化

### L1：个体能力记忆

每个实际参与 Agent 在任务结束后反思自身行为，可更新：

- `evolution/prompt_patches.md`：小范围、可累积的提示词补丁；
- `skills/<skill>/SKILL.md`：可复用任务技能；
- 或显式跳过更新。

超时或消息预算触发的 forced reflection 仍可执行 L1，但会明确标记终止原因，重点总结资源使用问题。

### L2：teammate profile

L2 是可选的角色行为观察层。其写入者由 Runner 的 profile 配置决定：旧式模式为所有参与者，Chairman-only 模式仅 Chairman，关闭时不进入 L2。

### Team reflection：结构记忆

原生 evaluator 完成后，Team Reflector 根据本题实际团队、选择信息与评测结果更新 family/template。它与 L1/L2 以及 handoff reflection 分开执行，不再因另一层选择“不更新”而被绑定阻断。

### 版本持久化

`RunManager` 为演化运行创建 `team/v000`，每个有资格演化的样本完成后持久化到下一版本。测试必须从冻结目录启动，并禁止演化写回。`scripts/freeze_evolved_team.sh` 负责复制指定版本并生成来源标记。

## 6. 原生 benchmark 边界

每个 adapter 负责五件事：

1. 读取并筛选自己的数据；
2. 创建独立 workspace、MCP 服务或 Docker；
3. 构造完整执行任务和可用于 family 选择的任务描述；
4. 注入该 benchmark 允许的工具与输出契约；
5. 调用原生 evaluator，保留原生分数与错误语义。

MIX-COOP 在外层记录真实 benchmark、split、task ID 和原生 index 以便审计；传入 Session 和演化记忆的是 `case-evolve-NNN` / `case-test-NNN` 这样的不透明运行 ID，避免数据集身份直接进入共享长期记忆。

## 7. 可靠性与审计

- `APIReliabilityTracker` 与共享 circuit breaker 区分模型/API 故障和普通任务失败；
- `ResultManifest` 记录每次尝试、有效记录和待重跑基础设施样本；
- `Session` / `EventLog` 保存细粒度事件；
- `trace.py` 提供终端时序视图；
- `audit.py` 生成文本与 HTML 审计报告；
- `SubmissionBridge` 与 `OutputContract` 保证最终交付符合各 benchmark 的原生格式。

