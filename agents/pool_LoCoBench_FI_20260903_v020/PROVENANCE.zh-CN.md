# 冻结团队来源：LoCoBench Feature Implementation

此目录是只读复现快照。

- 来源初始池：`agents/pool_LoCoBench`
- 演化 run：`runs/20260903_locobench_fi_final_train_evolve`
- 类别：Python `feature_implementation`
- 演化数据：index 0–19，20 题
- 冻结版本：`v020`
- 冻结时间：2026-09-03 11:19:25 UTC
- 原冻结名：`agents/pool_LoCoBench_fi_final_20260903`
- 训练平均分：0.6734
- 冻结测试数据：index 20–99，80 题，与训练 index 分离
- 快照统计：2 个 family、29 条 handoff rule

测试阶段曾受到上游 API 问题影响，不能使用最初污染的整轮 summary 作为最终成绩。清理后的覆盖方式为：

- `20260903_locobench_fi_final_test_rerun1` 中的 index 20–62；
- `20260904_locobench_fi_final_test_rerun2_63_99` 中的 index 63–99。

两段合并覆盖 index 20–99 共 80 题，没有缺失 index，也没有标记的基础设施失败；合并平均 score 为 0.66322125。

发布目录没有复制数据正文或大体积结果日志。请勿原地修改或继续训练；派生实验应复制为新的 pool 名。

