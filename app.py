from flask import Flask, render_template,redirect, url_for, request
from flask_dropzone import Dropzone
import sqlite3
import os

app = Flask(__name__)

########################## Dropzone Config ##################################
dropzone = Dropzone(app)
# Enable parallel uploads
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
# Number of files handleded per request
app.config['DROPZONE_PARALLEL_UPLOADS'] = 3
# Custom file types
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.doc, .docx, .html, .md, .pdf, .txt'





################################# Routes #####################################

@app.route("/")
def main():
    return render_template('index.html', data=getAllFromDb())

@app.route("/upload")
def upload():
    return render_template("upload.html")

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'), code=302)




########################### Backend #########################
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                fileToDB(f)
                # TODO: randomly generate filename https://stackoverflow.com/questions/2961509/python-how-to-create-a-unique-file-name/44992275#44992275
                f.save(os.path.join("./files/", f.filename))
    return "something"




########################## Database #########################
conn = sqlite3.connect('conglomerator.db')

def getAllFromDb():
    # TODO: for the user
    return conn.execute('SELECT * FROM files').fetchall();

def fileToDB(f):
    name = f.filename
    fType = f.content_type
    # TODO: check for duplicates
    conn.execute('INSERT INTO `files` (`name`, `type`) VALUES (?, ?);', [name, fType])
    conn.commit()







if __name__ == "__main__":
    app.run(host='0.0.0.0')
