from flask import Flask, render_template,redirect, url_for, request
from werkzeug import secure_filename

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/file")
def fileR():
    return render_template('file.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='images/favicon.ico'), code=302)


########################### Backend #########################

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files")
        for f in uploaded_files:
            f.save("./files/" + secure_filename(f.filename))
    return redirect('/file')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
