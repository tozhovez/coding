--    1. Employee question - you have the following tables:
--    • employees: employee_id, first_name, last_name, hire_date, salary, manager_id, department_id
--    • departments: department_id, department_name, location_id
--
--We would like to know for each department top earning employee, salary, difference
--from the second earning employee.

DROP TABLE IF EXISTS "departments";
CREATE TABLE "public"."departments" (
    "department_id" integer NOT NULL,
    "department_name" character varying(50) NOT NULL,
    "location_id" integer NOT NULL,
    CONSTRAINT "departments_department_id" PRIMARY KEY ("department_id")
) WITH (oids = false);

INSERT INTO "departments" ("department_id", "department_name", "location_id") VALUES
(1,	'department_a',	1),
(2,	'department_b',	2);

DROP TABLE IF EXISTS "employees";
CREATE TABLE "public"."employees" (
    "employee_id" integer NOT NULL,
    "first_name" character varying(50) NOT NULL,
    "last_name" character varying(50) NOT NULL,
    "hire_date" date NOT NULL,
    "salary" money NOT NULL,
    "manager_id" integer NOT NULL,
    "department_id" integer NOT NULL,
    CONSTRAINT "employees_employee_id" PRIMARY KEY ("employee_id"),
    CONSTRAINT "employees_department_id_fkey" FOREIGN KEY (department_id) REFERENCES departments(department_id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE
) WITH (oids = false);

INSERT INTO "employees" ("employee_id", "first_name", "last_name", "hire_date", "salary", "manager_id", "department_id") VALUES
(1,	'aaa',	'aaa',	'2020-09-22',	'₪ 2,000.00',	1,	1),
(2,	'aac',	'asd',	'2020-09-22',	'₪ 3,000.00',	2,	1),
(3,	'wer',	'dfg',	'2020-09-22',	'₪ 29,876.00',	1,	2),
(4,	'dfg',	'dfg',	'2020-09-22',	'₪ 398,765.00',	2,	1),
(5,	'rty',	'wret',	'2020-09-22',	'₪ 3,457.00',	2,	2);

WITH max_salarys(max_salary, department_id)
as(
SELECT MAX(salary) as max_salary, department_id
FROM employees
GROUP BY department_id
),
all_result (max_salary, department_id, employee_id) as
(SELECT a.max_salary, a.department_id, b.employee_id
FROM max_salarys a
inner join employees b
on (a.department_id=b.department_id and a.max_salary=b.salary
) ),
second_salary(second_max_salary, department_id ) as
(select max(salary) as max_salary, department_id
from employees
where  employee_id not in ( select employee_id from all_result)
GROUP BY department_id)

select a.department_id, a.employee_id, a.max_salary, (a.max_salary-b.second_max_salary) as diff
from all_result a inner join second_salary b on(a.department_id=b.department_id)
