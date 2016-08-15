import argparse

class ArgumentParser():
    def __init__(self, config_file_name):
        parser = argparse.ArgumentParser(description='Doughnut: Source Code Documenter')
        parser.add_argument('source_directory', metavar='s', type=str, nargs=1,
                           help='path of source directory with {config_file_name} file'.format(config_file_name=config_file_name))
        parser.add_argument('output', metavar='o', type=str, nargs=1,
                           help='output pdf file name with .pdf extension')

        args = parser.parse_args()

        self.source_directory = args.source_directory[0]
        self.output_file = args.output[0]


    def getSourceDirectory(self):
        return self.source_directory

    def getOutputFile(self):
        return self.output_file
