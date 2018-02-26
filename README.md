# Conglomerator

`make clean && make run`

## Dependencies

* Flask: `sudo pip3 install flask`
* Flask-Dropzone: `sudo pip3 install flask-dropzone`

### For file conversions:

#### [pdf2htmlEX](https://github.com/coolwanglu/pdf2htmlEX) for PDF
* Install [Docker](https://www.docker.com/community-edition#/download) and [allow running without `sudo`](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)
* Create a local alias for docker command: add the following to `~/.bash_aliases`
        alias pdf2htmlEX='docker run -ti --rm -v "${PWD}":/pdf bwits/pdf2htmlex pdf2htmlEX'
* Test: `pdf2htmlEX "test.pdf"`

#### [grip](https://github.com/joeyespo/grip) for Markdown
* `sudo pip3 install grip`
* Test: `grip test.md --export`

#### [LibreOffice](https://www.libreoffice.org/) for DOC and DOCX
* `sudo apt-get install libreoffice --no-install-recommends` (see [here](https://askubuntu.com/questions/519082/how-to-install-libre-office-without-gui))
* Test: `libreoffice --headless --convert-to html test.doc`
