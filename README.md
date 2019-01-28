## QUICKSTART
From your terminal, `cd` to project directory and run: `python analysis.py`
This was developed using Python Version 2.7.12

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

## LICENCE

This was created by Marlon Card and is covered under terms of the [MIT License](https://opensource.org/licenses/MIT).
