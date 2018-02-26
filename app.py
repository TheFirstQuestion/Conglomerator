from flask import *
from flask_dropzone import Dropzone
import sqlite3
import subprocess
import uuid
from subprocess import call


app = Flask(__name__)
myWD = "/home/sophie/GitHub/Conglomerator/files"


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
                f.save(os.path.join(myWD, newName))
    return "something"

def convert(myFile):
    extension = myFile[4]
    name = myFile[2]
    filename = "{}{}".format(name, extension)
    #os.chdir(myWD)

    # PDF
    if (extension == ".pdf"):
        cmd = ['docker', 'run', '-ti', '--rm', '-v', '/homt/sophie/GitHub/Conglomerator/files:/pdf'.format(myWD), 'bwits/pdf2htmlex' 'pdf2htmlEX', filename]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in p.stdout:
            print(line)
        p.wait()
        print(p.returncode)
    # Markdown
    elif (extension == ".md"):
        call(["grip", filename, "--export"])
    # Text
    elif (extension == ".txt"):
        contents = open("{}/{}".format(myWD, filename),"r")
        with open("{}.html".format(name), "w") as e:
            for lines in contents.readlines():
                e.write("<pre>" + lines + "</pre>\n")
    else:
        # Primarily DOCX and DOC
        call(["libreoffice", "--headless", "--convert-to", "html", filename])


@app.route('/showFile/<fileCode>')
def showFile(fileCode):
    filePath = "{}/{}.html".format(myWD, fileCode)
    return send_file(filePath)



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
    # TODO: check for duplicates, clean up input (lowercase, etc.)
    conn.execute('INSERT INTO `files` (`originalName`, `parsedType`, `systemName`, `systemType`) VALUES (?, ?, ?, ?);', [name, extension, newName, fType])
    conn.commit()
    # Return random name with same file extension
    return "{}{}".format(newName, extension)







if __name__ == "__main__":
    app.run(host='0.0.0.0')
