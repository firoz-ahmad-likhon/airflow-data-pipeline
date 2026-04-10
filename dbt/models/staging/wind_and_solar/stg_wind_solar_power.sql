select
    id,
    ingestion_ts,
    window_from_utc,
    window_to_utc,
    request_url,
    http_status,
    payload_json::jsonb as payload_json
from {{ source('elexon', 'bmrs_datasets') }}
where
    payload_json is not null
    and data_type = 'wind_and_solar_power'
    and http_status = 200
