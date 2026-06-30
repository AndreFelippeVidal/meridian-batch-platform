---
title: Meridian — Overview
---

```sql daily_data
select * from daily
```

```sql kpis
select
    sum(gmv)               as total_gmv,
    sum(orders_placed)     as total_orders,
    avg(aov)               as avg_aov,
    sum(units_sold)        as total_units,
    sum(revenue_collected) as total_collected
from daily
```

# Meridian Marketplace — Overview

<BigValue
  data={kpis}
  value="total_gmv"
  title="Total GMV"
  fmt="$#,##0.00"
/>
<BigValue
  data={kpis}
  value="total_orders"
  title="Total Orders"
  fmt="#,##0"
/>
<BigValue
  data={kpis}
  value="avg_aov"
  title="Avg Order Value"
  fmt="$#,##0.00"
/>
<BigValue
  data={kpis}
  value="total_collected"
  title="Revenue Collected"
  fmt="$#,##0.00"
/>

## GMV Over Time

<LineChart
  data={daily_data}
  x="order_date"
  y="gmv"
  title="Daily GMV"
  yFmt="$#,##0"
/>

## Orders & AOV Over Time

<LineChart
  data={daily_data}
  x="order_date"
  y={["orders_placed", "aov"]}
  title="Daily Orders & AOV"
/>
