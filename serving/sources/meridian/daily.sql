select
    order_date,
    gmv,
    orders_placed,
    aov,
    units_sold,
    revenue_collected,
    revenue_failed,
    revenue_refunded
from main_marts.mart_marketplace_daily
order by order_date
