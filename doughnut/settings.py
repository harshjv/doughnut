import os

CONFIG_FILE_NAME = "doughnut.json"
SCHEMA_FILE_NAME = "schema.json"

RESOURCE_DIRECTORY = os.path.abspath("resources")
UPLOAD_DIRECTORY = os.path.abspath("upload")
BUILD_DIRECTORY = os.path.abspath("build")
STATIC_DIRECTORY = os.path.abspath("static")

CSS_FILE = os.path.join(RESOURCE_DIRECTORY, "css", "style.css")
TEMPLATE_DIRECTORY = os.path.join(RESOURCE_DIRECTORY, "templates")
SCHEMA_FILE = os.path.join(STATIC_DIRECTORY, SCHEMA_FILE_NAME)

PDF_OPTIONS = {
    'encoding': 'UTF-8',
    'page-size': 'A4',

    'margin-top': '0.5in',
    'margin-bottom': '0.3in',
    'margin-left': '0in',
    'margin-right': '0in',

    'header-spacing': '3.8',
    'footer-spacing': '1.8',

    'no-outline': None,

    'disable-local-file-access': None,
    'disable-external-links': None
}

ASTYLE_OPTIONS = "--mode={mode} --style=google --indent=spaces=4 -xC50 -xG -C -S -K -N -L -xW -w -xw -Y -p -U -xe -k3 -W3 -j -xp -c -xy -xL -F"

PYGMENT_HTML_LINE_SPAN_PREFIX = "doughnut-span"

ASTYLE_BLACKLIST_EXTENSIONS = ['lex', 'l', 'html', 'jsp', 'hbm', 'cfg']
