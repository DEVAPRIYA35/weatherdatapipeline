CREATE DATABASE WEATHER_DB;
CREATE SCHEMA WEATHER_SCHEMA;

USE DATABASE WEATHER_DB;
USE SCHEMA WEATHER_SCHEMA;

CREATE OR REPLACE STORAGE INTEGRATION weather_s3_int
TYPE = EXTERNAL_STAGE
STORAGE_PROVIDER = S3
ENABLED = TRUE
STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::250847880906:role/snowflake-s3-role'
STORAGE_ALLOWED_LOCATIONS = ('s3://openweatherbucket-250847880906-us-east-1-an/');

DESC INTEGRATION weather_s3_int;

ALTER STORAGE INTEGRATION weather_s3_int
SET STORAGE_AWS_ROLE_ARN='arn:aws:iam::250847880906:role/snowflake-s3-role';

CREATE OR REPLACE STAGE weather_stage
STORAGE_INTEGRATION = weather_s3_int
URL = 's3://openweatherbucket-250847880906-us-east-1-an/';

LIST @weather_stage;

CREATE OR REPLACE TABLE weather_json (
    data VARIANT
);


COPY INTO weather_json
FROM @weather_stage
FILE_FORMAT = (TYPE = JSON);

SELECT * FROM weather_json;



CREATE OR REPLACE TABLE weather_data AS
SELECT
    value:city::STRING AS city,
    value:country::STRING AS country,
    value:humidity::INTEGER AS humidity,
    value:openweather_id::INTEGER AS openweather_id,
    value:temperature::FLOAT AS temperature,
    value:time::TIMESTAMP AS time,
    value:weather::STRING AS weather
FROM weather_json,
LATERAL FLATTEN(input => data);

CREATE OR REPLACE PIPE weather_pipe
AUTO_INGEST = TRUE
AS
COPY INTO weather_json
FROM @weather_stage
FILE_FORMAT = (TYPE = JSON);

SHOW PIPES;

DESC PIPE weather_pipe;

SHOW STAGES;

SHOW TABLES;

SELECT * FROM WEATHER_DATA;

SELECT CURRENT_USER();
SHOW WAREHOUSES;
SHOW DATABASES;
SHOW SCHEMAS;
SELECT CURRENT_ACCOUNT();
select current_region();