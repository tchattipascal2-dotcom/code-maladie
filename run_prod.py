from waitress import serve
import os
from app import app

port = int(os.environ.get("PORT", 5000))
serve(app, host="0.0.0.0", port=port)
