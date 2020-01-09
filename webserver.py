from library import build
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from urllib.parse import urlparse, parse_qs
import simplejson as json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')



    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()

        q = parse_qs(body)
        data = []
        for k, v in q.items():
            if k.decode("utf-8") == "full_image":
                full_image = v[0].decode("utf-8")
            elif k.decode("utf-8") == "image_partial":
                image_partial = v[0].decode("utf-8")


        if len(full_image) > 5 and len(image_partial):
            test_2 = build(full_image, image_partial)
            test = json.dumps({"x": str(test_2[0]), "y": str(test_2[1])}, sort_keys=True)

        response = BytesIO()
        response.write(test.encode())
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()



