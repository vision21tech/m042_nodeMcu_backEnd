import os.path
from pathlib import Path
from flask import stream_with_context, request, Response, jsonify
from flask import Flask, make_response, send_file
from werkzeug.utils import secure_filename
from flask import after_this_request
from flask.views import MethodView
from utils import ResponseParam
from arduino import create_temp_project, ino_builder, nodemcu_builder, nodemcu_fbuilder
import base64
import shutil

app = Flask(__name__)


class BuildAPI(MethodView):
    init_every_request = False

    def get(self):

        return jsonify(ResponseParam("success", "TestGET", "HelloWorld").get_response()), 200

    def post(self):
        data = request.get_json()
        print(data)
        # print(data)
        a = create_temp_project(data['message'])

        if data['board_type'] == "uno":
            b = ino_builder(a)
        elif str(data['board_type']) == "nodemcu":
            b = nodemcu_builder(a)

        # try:
        #     if data['board_type'] == "uno":
        #         b = ino_builder(a)
        #     elif str(data['board_type']) == "nodemcu":
        #         b = nodemcu_builder(a)
        # except Exception as e:
        #     b = ino_builder(a)
        #     print(e)
        # print(b)
        return jsonify(ResponseParam("success", "TestPOST", str(b)).get_response()), 200


class testapi(MethodView):
    def get(self):
        data = {
            "board_type": "nodemcu",
            "message": "LyoKICBFU1A4MjY2IEJsaW5rIGJ5IFNpbW9uIFBldGVyCiAgQmxpbmsgdGhlIGJsdWUgTEVEIG9uIHRoZSBFU1AtMDEgbW9kdWxlCiAgVGhpcyBleGFtcGxlIGNvZGUgaXMgaW4gdGhlIHB1YmxpYyBkb21haW4KCiAgVGhlIGJsdWUgTEVEIG9uIHRoZSBFU1AtMDEgbW9kdWxlIGlzIGNvbm5lY3RlZCB0byBHUElPMQogICh3aGljaCBpcyBhbHNvIHRoZSBUWEQgcGluOyBzbyB3ZSBjYW5ub3QgdXNlIFNlcmlhbC5wcmludCgpIGF0IHRoZSBzYW1lIHRpbWUpCgogIE5vdGUgdGhhdCB0aGlzIHNrZXRjaCB1c2VzIExFRF9CVUlMVElOIHRvIGZpbmQgdGhlIHBpbiB3aXRoIHRoZSBpbnRlcm5hbCBMRUQKKi8KCnZvaWQgc2V0dXAoKSB7CiAgcGluTW9kZShMRURfQlVJTFRJTiwgT1VUUFVUKTsgIC8vIEluaXRpYWxpemUgdGhlIExFRF9CVUlMVElOIHBpbiBhcyBhbiBvdXRwdXQKfQoKLy8gdGhlIGxvb3AgZnVuY3Rpb24gcnVucyBvdmVyIGFuZCBvdmVyIGFnYWluIGZvcmV2ZXIKdm9pZCBsb29wKCkgewogIGRpZ2l0YWxXcml0ZShMRURfQlVJTFRJTiwgTE9XKTsgIC8vIFR1cm4gdGhlIExFRCBvbiAoTm90ZSB0aGF0IExPVyBpcyB0aGUgdm9sdGFnZSBsZXZlbAogIC8vIGJ1dCBhY3R1YWxseSB0aGUgTEVEIGlzIG9uOyB0aGlzIGlzIGJlY2F1c2UKICAvLyBpdCBpcyBhY3RpdmUgbG93IG9uIHRoZSBFU1AtMDEpCiAgZGVsYXkoMTAwMCk7ICAgICAgICAgICAgICAgICAgICAgIC8vIFdhaXQgZm9yIGEgc2Vjb25kCiAgZGlnaXRhbFdyaXRlKExFRF9CVUlMVElOLCBISUdIKTsgIC8vIFR1cm4gdGhlIExFRCBvZmYgYnkgbWFraW5nIHRoZSB2b2x0YWdlIEhJR0gKICBkZWxheSgyMDAwKTsgICAgICAgICAgICAgICAgICAgICAgLy8gV2FpdCBmb3IgdHdvIHNlY29uZHMgKHRvIGRlbW9uc3RyYXRlIHRoZSBhY3RpdmUgbG93IExFRCkKfQo="
        }
        a = create_temp_project(data['message'])
        if data['board_type'] == "uno":
            b = ino_builder(a)
        elif str(data['board_type']) == "nodemcu":
            path = nodemcu_fbuilder(a)
            @after_this_request
            def remove_file(response):
                try:
                    shutil.rmtree(Path(path).resolve().parent.parent.parent)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file handle", error)
                return response

            if os.path.isfile(path):
                return send_file(path, as_attachment=True)


        return jsonify(ResponseParam("success", "TestGET", "HelloWorld").get_response()), 200

    def post(self):
        data = request.get_json()
        # print(data)
        a = create_temp_project(data['message'])

        if data['board_type'] == "uno":
            b = ino_builder(a)
        elif str(data['board_type']) == "nodemcu":
            path = nodemcu_fbuilder(a)

            @after_this_request
            def remove_file(response):
                try:
                    shutil.rmtree(Path(path).resolve().parent.parent.parent)
                except Exception as error:
                    app.logger.error("Error removing or closing downloaded file handle", error)
                return response

            if os.path.isfile(path):
                return send_file(path, as_attachment=True)
            

        return jsonify(ResponseParam("success", "TestPOST", str(b)).get_response()), 200


app.add_url_rule(
    "/api/build", view_func=BuildAPI.as_view("build")
)
app.add_url_rule(
    "/api/test", view_func=testapi.as_view("testapi")
)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=os.environ.get('FLASK_DEBUG', 'False') == 'True')
