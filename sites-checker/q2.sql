    --2. Site visiting question - you have the following tables:
    --• site_visitors : date, site, number of visitors
    --• promotion dates : start_date, end_date, site, promotion_code


DROP TABLE IF EXISTS "promotion_dates";
CREATE TABLE "public"."promotion_dates" (
    "start_date" date NOT NULL,
    "end_date" date NOT NULL,
    "site_id" integer NOT NULL,
    "promotion_code" integer NOT NULL
) WITH (oids = false);

INSERT INTO "promotion_dates" ("start_date", "end_date", "site_id", "promotion_code") VALUES
('2020-09-22',	'2020-09-22',	2,	2),
('2020-09-20',	'2020-09-22',	1,	1);

DROP TABLE IF EXISTS "site_visitors";
CREATE TABLE "public"."site_visitors" (
    "date" date NOT NULL,
    "number_of_visitors" integer,
    "site" integer NOT NULL
) WITH (oids = false);

INSERT INTO "site_visitors" ("date", "number_of_visitors", "site") VALUES
('2020-09-22',	30,	1),
('2020-09-21',	20,	1),
('2020-09-20',	10,	1),
('2020-09-20',	30,	2),
('2020-09-20',	30,	2),
('2020-09-22',	10,	2);


SELECT count("number_of_visitors")/avg("number_of_visitors"), site
FROM "site_visitors" a inner join promotion_dates b on (b.site_id=a.site)
where date BETWEEN "start_date" and "end_date"
GROUP BY site