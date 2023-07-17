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