{% set lookback_hours = var('lookback_hours', 6) %}

-- Incremental
with staged as (
    select *
    from {{ ref('stg_wind_solar') }}
    {% if is_incremental() %}
        where ingestion_ts >= now() - interval '{{ lookback_hours }} hour'
    {% endif %}
),

expanded as (
    select
        staged.id,
        staged.ingestion_ts,
        staged.window_from_utc,
        staged.window_to_utc,
        generation_items.generation_item
    from staged
    cross join
        lateral jsonb_array_elements(staged.payload_json -> 'data')
            as generation_items (generation_item)
),

typed as (
    select
        id,
        ingestion_ts,
        window_from_utc,
        window_to_utc,
        (generation_item ->> 'startTime')::timestamptz as start_time,
        generation_item ->> 'psrType' as psr_type,
        (generation_item ->> 'quantity')::numeric as quantity
    from expanded
),

-- Keep the latest ingested row for each event-time and generation-type key.
ranked as (
    select
        *,
        row_number() over (
            partition by start_time, psr_type
            order by ingestion_ts desc, window_to_utc desc, id desc
        ) as row_num
    from typed
)

select
    start_time,
    psr_type,
    quantity
from ranked
where row_num = 1
