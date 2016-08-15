import os
import uuid
from doughnut import settings
from doughnut.doughnut import Doughnut
from flask import Blueprint, send_from_directory, request, redirect, url_for, abort
from werkzeug import secure_filename
from jsonschema import ValidationError
from doughnut.exceptions import InvalidSource

frontend = Blueprint('frontend', __name__, static_folder=settings.STATIC_DIRECTORY)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['zip'])
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def makeHTML(title, body):
    return "<html><head><title>{title} - Doughnut</title></head><body>{body}</body></html>".format(title=title, body=body)

@frontend.route('assets/<path:asset>')
def assets(asset):
    if os.path.exists(os.path.join(settings.STATIC_DIRECTORY, 'assets', asset)):
        return frontend.send_static_file(os.path.join('assets', asset))
    else:
        abort(404)

@frontend.route('/', defaults={'page': 'index.html'})
@frontend.route('<page>')
def show(page):
    if os.path.exists(os.path.join(settings.STATIC_DIRECTORY, page)):
        return frontend.send_static_file(page)
    else:
        abort(404)

@frontend.route('make/doughnut.pdf', methods=['POST'])
def make_pdf():
    file = request.files['file']
    if file and allowed_file(file.filename):
        if not os.path.exists(settings.UPLOAD_DIRECTORY):
            os.makedirs(settings.UPLOAD_DIRECTORY)

        filename = secure_filename(file.filename)
        zip_path = os.path.join(settings.UPLOAD_DIRECTORY, str(uuid.uuid4()))
        zip_path = "{path}.zip".format(path=zip_path)
        file.save(zip_path)

        build_directory = os.path.join(settings.BUILD_DIRECTORY, str(uuid.uuid4()))
        output_file = "doughnut.pdf"

        d = Doughnut(zip_path, build_directory, output_file)

        try:
            d.build()
        except ValidationError as e:
            return makeHTML("doughnut.json file error", "ERROR: Check your <b>doughnut.json</b> file for following errors:<br><br>%s<br><br>Use <a href='http://jsonschemalint.com/' target='_blank'>JSONSchemaLint</a> for JSONSchema validation against doughnut.json's schema available <a href='/schema.json'>here</a>" % e)
        except IOError as e:
            return makeHTML("Error", "ERROR: PDF Generation failed due to following error: %s" % e)
        except InvalidSource as e:
            return makeHTML("Error", "ERROR: %s" % e.value)
        except KeyError as e:
            return makeHTML("Error", "ERROR: %s" % e)
        return send_from_directory(directory=build_directory, filename=output_file)
    else:
        return makeHTML("Invalid input", "Upload valid <b>ZIP</b> archive with valid <b>%s</b> configuration file in it" % settings.CONFIG_FILE_NAME)

@frontend.route('test_data')
def test_data():
    return send_from_directory(directory=settings.STATIC_DIRECTORY, filename="test_data.zip", as_attachment=True)
