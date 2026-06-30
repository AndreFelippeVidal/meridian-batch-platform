---
title: Meridian — Data Quality
---

```sql failed_days
select count(*) as days_with_failures
from daily
where gmv < 0
```

```sql payment_buckets
select
    order_date,
    revenue_collected,
    revenue_failed,
    revenue_refunded
from daily
order by order_date
```

```sql gmv_check
select
    order_date,
    orders_placed,
    gmv,
    revenue_collected,
    case when gmv >= 0 then 'OK' else 'FAIL' end as gmv_status
from daily
order by order_date
```

# Data Quality

<BigValue
  data={failed_days}
  value="days_with_failures"
  title="Days with Negative GMV"
/>

## GMV Integrity Check

<DataTable data={gmv_check} rows=15>
  <Column id="order_date"        title="Date" />
  <Column id="orders_placed"     title="Orders" fmt="#,##0" />
  <Column id="gmv"               title="GMV" fmt="$#,##0.00" />
  <Column id="revenue_collected" title="Collected" fmt="$#,##0.00" />
  <Column id="gmv_status"        title="Check" />
</DataTable>

## Revenue Buckets Over Time

<BarChart
  data={payment_buckets}
  x="order_date"
  y={["revenue_collected", "revenue_failed", "revenue_refunded"]}
  title="Daily Revenue by Status"
  yFmt="$#,##0"
/>

---

*Data quality enforced by Elementary + dbt singular test `assert_daily_gmv_non_negative`.
Any negative GMV row fails the pipeline build gate.*
