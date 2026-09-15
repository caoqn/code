# Benchmark Integration

本目录集成 GAIA、LoCoBench、LOCA-Bench 和 BeyondSWE。`adapter.py` 定义共同生命周期，四个 `adapter_*.py` 保留各自的任务构造、环境、工具范围、输出契约和原生 evaluator。

数据集不随仓库分发。请先阅读根目录 `data/README.md` 和各上游 benchmark README。`MIX-COOP/` 只固定混合划分、顺序和共享演化边界，不复制数据，也不把四种原生分数改造成新的 evaluator。

