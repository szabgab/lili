import argparse
import datetime
import json
import requests
import os
import sys
import zipfile
import shutil
import tempfile


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--outdir',        required=True, help='path to output directory')
    args = parser.parse_args()
    return args

def generate_html(start_time, end_time, links, outdir):
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
    with open(os.path.join(outdir, "index.html"), 'w') as fh:
        fh.write(html)


def download_course(url, tempdir):
    # download zip file
    res = requests.get(url, stream=True)
    filename = os.path.join(tempdir.name, "course.zip")
    if res.status_code == 200:
        with open(filename, 'wb') as fh:
            res.raw.decode_content
            shutil.copyfileobj(res.raw, fh)

    # unzip
    zf = zipfile.ZipFile(filename)
    zf.extractall(path=tempdir.name)


def generate_course(sdir, outdir, tdir):
    current_dir = os.getcwd()
    os.chdir(sdir)
    docs_dir = os.path.join(outdir, tdir)
    cmd = f"{python} {current_dir}/LibreLingo-tools/lili.py --course course --html {docs_dir}"
    print(cmd)
    success = os.system(cmd) == 0
    os.chdir(current_dir)
    with open(os.path.join(docs_dir, 'stats.json')) as fh:
        count = json.load(fh)
    return f'''<tr><td><a href="{tdir}">{tdir}</a></td><td>{count["words"]}</td><td>{count["phrases"]}</td></tr>'''


def main():
    args = get_args()
    outdir = os.path.abspath(args.outdir)

    tempdir = tempfile.TemporaryDirectory()
    root = os.path.dirname(os.path.abspath(__file__))


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

    print(tempdir.name)

    if os.path.exists(outdir):
        shutil.rmtree(outdir)
    os.mkdir(outdir)

    links = []

    for course in courses:
        download_course(course['url'], tempdir)
        links.append( generate_course(sdir=os.path.join(tempdir.name, course['sdir']), outdir=outdir, tdir=course['tdir']) )

    current_dir = os.getcwd()
    os.chdir('LibreLingo')
    tdir = 'basque-from-english'
    docs_dir = os.path.join(outdir, tdir)
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
        docs_dir = os.path.join(outdir, tdir)
        cmd = f"{python} {current_dir}/LibreLingo-tools/lili.py --course temporarily_inactive_courses/{tdir} --html {docs_dir}"
        print(cmd)
        assert os.system(cmd) == 0
        with open(os.path.join(docs_dir, 'stats.json')) as fh:
            count = json.load(fh)
        links.append(f'''<tr><td><a href="{tdir}">{tdir}</a></td><td>{count["words"]}</td><td>{count["phrases"]}</td></tr>''')
        os.chdir(current_dir)

    end_time = datetime.datetime.now()
    generate_html(start_time, end_time, links, outdir)


python = sys.executable

main()

