create or replace database DIABETES_DB;

CREATE or replace schema DIABETES_DB.EXTERNAL_STAGES;
CREATE or replace schema DIABETES_DB.file_formats;
CREATE or replace schema DIABETES_DB.INTERNAL_STAGES;

CREATE OR REPLACE FILE FORMAT DIABETES_DB.file_formats.csv_fileformat    
    TYPE = CSV
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    RECORD_DELIMITER = '\r'
    NULL_IF = ('NULL','null')
    EMPTY_FIELD_AS_NULL = TRUE;



CREATE OR REPLACE STAGE DIABETES_DB.EXTERNAL_STAGES.DIABETES_DATA
    URL = 's3://diabetes-ml2025/'
    CREDENTIALS = (
        AWS_KEY_ID = 'YOURKEY'
        AWS_SECRET_KEY = 'YOURKEY2'
    )
    FILE_FORMAT = DIABETES_DB.file_formats.csv_fileformat;

CREATE OR REPLACE TABLE DIABETES_DB.public.DIABETES_TABLE(
    ID int,
    No_Pation int,
    Gender string,
    AGE int,
    Urea float,
    Cr int,
    HbA1c float,
    Chol float,
    TG float,
    HDL float,
    LDL float,
    VLDL float,
    BMI float,
    clase string );

COPY INTO DIABETES_DB.public.DIABETES_TABLE
  FROM @DIABETES_DB.EXTERNAL_STAGES.DIABETES_DATA
  ON_ERROR = 'CONTINUE';
    
SELECT * FROM DIABETES_DB.public.diabetes_table;