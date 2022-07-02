from waitress import serve
import app

import os
HOST = os.environ.get('SERVER_HOST', 'localhost')
try:
    PORT = int(os.environ.get('SERVER_PORT', '5555'))
except ValueError:
    PORT = 5555

print("Starting server...")
serve(app.app, host=HOST, port=PORT)