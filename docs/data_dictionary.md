# Data Dictionary

## snapshot fields
- `as_of_utc`: ISO8601 timestamp
- `asset`: symbol/name
- `market.price_usd`: spot price
- `market.volume_24h_usd`: 24h volume
- `market.liquidity_usd`: aggregate liquidity proxy
- `onchain.top10_holder_pct`: concentration ratio (top-10 holders / total supply)
- `onchain.top10_holder_source`: data source id for concentration metric (`moralis`/`solscan`/`birdeye`/`solana-rpc`/`heuristic-proxy`)
- If holder endpoints are unavailable, system uses a transparent heuristic proxy model:
  - `top10_holder_pct_proxy = 100 - ((liquidity_usd / fdv_usd) * 100 * 1.5)`
  - with floor `55.0%` and cap `99.0%`
  - and emits risk flag `using_heuristic_proxy`
- `onchain.dex_depth_2pct_usd`: depth within ±2%
- `onchain.exchange_inflow_usd_24h`: exchange inflow
- `onchain.exchange_outflow_usd_24h`: exchange outflow
- `narrative.news_count_24h`: count of relevant articles
- `narrative.social_velocity_score`: normalized social momentum
