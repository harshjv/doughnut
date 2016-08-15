import os
import uuid
from doughnut import settings
from doughnut.configuration import Configuration
from doughnut.template import Template
from doughnut.pdf_generator import PDFGenerator
from doughnut.read_source import ReadSource

class Doughnut:
    def __init__(self, source, build_directory, output_file):
        self.source = source
        self.build_directory = build_directory
        self.output_file = output_file

    def build(self):
        pdf_options = settings.PDF_OPTIONS

        pdf_options['header-html'] = os.path.join(self.build_directory, "header.html")
        pdf_options['footer-html'] = os.path.join(self.build_directory, "footer.html")

        source = ReadSource(self.source)
        config = Configuration(source).read()

        try:
            if config['title']:
                pdf_options['title'] = config['title']

            if config['page-starts-from-index']:
                if config['page-starts-from-index'] > 1:
                    pdf_options['page-offset'] = config['page-starts-from-index'] - 1
        except KeyError:
            print("KeyError: Skipping")

        template = Template(config, source, self.build_directory)
        template.register()
        template.buildAll()

        pdf_generator = PDFGenerator(self.build_directory, self.output_file, pdf_options)
        pdf_generator.generate()
