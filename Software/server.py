import os

import werkzeug.utils
from flask import *
from main import run

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    file = request.files['file']
    filename = werkzeug.utils.secure_filename(file.filename)
    print("\nReceived: " + filename)
    file.save("./Input/" + filename)
    run("./Input/" + filename)
    os.remove("./Input/" + filename)
    return send_file("./Result/output.mid", mimetype="audio/midi")


app.run(host="0.0.0.0", port=5000, debug=True)
