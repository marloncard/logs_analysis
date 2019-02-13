# Logs Analysis: Reporting Tool
This "**reporting tool**" represents my solution to the "_Logs Analysis_" project as part of Udacity's Full Stack Web Developer Nanodegree. This project explores basic concepts in Python and relational databases (Postgresql) including querying, creating views and aggregate functions.

## QUICKSTART
From your terminal, `cd` to project directory and run: `python analysis.py`

## DEPENDENCIES
* This was developed using Python Version 2.7.12
* This script uses the `psycopg2` module
* The database used is Postgresql Version 9.5.14

## DATABASE
The data is presented as being from a fictional news website. It provides information on authors, their articles and a website log of about 1.6 million rows detailing which articles were accessed, when and the status code that was returned. Specifically, the database includes three tables with the following information:
 * `authors` containing information on each author
 * `articles` containing a list of articles written by each author
 * `log` shows access of each article over the course of a month as well as returned HTTP response codes (`200 OK`, `404 NOT FOUND`).

## QUESTIONS
1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser.


## POSTGRESQL VIEWS
```
CREATE VIEW ok_status AS
  SELECT DATE(time) as date1, count(path) as num1
  FROM log
  WHERE status LIKE '%200%'
  GROUP BY date1
  ORDER BY date1
```
```
CREATE VIEW not_ok AS
  SELECT DATE(time) AS date2, count(path) as num2
  FROM log
  WHERE status NOT LIKE '%200%'
  GROUP BY date2
  ORDER BY date2
```

## LICENSE

This was created by Marlon Card and is covered under terms of the [MIT License](https://opensource.org/licenses/MIT).
