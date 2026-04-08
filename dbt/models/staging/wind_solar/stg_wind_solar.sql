select
    payload_json
from {{ source('ingestion', 'wind_and_solar_power_generation') }}
where payload_json is not null
