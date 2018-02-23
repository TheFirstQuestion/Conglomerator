from flask import *
from flask_dropzone import Dropzone
import sqlite3
import os
import uuid
from subprocess import call


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

@app.route("/file")
def viewFile():
    myFile = request.args.get('file', None)
    # Pass full file data to page
    myFile = getFile(myFile)[0]
    # Do the conversion of the file so it will be available
    convert(myFile)
    return render_template("viewFile.html", data=myFile)

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'), code=302)




########################### Backend #########################
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        for key, f in request.files.items():
            if key.startswith('file'):
                newName = fileToDB(f)
                f.save(os.path.join("./files/", newName))
    return "something"

def convert(myFile):
    extension = myFile[4]
    name = myFile[2]
    filename = "{}{}".format(name, extension)
    os.chdir("/home/sophie/GitHub/Conglomerator/files")

    if (extension == ".pdf"):
        print("PDF")
        call(["sudo", "pdf2htmlEX", filename])
    elif (extension == ".md"):
        print("markdown")
        call(["grip", filename, "--export"])

@app.route('/maps/map.html')
def showFile():
    return send_file('/home/sophie/GitHub/Conglomerator/files/1c8b3bfb1ebf4887bff8f80db1015174.html')



########################## Database #########################
conn = sqlite3.connect('conglomerator.db')

def getAllFromDb():
    # TODO: for the user
    return conn.execute('SELECT * FROM files').fetchall()

def getFile(systemName):
    return conn.execute('SELECT * FROM files WHERE `systemName` IS (?)', (systemName,)).fetchall()

def fileToDB(f):
    fullName = f.filename
    name = os.path.splitext(fullName)[0]
    fType = f.content_type
    # Generate random filename
    newName = uuid.uuid4().hex
    extension = os.path.splitext(fullName)[1]
    # TODO: check for duplicates
    conn.execute('INSERT INTO `files` (`originalName`, `parsedType`, `systemName`, `systemType`) VALUES (?, ?, ?, ?);', [name, extension, newName, fType])
    conn.commit()
    # Return random name with same file extension
    return "{}{}".format(newName, extension)







if __name__ == "__main__":
    app.run(host='0.0.0.0')
