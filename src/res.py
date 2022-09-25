import io
import os
import zipfile


authdatafile = os.path.join(os.getenv("HOME"), ".reddit-token")
zip = os.path.dirname(__file__)


def auth_data():
    try:
        with io.open(authdatafile, "r") as f:
            return f.read()
    except (IOError, ValueError, FileNotFoundError):
        return None


def write_auth_data(data):
    with io.open(authdatafile, "w") as f:
        f.write(data)


def get_icon():
    with zipfile.ZipFile(zip, "r") as zf:
        return zf.read("res/icon.png")

