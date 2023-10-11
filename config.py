# config.py

class ConFig(object):
    HOST = "0.0.0.0"
    PORT = "9085"
    DEBUG = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    LOGGING = False
    # PATH_DIRECTORY_LOCAL = '/app/www/vhosts/chat.cosmenet.in.th/httpdocs-chat-web/'
    # PATH_DIRECTORY_LOCAL_BACKEND = '/app/www/vhosts/cosmenet.in.th/httpdocs-backend/'

    # PATH_DIRECTORY_LOCAL = '/Users/nawaphongyoochum/Work-TNT/Cosmenet/scanner/'
    PATH_DIRECTORY_LOCAL = '/Users/nawaphongyoochum/Work-TNT/Cosmenet/insert2es/'
    # PATH_DIRECTORY_LOCAL_BACKEND = '/Users/nawaphongyoochum/Work-TNT/Cosmenet/scanner/'
    PATH_DIRECTORY_LOCAL_BACKEND = '/Users/nawaphongyoochum/Work-TNT/Cosmenet/data_image'


    PATH_DIRECTORY_LOCAL_UAT = '/app/www/vhosts/cosmenet.in.th/httpdocs-chat-new/httpdocs-chat-web/'

    PATH_ONNX_EMBEDDED = './models/model.onnx'
    PATH_ONNX_YOLOV7 = './models/yolov7-cosme.onnx'
    DETECTION_THRESHOLD = 0.9
    IS_ONNX_MODEL = True
    IS_TENSORFLOW_MODEL = False
