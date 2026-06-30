select
    product_title,
    product_category,
    total_revenue,
    total_units_sold,
    margin_pct,
    cost,
    price
from main_marts.dim_product
order by total_revenue desc
