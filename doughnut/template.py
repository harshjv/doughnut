import os
import base64
import imghdr
import jinja2
import pyastyle
import pygments
import pygments.lexers
import pygments.formatters
import doughnut.fixer
from doughnut import settings
from doughnut.exceptions import InvalidSource

class Template:
    def __init__(self, config, source, build_directory):
        self.config = config
        self.build_directory = build_directory
        self.source = source
        self.env = jinja2.Environment(loader=jinja2.FileSystemLoader(settings.TEMPLATE_DIRECTORY))

    def register(self):
        self.env.filters['datetimeformat'] = self.__datetimeformat
        self.env.filters['basename'] = self.__basename
        self.env.globals['print_source'] = self.__print_source
        self.env.globals['print_text'] = self.__print_text
        self.env.globals['print_image'] = self.__print_image
        self.env.globals['get_stylesheet'] = self.__get_stylesheet
        self.env.globals['print_indexes'] = self.__print_indexes
        self.env.globals['get_index0'] = self.__get_index0
        self.env.globals['get_index1'] = self.__get_index1

    def buildAll(self):
        if not os.path.exists(self.build_directory):
            os.makedirs(self.build_directory)

        self.build('index.html')
        self.build('header.html')
        self.build('footer.html')

    def build(self, name):
        template = self.env.get_template(name)

        with open(os.path.join(self.build_directory, name), 'w') as out:
            out.write(template.render(config=self.config) + '\n')

    def __get_index0(self, string):
        if not string:
            return False
        elif "." in string:
            return int(string.split(".")[0])
        else:
            return int(string)

    def __get_index1(self, string):
        if "." in string:
            return int(string.split(".")[1])
        else:
            return False

    def __print_indexes(self, index0, index1='', index2='', index3=''):
        k = [ x for x in [str(index3), str(index2), str(index1), str(index0)] if len(x) > 0 ]
        return '.'.join(k)

    def __datetimeformat(self, value, format="%d/%m/%y"):
        return datetime.strptime(value, format).strftime('%-d %B %Y')

    def __basename(self, value):
        return os.path.basename(value)

    def __get_stylesheet(self):
        with open(settings.CSS_FILE, "r") as text_file:
            text = text_file.read()

        return text

    def __print_text(self, filename):
        text = self.source.read(filename)
        return "<pre>{text}</pre>".format(text=text)

    def __print_image(self, filename):
        bytes = self.source.readBytes(filename)
        encoded_string = base64.b64encode(bytes).decode('UTF-8')

        img_html = '<img src="data:image/{type};base64,{data_uri}">'
        img_html = img_html.format(type=imghdr.what(filename, self.source.readBytes(filename, 32)), data_uri=encoded_string.replace("\n", ""))

        return img_html

    def __print_source(self, filename):
        try:
            lexer = pygments.lexers.get_lexer_for_filename(filename)
        except pygments.util.ClassNotFound as e:
            lexer = pygments.lexers.get_lexer_for_filename("hello.c")

        code = self.source.read(filename)
        mode = os.path.splitext(filename)[1].lower()[1:]

        if mode not in settings.ASTYLE_BLACKLIST_EXTENSIONS:
            if mode not in ['c', 'cs', 'java']:
                mode = 'c'

            opts = settings.ASTYLE_OPTIONS.format(mode=mode)
            code = pyastyle.format(code, opts)

        return doughnut.fixer.fix_highlight(pygments.highlight(code, lexer, pygments.formatters.HtmlFormatter(linenos=True, linespans=settings.PYGMENT_HTML_LINE_SPAN_PREFIX)))
