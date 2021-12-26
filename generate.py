import datetime
import json
import requests
import os
import sys
import zipfile
import shutil
import tempfile

root = tempfile.TemporaryDirectory()

python = sys.executable

start_time = datetime.datetime.now()

courses = [
    {
        'url': 'https://github.com/kantord/LibreLingo-ES-from-EN/archive/refs/heads/main.zip',
        'sdir': 'LibreLingo-ES-from-EN-main',
        'tdir': 'spanish-from-english',
    },
    {
        'url': 'https://github.com/szabgab/LibreLingo-Judeo-Spanish-from-English/archive/refs/heads/main.zip',
        'sdir': 'LibreLingo-Judeo-Spanish-from-English-main',
        'tdir': 'ladino-from-english',
    },
    {
        'url': 'https://github.com/szabgab/LibreLingo-Judeo-Spanish-from-Hebrew/archive/refs/heads/main.zip',
        'sdir': 'LibreLingo-Judeo-Spanish-from-Hebrew-main',
        'tdir': 'ladino-from-hebrew',
    },
    {
        'url': 'https://github.com/szabgab/LibreLingo-Judeo-Spanish-from-Spanish/archive/refs/heads/main.zip',
        'sdir': 'LibreLingo-Judeo-Spanish-from-Spanish-main',
        'tdir': 'ladino-from-spanish',
    },
    {
        'url': 'https://codeberg.org/Lamdarer/LibreLingo-DE-from-EN/archive/main.zip',
        'sdir': 'librelingo-de-from-en',
        'tdir': 'german-from-english',
    },
]

print(root.name)

docs = 'docs'

if os.path.exists(docs):
    shutil.rmtree(docs)
os.mkdir(docs)

links = []

for course in courses:
    tdir = course['tdir']
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
    docs_dir = os.path.join(current_dir, docs, tdir)
    cmd = f"{python} {current_dir}/LibreLingo-tools/lili.py --course course --html {docs_dir}"
    print(cmd)
    assert os.system(cmd) == 0
    os.chdir(current_dir)
    with open(os.path.join(docs_dir, 'stats.json')) as fh:
        count = json.load(fh)
    links.append(f'''<tr><td><a href="{tdir}">{tdir}</a></td><td>{count["words"]}</td><td>{count["phrases"]}</td></tr>''')


current_dir = os.getcwd()
os.chdir('LibreLingo')
tdir = 'basque-from-english'
docs_dir = os.path.join(current_dir, docs, tdir)
cmd = f"{python} {current_dir}/LibreLingo-tools/lili.py --course courses/basque-from-english --html {docs_dir}"
print(cmd)
#assert os.system(cmd) == 0
os.system(cmd)
with open(os.path.join(docs_dir, 'stats.json')) as fh:
    count = json.load(fh)
links.append(f'''<tr><td><a href="{tdir}">{tdir}</a></td><td>{count["words"]}</td><td>{count["phrases"]}</td></tr>''')
os.chdir(current_dir)

for tdir in os.listdir('LibreLingo/temporarily_inactive_courses/'):
    if tdir == 'basque-from-english':
        continue
    current_dir = os.getcwd()
    os.chdir('LibreLingo')
    docs_dir = os.path.join(current_dir, docs, tdir)
    cmd = f"{python} {current_dir}/LibreLingo-tools/lili.py --course temporarily_inactive_courses/{tdir} --html {docs_dir}"
    print(cmd)
    assert os.system(cmd) == 0
    with open(os.path.join(docs_dir, 'stats.json')) as fh:
        count = json.load(fh)
    links.append(f'''<tr><td><a href="{tdir}">{tdir}</a></td><td>{count["words"]}</td><td>{count["phrases"]}</td></tr>''')
    os.chdir(current_dir)

end_time = datetime.datetime.now()
links_str = '\n'.join(sorted(links))

html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=yes">
  <head>
    <title>LibreLingo courses</title>
  </head>
  <body>
    <h1><a href="https://librelingo.app/">LibreLingo courses</a></h1>
    <table>
        <tr><th>Course</th><th>Words</th><th>Phrases</th></tr>
        {links_str}
    </table>
    <div>Generated at {start_time} Elapsed time: {(end_time-start_time).seconds} seconds</div>
  </body>
</html>
"""
with open(os.path.join(docs, "index.html"), 'w') as fh:
    fh.write(html)



