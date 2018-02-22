# Conglomerator

`make clean && make run`

## Dependencies

* Flask: `sudo pip3 install flask`
* Flask-Dropzone: `sudo pip3 install flask-dropzone`

### For file conversions:

#### [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX) for PDF
* Install [Docker](https://www.docker.com/community-edition#/download)
* Create a local alias for docker command: add the following to `~/.bash_aliases`
        alias pdf2htmlEX='sudo docker run -ti --rm -v `pwd`:/pdf bwits/pdf2htmlex pdf2htmlEX'
* Test: `pdf2htmlEX "test.pdf"`

#### [mammoth](https://github.com/mwilliamson/python-mammoth) for DOCX
* `sudo pip3 install mammoth`
* `mammoth test.docx output.html`

#### [grip](https://github.com/joeyespo/grip) for Markdown
* `sudo pip3 install grip`
* `grip test.md --export`

#### [LibreOffice](https://www.libreoffice.org/) for DOC
* `sudo apt-get install libreoffice --no-install-recommends` (see [here](https://askubuntu.com/questions/519082/how-to-install-libre-office-without-gui))
* `libreoffice --headless --convert-to html test.doc`
