from flask import Flask, jsonify
from api.scanbarcode import scanbarcode_api
# from api.ocr_reader import ocr_reader_api
from config import ConFig
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

arg = ConFig()

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y")

if not os.path.exists('Logs'):
    try:
        os.mkdir('Logs')
    except Exception as err:
        print(err)

def configure_logging():
    # register root logging
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = TimedRotatingFileHandler('Logs/' + dt_string + '.log', when="midnight", interval=1, encoding='utf8')
    handler.suffix = "%d-%m-%Y"
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

app = Flask(__name__)
if arg.LOGGING:
    configure_logging()

app.config['MAX_CONTENT_LENGTH'] = arg.MAX_CONTENT_LENGTH

app.register_blueprint(scanbarcode_api)

if arg.IS_ONNX_MODEL:
    from api.scanproduct_onnx import scanproduct_onnx_api
    app.register_blueprint(scanproduct_onnx_api)

if arg.IS_TENSORFLOW_MODEL:
    from api.scanproduct import scanproduct_api
    app.register_blueprint(scanproduct_api)

# app.register_blueprint(ocr_reader_api)

@app.route('/test')
def test():
    return jsonify({'message': 'api scanner connected'}), 200


if __name__=='__main__':
    app.run(host=os.getenv('IP', arg.HOST), port=int(os.getenv('POST',arg.PORT)), debug=arg.DEBUG)