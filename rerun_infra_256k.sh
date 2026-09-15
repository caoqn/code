#!/bin/zsh
set -a
source "/Users/caoqinuo/Desktop/6月课题/meta_team evolution/new code/apiconfig/gaia.env"
set +a
export META_TEAM_ENV_FILE="/Users/caoqinuo/Desktop/6月课题/meta_team evolution/new code/apiconfig/gaia.env"
export LOCA_STRICT_PREPROCESS=1
py="/Users/caoqinuo/Desktop/6月课题/meta_team evolution/new code/.venv-loca/bin/python"
for spec in \
  "ApplyPhDEmail:42" "ApplyPhDEmail:123" "ApplyPhDEmail:456" "ApplyPhDEmail:789" "ApplyPhDEmail:2024" \
  "FilterLowSelling:42" "FilterLowSelling:123" "FilterLowSelling:456" "FilterLowSelling:789" "FilterLowSelling:2024" \
  "WoocommerceStockAlert:42" "WoocommerceStockAlert:123" "WoocommerceStockAlert:456" "WoocommerceStockAlert:789" "WoocommerceStockAlert:2024" \
  "WoocommerceNewWelcome:789" "WoocommerceNewWelcome:2024"; do
  task=${spec%%:*}
  seed=${spec##*:}
  run_id="20260914_loca_v116_original256k_gaia_rerun_${task}_seed${seed}"
  "$py" benchmarks/adapter_locabench.py --split 256k --task "$task" --seed "$seed" \
    --team pool_MIX_COOP_official116_seed20260828_v116_frozen --max-cost 100 \
    --timeout 7200 --effective-timeout 7200 --workers 1 \
    --api-case-retries 3 --api-case-retry-wait 90 --run-id "$run_id" \
    >> "logs_${run_id}.log" 2>&1 || exit $?
done
