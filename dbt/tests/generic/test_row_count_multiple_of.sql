{% test row_count_multiple_of(model, divisor=3) %}

with validation as (
    select count(*) as total_rows
    from {{ model }}
),

validation_errors as (
    select total_rows
    from validation
    where mod(total_rows, {{ divisor }}) != 0
)

select *
from validation_errors

{% endtest %}
