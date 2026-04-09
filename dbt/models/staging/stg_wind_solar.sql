select
    id,
    ingestion_ts,
    window_from_utc,
    window_to_utc,
    request_url,
    http_status,
    payload_json::jsonb as payload_json
from {{ source('ingestion', 'wind_and_solar_power_generation') }}
where
    payload_json is not null
    and http_status = 200
