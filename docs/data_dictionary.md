# Data Dictionary

## snapshot fields
- `as_of_utc`: ISO8601 timestamp
- `asset`: symbol/name
- `market.price_usd`: spot price
- `market.volume_24h_usd`: 24h volume
- `market.liquidity_usd`: aggregate liquidity proxy
- `onchain.top10_holder_pct`: concentration ratio (top-10 holders / total supply)
- `onchain.top10_holder_source`: data source id for concentration metric
- `onchain.dex_depth_2pct_usd`: depth within ±2%
- `onchain.exchange_inflow_usd_24h`: exchange inflow
- `onchain.exchange_outflow_usd_24h`: exchange outflow
- `narrative.news_count_24h`: count of relevant articles
- `narrative.social_velocity_score`: normalized social momentum
