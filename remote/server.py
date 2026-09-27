import sys
import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from brain import Brain

brain = Brain()

HOST = "0.0.0.0"
PORT = 8765


class AvanHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):

        response = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json"
        )
        self.send_header(
            "Content-Length",
            str(len(response))
        )
        self.end_headers()

        self.wfile.write(response)

    def do_GET(self):

        if self.path == "/":

            self.send_json({
                "status": "online",
                "assistant": "Avan"
            })

            return

        self.send_json({
            "error": "Not found"
        }, 404)

    def do_POST(self):

        if self.path != "/command":

            self.send_json({
                "error": "Not found"
            }, 404)

            return

        try:

            length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = self.rfile.read(length)

            data = json.loads(
                body.decode("utf-8")
            )

            command = data.get(
                "command",
                ""
            ).strip()

            if not command:

                self.send_json({
                    "error": "Command is empty"
                }, 400)

                return

            print(
                f"\n📱 Remote command: {command}"
            )

            answer = brain.think(command)

            print(
                f"🤖 Avan response: {answer}"
            )

            self.send_json({
                "status": "success",
                "command": command,
                "response": answer
            })

        except Exception as e:

            print(
                f"❌ Remote error: {e}"
            )

            self.send_json({
                "status": "error",
                "error": str(e)
            }, 500)


def start_server():

    server = HTTPServer(
        (HOST, PORT),
        AvanHandler
    )

    print("=" * 45)
    print("📡 AVAN REMOTE SERVER")
    print("=" * 45)
    print(
        f"🟢 Server running on port {PORT}"
    )
    print(
        "📱 Waiting for remote commands..."
    )
    print("=" * 45)

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\n🛑 Remote server stopped."
        )

        server.server_close()


if __name__ == "__main__":
    start_server()