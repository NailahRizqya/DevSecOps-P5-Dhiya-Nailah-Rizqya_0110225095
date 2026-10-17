"""Entry point: jalankan dengan `SECURENOTES_SECRET=... python run.py`."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    # Debug dimatikan agar tidak membuka Werkzeug debugger (risiko RCE).
    app.run(host="127.0.0.1", port=5000, debug=False)
