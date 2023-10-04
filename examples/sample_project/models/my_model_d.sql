select id from {{ ref('my_model_c') }}
where id is not null
