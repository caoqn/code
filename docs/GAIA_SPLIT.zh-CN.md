# GAIA 训练集与测试集的具体文件

GAIA adapter 在 `benchmarks/adapter_gaia.py` 中按 Level `1 → 2 → 3` 拼接文件。因此“全局 index”是拼接后的 index，不是文件内独立编号。

## 训练集：`train_20`

| 文件 | Level | 题数 | 拼接后的全局 index |
|---|---:|---:|---:|
| `data/gaia/level_1_train_20.json` | 1 | 6 | 0–5 |
| `data/gaia/level_2_train_20.json` | 2 | 9 | 6–14 |
| `data/gaia/level_3_train_20.json` | 3 | 5 | 15–19 |
| **合计** |  | **20** | **0–19** |

训练命令固定使用：

```bash
python benchmarks/adapter_gaia.py \
  --split train_20 --team pool_GAIA_pool --evolve
```

## 测试集：`test_100`

| 文件 | Level | 题数 | 拼接后的全局 index |
|---|---:|---:|---:|
| `data/gaia/level_1_test_100.json` | 1 | 38 | 0–37 |
| `data/gaia/level_2_test_100.json` | 2 | 49 | 38–86 |
| `data/gaia/level_3_test_100.json` | 3 | 13 | 87–99 |
| **合计** |  | **100** | **0–99** |

测试命令固定使用冻结团队且不带 `--evolve`：

```bash
python benchmarks/adapter_gaia.py \
  --split test_100 --team pool_GAIA_81pct_20260902
```

## 与 MIX-COOP 的对应关系

主清单 `benchmarks/MIX-COOP/manifests/mix_coop_official_116_seed20260828.json` 中：

- GAIA `evolve`：引用 `train_20` 的 20 个样本，source index 覆盖 0–19；
- GAIA `test` smoke：引用 `test_100` 的 2 个样本，source index 为 0 和 1（均来自 Level 1 文件）；
- 这 2 个 smoke case 只用于协议连通性检查，不是完整 GAIA 测试；完整测试仍是 `test_100` 的 100 题。

## 数据文件与发布包的关系

上述 JSON 和 `val_files/` 属于原始数据，未复制到 GitHub 发布目录。将数据放回 `data/gaia/` 后，使用 `validate_manifest.py --resolve-native` 或 `scripts/preflight_gaia.py` 检查文件、题数和 immutable task ID。

