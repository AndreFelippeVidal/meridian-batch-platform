---
title: Meridian — Customers
---

```sql by_segment
select
    customer_segment,
    count(*)             as total_customers,
    sum(lifetime_orders) as total_orders,
    avg(lifetime_orders) as avg_orders
from customers
where has_ordered = true
group by customer_segment
order by total_orders desc
```

```sql new_daily
select
    signup_date,
    count(*) as new_customers
from customers
group by signup_date
order by signup_date
```

```sql top25
select
    customer_name,
    customer_segment,
    customer_country,
    lifetime_orders,
    first_order_date,
    last_order_date
from customers
where has_ordered = true
order by lifetime_orders desc
limit 25
```

# Customers

## New Customers Over Time

<LineChart
  data={new_daily}
  x="signup_date"
  y="new_customers"
  title="New Customers per Day"
/>

## Orders by Segment

<BarChart
  data={by_segment}
  x="customer_segment"
  y="total_orders"
  title="Total Orders by Segment"
  yFmt="#,##0"
/>

## Top 25 Customers by Lifetime Orders

<DataTable data={top25} rows=10>
  <Column id="customer_name"    title="Name" />
  <Column id="customer_segment" title="Segment" />
  <Column id="customer_country" title="Country" />
  <Column id="lifetime_orders"  title="Orders" fmt="#,##0" />
  <Column id="first_order_date" title="First Order" />
  <Column id="last_order_date"  title="Last Order" />
</DataTable>
