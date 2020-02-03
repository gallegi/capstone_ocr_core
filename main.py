from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
import json
from PIL import Image
import base64
import io
import numpy as np
from src.recognizer_master import RecognizerMaster
import tensorflow as tf
import traceback
import re
global recognizer_master
graph = tf.compat.v1.get_default_graph()
with graph.as_default():
    recognizer_master = RecognizerMaster()


class OcrHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers",
                        "authorization, Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With, Access-Control-Allow-Origin")
        self.set_header("Access-Control-Allow-Methods", "GET,PUT,POST,OPTIONS")

    def options(self):
        self.set_status(204)
        self.finish()

    def response(self, code, message):
        self.set_status(code)
        self.write(message)

    def post(self):
        try:
            global recognizer_master
            with graph.as_default():
                request_data = json.loads(self.request.body.decode())
                image_input = request_data['image']

                with open('log.txt', 'a') as f:
                    f.write(image_input + '\n')

                pattern = 'data:image\/[^;]+;base64,'
                base64_str = re.sub(pattern, '', image_input)

                base64_decoded = base64.b64decode(base64_str)
                image = Image.open(io.BytesIO(base64_decoded))
                image_np = np.array(image)
                result = recognizer_master.recognizer_image(image_np)
                self.set_status(200)
                self.write(result)
        except:
            print(traceback.format_exc())
            self.response(500, {"message": "Internal server error!"})


def make_app():
    routes = [('/api/ocr/ocr_cmnd', OcrHandler)]
    return Application(routes)


if __name__ == '__main__':
    app = make_app()
    print('Start serving')
    app.listen(3100)
    IOLoop.current().start()
