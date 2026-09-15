# Archived experimental-variant tests

这三个测试来自早期的 `team_selector_test.py` / `team_reflector_test.py` 对照实现。当前 `new code` 已不再保留那两个实现文件，因此它们不参与默认 pytest 收集，只作为实验设计记录保留：

- `archived_gaia_experimental_entrypoint.py`
- `archived_team_reflector_description_variants.py`
- `archived_team_selector_variants.py`

默认回归测试覆盖当前正式的 `core/team_selector.py` 与 `core/team_reflector.py`。若将来恢复对照实现，应先补回明确命名的 variant 模块，再把这些测试移回 `tests/`。
