#!/usr/bin/env python2.7
import psycopg2


DBNAME = "news"

def main():
    output = top_three()
    output = top_author()
    output = one_percent()

def top_three():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    # 1. What are the most popular three articles of all time?
    cursor.execute('''
        SELECT articles.title, count(log.path) as num
        FROM articles
        JOIN log
        ON log.path LIKE '%' || articles.slug || '%'
        GROUP BY articles.title
        ORDER BY num DESC
        LIMIT 3;
        ''')
    return cursor.fetchall()
    db.close()

def top_author():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    # 2. What are the most popular article authors of all time?
    cursor.execute('''
        SELECT authors.name, count(log.path) as num
        FROM authors
        JOIN articles
        ON authors.id = articles.author
        JOIN log
        ON log.path LIKE '%' || articles.slug || '%'
        GROUP BY authors.name
        ORDER BY num DESC;
        ''')
    return cursor.fetchall()
    db.close()

def one_percent():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    # 3. On which days did more than 1% of requests lead to errors?
    # CREATE VIEW ok_status AS
    #   SELECT DATE(time) as date1, count(path) as num1
    #   FROM log
    #   WHERE status LIKE '%200%'
    #   GROUP BY date1
    #   ORDER BY date1
    # CREATE VIEW not_ok AS
    #   SELECT DATE(time) AS date2, count(path) as num2
    #   FROM log
    #   WHERE status NOT LIKE '%200%'
    #   GROUP BY date2
    #   ORDER BY date2
    cursor.execute('''
        SELECT date1,
          (CAST(num2 AS decimal)  / CAST(num1+num2 AS decimal))*100 AS num_tot
          FROM ok_status
          JOIN not_ok
          ON date1 = date2
          WHERE (CAST(num2 AS decimal)  / CAST(num1+num2 AS decimal))*100 > 1;
          ''')
    return cursor.fetchall()
    db.close()

def format_output(arg1):
    for item in output:
        print(str(item[0]) + ' - ' + str(item[1]))


output = one_percent()
print("What are the most popular three articles of all time?\n" + "=" * 30)
format_output(output)
