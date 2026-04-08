with staged as (
    select *
    from {{ ref('stg_wind_solar') }}
),

expanded as (
    select
        generation_item
    from staged
    cross join lateral jsonb_array_elements((staged.payload_json::jsonb -> 'data')) as generation_item
)

select
    (generation_item ->> 'startTime')::timestamptz as start_time,
    generation_item ->> 'psrType' as psr_type,
    (generation_item ->> 'quantity')::numeric as quantity
from expanded
