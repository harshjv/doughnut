import os
import pdfkit

class PDFGenerator:
    def __init__(self, build_directory, output_file, options):
        self.build_directory = build_directory
        self.output_file = output_file
        self.options = options

    def generate(self):
        pdfkit.from_file(os.path.join(self.build_directory, "index.html"), os.path.join(self.build_directory, self.output_file), options=self.options)
