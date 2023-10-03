select id from {{ ref('my_model_a') }}
union
select id from {{ ref('my_model_b') }}