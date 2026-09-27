# avan_status_server.py

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Lock


HOST = "127.0.0.1"
PORT = 8765


_state = {
    "status": "OFFLINE",
    "last_command": "",
    "modules": {
        "BRAIN": False,
        "MEMORY": False,
        "VISION": False,
        "SYSTEM": False,
        "SKILLS": False,
    },
}

_lock = Lock()


class AvanStatusHandler(BaseHTTPRequestHandler):

    def _send_json(self, data, status=200):

        body = json.dumps(data).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.end_headers()

        self.wfile.write(body)


    def do_GET(self):

        if self.path == "/status":

            with _lock:
                data = dict(_state)

                data["modules"] = dict(
                    _state["modules"]
                )

            self._send_json(data)

            return


        if self.path == "/health":

            self._send_json({
                "online": True,
                "service": "Avan Status Server"
            })

            return


        self._send_json({
            "error": "Not Found"
        }, 404)


    def do_POST(self):

        if self.path != "/status":

            self._send_json({
                "error": "Not Found"
            }, 404)

            return


        try:

            length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            raw_data = self.rfile.read(length)

            data = json.loads(
                raw_data.decode("utf-8")
            )

            with _lock:

                if "status" in data:

                    _state["status"] = str(
                        data["status"]
                    ).upper()


                if "last_command" in data:

                    _state["last_command"] = str(
                        data["last_command"]
                    )


                if "modules" in data:

                    for name, value in data["modules"].items():

                        name = str(name).upper()

                        if name in _state["modules"]:

                            _state["modules"][name] = bool(
                                value
                            )


            self._send_json({
                "success": True
            })


        except Exception as e:

            self._send_json({
                "success": False,
                "error": str(e)
            }, 400)


    def log_message(self, format, *args):

        # HTTP request logs hide kar rahe hain
        return


def start_server():

    server = HTTPServer(
        (HOST, PORT),
        AvanStatusHandler
    )

    print("=" * 45)
    print("        AVAN STATUS SERVER")
    print("=" * 45)

    print(
        f"Server running on "
        f"http://{HOST}:{PORT}"
    )

    print(
        "Status endpoint:"
        f" http://{HOST}:{PORT}/status"
    )

    print(
        "Health endpoint:"
        f" http://{HOST}:{PORT}/health"
    )

    print("=" * 45)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print("\n🛑 Avan Status Server stopped.")

    finally:

        server.server_close()


if __name__ == "__main__":

    start_server()