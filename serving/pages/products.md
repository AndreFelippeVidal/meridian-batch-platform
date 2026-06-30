---
title: Meridian — Products
---

```sql top20
select
    product_title,
    product_category,
    total_revenue,
    total_units_sold,
    margin_pct
from products
order by total_revenue desc
limit 20
```

```sql by_category
select
    product_category,
    sum(total_revenue)    as category_revenue,
    sum(total_units_sold) as category_units,
    avg(margin_pct)       as avg_margin_pct
from products
group by product_category
order by category_revenue desc
```

# Products

## Revenue by Category

<BarChart
  data={by_category}
  x="product_category"
  y="category_revenue"
  title="Revenue by Category"
  yFmt="$#,##0"
/>

## Average Margin by Category

<BarChart
  data={by_category}
  x="product_category"
  y="avg_margin_pct"
  title="Average Margin % by Category"
  yFmt="0.0%"
/>

## Top 20 Products by Revenue

<DataTable data={top20} rows=10>
  <Column id="product_title"    title="Product" />
  <Column id="product_category" title="Category" />
  <Column id="total_revenue"    title="Revenue" fmt="$#,##0.00" />
  <Column id="total_units_sold" title="Units Sold" fmt="#,##0" />
  <Column id="margin_pct"       title="Margin %" fmt="0.0%" />
</DataTable>
