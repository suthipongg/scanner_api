from flask import Flask, jsonify
from api.scanbarcode import scanbarcode_api
from config import ConFig
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y")

if not os.path.exists('Logs'):
    try:
        os.mkdir('Logs')
    except Exception as err:
        logging.error(err)


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
if ConFig.LOGGING:
    configure_logging()

app.config['MAX_CONTENT_LENGTH'] = ConFig.MAX_CONTENT_LENGTH

app.register_blueprint(scanbarcode_api)

if ConFig.IS_ONNX_MODEL:
    from api.scanproduct_onnx_v3 import scanproduct_onnx_v3_api
    app.register_blueprint(scanproduct_onnx_v3_api)

@app.route('/test')
def test():
    return jsonify({'message': 'api scanner connected'}), 200


if __name__=='__main__':
    app.run(host=os.getenv('IP', ConFig.HOST), 
            port=int(os.getenv('POST',ConFig.PORT)), 
            debug=ConFig.DEBUG)