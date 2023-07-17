
# Globant's DE Coding Challenge

Technical test for Data Engineer role in Globant

#### NOTE: All AWS resources were stopped and deleted for avoid consume in my AWS account


## Architecture Diagram

![alt text](https://github.com/giorocar/GlobantCodingChallenge/blob/main/images/diagram_app.png?raw=true)

To resolve the challenge was used this stack

API REST: Flask Api a popular python framework used in api creation.

DATABASE: the database used is AWS Redshift Warehouse service, according to the challenge these need to support big data, so for me these is appropriate in order to take advantage of their scalability, flexibility and compatibility.

ENDPOINTS: The API REST is developed with Python, Flask API which have 2 endpoints to use
uploadFile/ to upload the data Challenge 1.
metrics/ to show insights Challenge 2

## Repositorio Estructura

```
├── src/                        --App folder 
│   ├── data_quality/
│   │   └── data_quality.py     --review data quality
│   ├── database/
│   │   └── services.py         --functiones with database
│   ├── dict/
│   │   └── tables.py           --structure of tables
│   └── security/
│       └── AWSSecretManager.py --get credenciales AWS
├── Dockerfile                  --Dockerfile
├── gunicorn.sh                 --Script for start web services
├── README.md                   --README file
└── requirements.txt            --python libraries
```
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`AWS_ACCESS_KEY`

`AWS_SECRET_KEY`


## Installation

#### Install database
Prerequisite:

- Cluster Redshift

#### Scripts

``` sql
CREATE TABLE IF NOT EXISTS HIRED_EMPLOYEES
(
    ID            INTEGER PRIMARY KEY,
    NAME          VARCHAR,
    DATETIME      VARCHAR,
    DEPARTMENT_ID INTEGER,
    JOB_ID        INTEGER
);

CREATE TABLE IF NOT EXISTS DEPARTMENTS
(
    ID         INTEGER PRIMARY KEY,
    DEPARTMENT VARCHAR
);

CREATE TABLE IF NOT EXISTS JOBS
(
    ID  INTEGER PRIMARY KEY,
    JOB VARCHAR
);

--Number of employees hired for each job and department 
--in 2021 divided by quarter. The
table must be ordered alphabetically by department and job.
CREATE OR REPLACE VIEW num_emp_hired_x_job_dpto AS
SELECT * FROM (
        SELECT DEPARTMENT,
                JOB,
                EXTRACT(QTR FROM TO_DATE("DATETIME", 'YYYY-MM-DD"T"HH24:MI:SSZ')) AS QTR
        FROM HIRED_EMPLOYEES E
                LEFT JOIN JOBS J ON E.JOB_ID = J.ID
                LEFT JOIN DEPARTMENTS D ON E.DEPARTMENT_ID = D.ID
        WHERE EXTRACT(Y FROM TO_DATE("DATETIME", 'YYYY-MM-DD"T"HH24:MI:SSZ')) = 2021
)PIVOT (COUNT(*)  FOR QTR IN (1, 2, 3, 4))
		AS P(DEPARTMENT,
                        JOB,                        
                        "Q1",
                        "Q2",
                        "Q3",
                        "Q4")
	ORDER BY
		DEPARTMENT, JOB 
;

--List of ids, name and number of employees hired of each 
--department that hired more
--employees than the mean of employees hired in 2021 for 
--all the departments, ordered
--by the number of employees hired (descending).
CREATE OR REPLACE VIEW list_emp_hired_x_dpto AS
WITH COUNT_HIRES_BY_DEPARTMENT AS 
(
        SELECT D.ID, DEPARTMENT, COUNT(*) HIRED
        FROM HIRED_EMPLOYEES E
        LEFT JOIN DEPARTMENTS D ON E.DEPARTMENT_ID = D.ID
        WHERE EXTRACT(Y FROM TO_DATE("DATETIME", 'YYYY-MM-DD"T"HH24:MI:SSZ')) = 2021
        GROUP BY 1, 2
)
SELECT ID, DEPARTMENT, HIRED
FROM COUNT_HIRES_BY_DEPARTMENT
WHERE HIRED > (SELECT AVG(HIRED) FROM COUNT_HIRES_BY_DEPARTMENT)
ORDER BY 3 DESC;
```

To install and use the api.

Build the container, providing a tag:

```docker build -t starwars/app:1.0 .```

Then you can run the container, passing in a name for the container, and the previously used tag:
```docker run -p 8000:8000 --name my-api starwars/app:1.0```

The API will be available in or in the machine host used http://127.0.0.1:8000/

Note that if you used the code as-is with the ```--reload``` option that you won't be able to kill the container using ```CTRL + C```.
Instead in another terminal window you can kill the container using Docker's kill command:

```docker kill my-api```
## API Reference

#### Get root

```http
  GET /
```
#### Post uploadFile

```http
  POST /uploadFile
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `Binary` | **Required**. File to upload |

Here you can upload data from a file csv. This endpoint just accept the next filename:

- hired_employeesXXXXXXX.csv
- departmentsXXXXXXX.csv
- jobsXXXXXXX.csv

#### Response
```json
{
  "content": {
    "columns": [
      "id",
      "job"
    ],
    "file": "jobs.csv",
    "nrows_inserted": 183,
    "result": "All the records have been uploaded",
    "rows": 183,
    "type": "jobs"
  },
  "status_code": 200
}
```

#### Post metrics

```http
  POST /metrics
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `metric`      | `string` | **Required**. metric name to request, only is permited the values num_emp_hired_x_job_dpto and list_emp_hired_x_dpto|

Here you can get two kinds of metrics:

- num_emp_hired_x_job_dpto

Number of employees hired for each job and department in 2021 divided by quarter. The table must be ordered alphabetically by department and job.

- list_emp_hired_x_dpto

List of ids, name and number of employees hired of each department that hired more employees than the mean of employees hired in 2021 for all the departments, ordered by the number of employees hired (descending).

#### Response
```json
{
    "content": [
        {
            "department": "Accounting",
            "job": "Analyst Programmer",
            "q1": 0,
            "q2": 0,
            "q3": 4,
            "q4": 0
        },
        {
            "department": "Accounting",
            "job": "Budget/Accounting Analyst III",
            "q1": 0,
            "q2": 4,
            "q3": 0,
            "q4": 0
        },
        {
            "department": "Accounting",
            "job": "Cost Accountant",
            "q1": 0,
            "q2": 4,
            "q3": 0,
            "q4": 0
        },
        {
            "department": "Accounting",
            "job": "Database Administrator III",
            "q1": 0,
            "q2": 0,
            "q3": 0,
            "q4": 4
        },
        {
            "department": "Accounting",
            "job": "Desktop Support Technician",
            "q1": 0,
            "q2": 0,
            "q3": 4,
            "q4": 0
        },
    ]
}
```

## Running App

To run App, run the following command

Endpoint: Upload File
```
curl \
  -F "file=@/path/to/file/jobs.csv" \
  http://<HOST_NAME>:8000/uploadFile
```

Endpoint: Metric 1
```
  curl --location http://<HOST_NAME>:8000/metrics?query=num_emp_hired_x_job_dpto'
```

Endpoint: Metric 2
```
  curl --location 'http://<HOST_NAME>:8000/metrics?query=list_emp_hired_x_dpto'
```
