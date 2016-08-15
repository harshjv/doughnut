import os
import doughnut
from doughnut.argument_parser import ArgumentParser
from doughnut.configuration import Configuration
from doughnut.template import Template
from doughnut.pdf_generator import PDFGenerator

# args = ArgumentParser(doughnut.CONFIG_FILE_NAME)

source_directory = "upload/java" # args.getSourceDirectory()
output_file = "test.pdf"

here = os.path.abspath(os.path.dirname(__file__))

options = {
    'encoding': 'UTF-8',
    'page-size': 'A4',

    'margin-top': '0.5in',
    'margin-bottom': '0.3in',
    'margin-left': '0in',
    'margin-right': '0in',

    'header-spacing': '3.8',
    'footer-spacing': '1.8',

    'no-outline': None,

    'header-html': os.path.join(here, doughnut.BUILD_DIRECTORY, "header.html"),
    'footer-html': os.path.join(here, doughnut.BUILD_DIRECTORY, "footer.html"),

    'disable-local-file-access': None,
    'disable-external-links': None
}

config = Configuration(doughnut.CONFIG_FILE_NAME, source_directory).getConfig()

if config['title']:
    options['title'] = config['title']

if config['page-starts-from']:
    options['page-offset'] = config['page-starts-from'] - 1

template = Template(config, doughnut.TEMPLATE_DIRECTORY, source_directory, doughnut.BUILD_DIRECTORY, "%s/css/style.css" % os.path.join(here, doughnut.CSS_DIRECTORY))
template.register()
template.buildAll()
pdf_generator = PDFGenerator(doughnut.BUILD_DIRECTORY, output_file, options)

print(os.path.join(doughnut.BUILD_DIRECTORY, output_file))
