with source as (

    select * from {{ ref('raw_suppliers') }}

),

cleaned as (

    select
        supplier_id,
        trim(supplier_name)                        as supplier_name_raw,
        lower(trim(supplier_name))                 as supplier_name_key,
        nullif(trim(region), '')                   as region,
        lower(trim(status)) = 'active'             as is_active,
        cast(created_at as date)                   as created_at
    from source

)

select * from cleaned