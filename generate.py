import datetime
import requests
import os
import zipfile
import shutil
import tempfile

root = tempfile.TemporaryDirectory()

now = datetime.datetime.now()

courses = [
    {
        'url': 'https://github.com/szabgab/LibreLingo-Judeo-Spanish-from-English/archive/refs/heads/main.zip',
        'sdir': 'LibreLingo-Judeo-Spanish-from-English-main',
        'tdir': 'ladino-from-english',
    },
    {
        'url': 'https://codeberg.org/Lamdarer/LibreLingo-DE-from-EN/archive/main.zip',
        'sdir': 'librelingo-de-from-en',
        'tdir': 'german-from-english',
    },
]
#https://github.com/kantord/LibreLingo-ES-from-EN/archive/refs/heads/main.zip spanish-from-english
#https://github.com/szabgab/LibreLingo-Judeo-Spanish-from-Spanish/archive/refs/heads/main.zip" ladino-from-spanish
#https://github.com/szabgab/LibreLingo-Judeo-Spanish-from-Hebrew/archive/refs/heads/main.zip" ladino-from-hebrew

print(root.name)

if os.path.exists('docs'):
    shutil.rmtree('docs')
os.mkdir('docs')

links = ''

for course in courses:
    #download zip file
    res = requests.get(course['url'], stream=True)
    filename = os.path.join(root.name, "course.zip")
    if res.status_code == 200:
        with open(filename, 'wb') as fh:
            res.raw.decode_content
            shutil.copyfileobj(res.raw, fh)

    #unzip it
    zf = zipfile.ZipFile(filename)
    zf.extractall(path=root.name)


    # generate file
    #course_dir = os.path.join(root.name, course['sdir'], 'course')
    course_dir = os.path.join(root.name, course['sdir'])
    current_dir = os.getcwd()
    os.chdir(course_dir)
    docs_dir = os.path.join(current_dir, 'docs', course['tdir'])
    os.system(f"python {current_dir}/LibreLingo-tools/lili.py --course course --html {docs_dir}")
    os.chdir(current_dir)
    links += f'''<li><a href="{course['tdir']}">{course['tdir']}</a></li>\n'''


html = f"""
<html>
  <head>
    <title>LibreLingo courses</title>
  </head>
  <body>
    <h1><a href="https://librelingo.app/">LibreLingo courses</a></h1>
    <ul>
        {links}
    </ul>
    <div>Generated at {now}</div>
  </body>
</html>
"""
with open("docs/index.html", 'w') as fh:
    fh.write(html)



