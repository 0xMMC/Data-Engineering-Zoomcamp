{{
    config(
        materialized='view'
    )
}}


  select 
    *,
  from 
    {{ source('staging','fhv') }}
  where
    left(pickup_datetime, 4) = '2019'