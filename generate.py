import datetime

now = datetime.datetime.now()

courses = []

html = f"""
<html>
  <head>
    <title>LibreLingo courses</title>
  </head>
  <body>
    <h1><a href="https://librelingo.app/">LibreLingo courses</a></h1>
    <div>Generated at {now}</div>
  </body>
</html>
"""
with open("docs/index.html", 'w') as fh:
    fh.write(html)



#LibreLingo-tools/lili.py --ids --course course/ --images LibreLingo/apps/web/static/images/ --export
