-- Creating external table referring to gcs path
CREATE OR REPLACE EXTERNAL TABLE `ny_taxi.green_cab_data`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://mage-zoomcamp-marius/green_taxi_data_monthly/*']
);

-- Check green trip data
SELECT * FROM ny_taxi.green_cab_data limit 10;

-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE ny_taxi.green_tripdata_non_partitoned AS
SELECT * FROM ny_taxi.green_cab_data;

-- Check non partitioned data
SELECT count(*) FROM ny_taxi.green_tripdata_non_partitoned;

-- Count the distinct number of PULocationIDs for the entire dataset - BOTH TABLES
SELECT count(DISTINCT PULocationID) FROM `ny_taxi.green_cab_data`;
SELECT count(DISTINCT PULocationID) FROM ny_taxi.green_tripdata_non_partitoned;

-- records with a fare_amount of 0?
SELECT 
  count(*) 
FROM 
  ny_taxi.green_tripdata_non_partitoned
WHERE
  fare_amount = 0;

-- query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 - NON PARTITIONED
select 
  DISTINCT PULocationID
from
  ny_taxi.green_tripdata_non_partitoned
where
  TIMESTAMP_SECONDS(cast(lpep_pickup_datetime/1000000000 as int64)) between '2022-06-01' and '2022-06-30';

-- CREATE partitioned and clustered table

CREATE OR REPLACE TABLE ny_taxi.green_tripdata_partitoned_clustered
PARTITION BY PU_DATE
CLUSTER BY PUlocationID AS
SELECT 
  *,
  date(TIMESTAMP_SECONDS(cast(lpep_pickup_datetime/1000000000 as int64)) ) as PU_DATE
FROM 
  ny_taxi.green_tripdata_non_partitoned;


  -- query to retrieve the distinct PULocationID between lpep_pickup_datetime 06/01/2022 and 06/30/2022 - PARTITIONED
select 
  DISTINCT PULocationID
from
  ny_taxi.green_tripdata_partitoned_clustered
where
  TIMESTAMP_SECONDS(cast(lpep_pickup_datetime/1000000000 as int64)) between '2022-06-01' and '2022-06-30'
limit 10;