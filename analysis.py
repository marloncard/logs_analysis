#!/usr/bin/env python2
import psycopg2


DBNAME = "news"


try:
    db = psycopg2.connect(database=DBNAME)
except psycopg2.Error as e:
    print("Unable to connect to the database")


def main():
    format_output(topThree())
    format_output(topAuthor())
    format_output(onePercent())
    db.close()


def topThree():
    cursor = db.cursor()
    query_question = "1. What are the most popular three articles of all time?"
    cursor.execute('''
        SELECT articles.title, count(log.path) || ' views' as num
        FROM articles
        JOIN log
        ON log.path LIKE '%' || articles.slug
        GROUP BY articles.title
        ORDER BY count(log.path) DESC
        LIMIT 3;
        ''')
    return (cursor.fetchall(), query_question)


def topAuthor():
    cursor = db.cursor()
    query_question = '''2. What are the most popular article authors of all
    time?'''
    cursor.execute('''
        SELECT authors.name, count(log.path) || ' views' as num
        FROM authors
        JOIN articles
        ON authors.id = articles.author
        JOIN log
        ON log.path LIKE '%' || articles.slug
        GROUP BY authors.name
        ORDER BY count(log.path) DESC;
        ''')
    return (cursor.fetchall(), query_question)


def onePercent():
    cursor = db.cursor()
    query_question = '''3. On which days did more than 1% of requests lead to
    errors?'''
    # DATABASE VIEWS #
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
        SELECT to_char(date1, 'FMMonth DD, YYYY'),
          round((num2::decimal  / (num1+num2)::decimal)*100, 2) || '% errors'
          AS num_tot
          FROM ok_status
          JOIN not_ok
          ON date1 = date2
          WHERE (num2::decimal  / (num1+num2)::decimal)*100 > 1;
         ''')
    return (cursor.fetchall(), query_question)


def format_output((arg1, arg2)):
    print(arg2)
    print("=" * len(arg2))
    for item in arg1:
        print(str(item[0]) + ' - ' + str(item[1]))
    print("=" * len(arg2))
    print("\n\n")


if __name__ == "__main__":
    main()
