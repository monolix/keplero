from v1 import app
from os import environ

if __name__ == "__main__":
    if environ.get("PRODUCTION") == "true":
        app.run(port=8000)
    else:
        app.run(
            port=8000,
            debug=True
        )
