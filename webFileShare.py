"""
Copyright (c) 2023 Baldwin Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from flask import Flask, send_file, request, abort, jsonify
import html
import random
import qrcode
import psutil
import urllib.parse
from io import BytesIO
from termcolor import colored
import os.path
from werkzeug.utils import secure_filename
import logging

# VARIABLES
# If empty string then it will be disabled
file_location = "webFileShare.py"
text_copy = "Test"
#PASSWORD, True or False, password is a string
is_PASSWORD = True
password = ""  # If left blank a 6 digit password will be generated
# Hosting configuration
HOST = ""
for i in [addr.address for interface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == 2]:
            if i != "127.0.0.1":
                HOST = i
PORT = 8000

if HOST == "":
    raise("No host found, please check for a wifi connection, if none can be found try with you own wifi hotspot.")

if is_PASSWORD and not password:
    password = f"{str(round(random.randint(0, 999999))):0>6}"

if not is_PASSWORD:
    print(colored("##################################################", "cyan"))
    print(colored("Use this link to enter and share: ", "blue") + colored(f"https://{HOST}:{str(PORT)}/", "red"))
    print(colored("##################################################", "cyan"))

def is_file_location():
    if file_location.strip():
        return f"""
    <legend>Attachment: </legend>
    <div class="codeSnippet" onclick="window.open('file?p={urllib.parse.quote(password)}', '_blank');">
        <code>Download file</code>
    </div>
"""
    else:
        return ""
def is_text_copy():
    if text_copy.strip():
        return """
    <legend>Text (Click to copy): </legend>
    <div id="codeSnippet" class="codeSnippet" onclick="myFunction()">
        <code id="code">""" + html.escape(text_copy) + """
        </code>
        <span class="tooltiptext">Copy text</span>
    </div>
"""
    else:
        return ""
def is_hr():
    if file_location.strip() == "" or text_copy.strip() == "":
        return ""
    else:
        return "<hr></hr>"
    
def is_empty():
    if file_location.strip() == "" and text_copy.strip() == "":
        return "<h1 style='text-align: center; color: #fff;'>Looks like nothing has been shared with you :(</h1><img src='https://media.tenor.com/9zmtHZ0tIjkAAAAi/nyancat-rainbow-cat.gif' width=300 style='display: block; margin-left: auto; margin-right: auto; width: 50%; max-width: 500px; margin-top: 200px'>"
    else:
        return f"<legend style='margin-top: 100px'>Share it with others (Scan):</legend><img src='/qrcode?p={urllib.parse.quote(password)}' width=300 style='display: block; margin: 8px;margin-left: auto; margin-right: auto; width: 70%; max-width: 400px;'>"

app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True

@app.route("/")
def index():
    if is_PASSWORD and request.args.get("p") != password:
        abort(403)
    return """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: monospace;
            font-weight: 400;
            background-color: #21262d;
        }
        .codeSnippet {
            background-color: #202531;
            margin: 8px;
            padding: 15px;
            border: solid 6.4px #353c4c;
        }
        .tooltiptext {
            visibility: hidden;
            color: aqua;
        }
        .codeSnippet:hover{
            background-color: #353c4c;
        }
        .codeSnippet:hover > .tooltiptext{
            visibility: visible;
        }
        code, legend {
            color: #fff;
            text-align: center;
        }
        a {
            color: #fff;
        }
        button {
            width: 25.5px;
            height: 25.5px;
            text-align: center;
        }
        svg {
            display: flex;
            justify-content: center;
            align-items: center;
        }
    </style>
</head>
<body> """ + is_file_location() + """ """ + is_hr() + """ """ + is_text_copy() + """ """ + is_empty() + """
    <script>
        function myFunction() {
            var text = document.querySelector("#code").textContent;
            navigator.clipboard.writeText(text).then(function() {
                alert("Copied the text: " + text);
            });
            
        }
    </script>
    <footer style="position: fixed; bottom: 0; border: 2px solid #21262d; background-color: #21262d;">
        <code>Share a file <a href='/submit?p=""" + urllib.parse.quote(password) + """'>here</a>, or download a copy of the software <a href="https://github.com/Baldwinplayz/Web-File-Sharing">here</a></code>
    </footer>
</body>
</html>
"""

@app.route("/file")
def file():
    if is_PASSWORD and request.args.get("p") != password:
        abort(403)
    return send_file(file_location, as_attachment=True)

@app.route("/text")
def text():
    if is_PASSWORD and request.args.get("p") != password:
        abort(403)
    return text_copy

@app.route("/qrcode")
def qrcode_img():
    if is_PASSWORD and request.args.get("p") != password:
        abort(403)
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(f"https://{HOST}:{str(PORT)}/?p={urllib.parse.quote(password)}")
    qr.make(fit=True)
    img = qr.make_image()

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

@app.route("/submit")
def submit():
     if is_PASSWORD and request.args.get("p") != password:
        abort(403)
     return """
<html data-lt-installed="true">
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {
                font-family: monospace;
                font-weight: 400;
                background-color: #21262d;
            }
            .codeSnippet {
                background-color: #202531;
                margin: 8px;
                padding: 15px;
                border: solid 6.4px #353c4c;
                color: #fff;
            }
            .codeSnippet:hover{
                background-color: #353c4c;
            }
            code, legend {
                color: #fff;
            }
            a {
                color: #fff;
            }
            button {
                width: 25.5px;
                height: 25.5px;
                text-align: center;
            }
            svg {
                display: flex;
                justify-content: center;
                align-items: center;
            }
            .textarea {
                display: block;
                color: #fff;
                background-color: #202531;
                width: 100%;
                height: auto;
                resize: vertical;
                overflow: auto;
            }
            .textarea:hover {
                background-color: #353c4c;
            }
        </style>
    </head>
    <body> 
        <legend>Submit Attachment: </legend>
        <form action="/submitFile" method="post" enctype="multipart/form-data">
            <div class="codeSnippet" id="parentBox" style="display: flex;">
                <input style="display: none;" type="file" name="submited-file" id="submitFile" multiple="">
                </input>
                <p style="color: #fff; margin: 0; width: 50%;">Submit File</p>
                <p id="selectedFiles" style="color: aqua; margin: 0; text-align: right; width: 50%;"></p>
            </div>
        </form>
        <script>
            var submitFile = document.querySelector("#submitFile");
            var parentBox = document.querySelector("#parentBox");
            var selectedFiles = document.querySelector("#selectedFiles");
            
            submitFile.onchange = function() {

                var files = submitFile.files;

                switch (files.length) {
                    case 1:
                    selectedFiles.textContent = files[0]["name"];
                    break;

                    default:
                    selectedFiles.textContent = `${files[0]["name"]} & another ${files.length - 1}`;
                }
            }

            parentBox.addEventListener("click", function() {
                submitFile.click();
            });
        </script>
        <hr> 
        <legend>Submit Text: </legend>
        <div id="codeSnippet" class="codeSnippet" contentEditable="" spellcheck="false"></div>
        <hr>
        <div id="codeSnippet" class="codeSnippet" style="margin-top: 15px;" onclick="submit()">
            <p style="text-align: center; margin: 0; color: #fff;">Submit!!!</p>
        </div>
        <script>
            function submit() {
                var submitFile = document.querySelector("#submitFile");
                var text = document.getElementById("codeSnippet");
                if (submitFile.files.length > 0) {
                    const formData = new FormData();
                    for (const file of submitFile.files) {
                        formData.append('file', file, file.name);
                    }

                    fetch('/submitFile?p=""" + urllib.parse.quote(password) + """', {
                        method: 'POST',
                        body: formData
                        }).then(response => response.json()).then(data => {
                    console.log(data);
                    }).catch(error => {
                    console.error('Error:', error);
                    });
                }
                if (text.textContent.length > 0) {
                    fetch('/submitText?p=""" + urllib.parse.quote(password) + """', {
                        method: 'POST',
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({"text": text.textContent})
                        }).then(response => response.json()).then(data => {
                    console.log(data);
                    }).catch(error => {
                    console.error('Error:', error);
                    });
                }
                alert("Form Submited!!!");
            }
        </script>
        <footer style="position: fixed; bottom: 0; border: 2px solid #21262d; background-color: #21262d;">
            <code>Go back <a href='/?p=""" + urllib.parse.quote(password) + """'>here</a>, or download a copy of the software <a href="https://github.com/Baldwinplayz/Web-File-Sharing">here</a></code>
        </footer>
    </body>
</html>
"""


@app.route('/submitFile', methods=["GET", "POST"])
def submit_file():
    if is_PASSWORD and request.args.get("p") != password:
        abort(403)
    files = next(request.files.lists())[1]
    for thing in files:
        consent = input(colored(f"Save {thing} from {colored(request.remote_addr, 'red')}, {colored('[y/n]', 'green')}", 'blue')).lower()
        print()
        if consent == "y":
            filename = secure_filename(thing.filename)
            thing.save(os.path.join(os.getcwd(), filename))
    return jsonify({"status": "sent"})

@app.route('/submitText', methods=["GET", "POST"])
def submit_text():
    if is_PASSWORD and request.args.get("p") != password:
        abort(403)
    try:
        if input(colored(f"Print {len(request.json['text'])} characters from {colored(request.remote_addr, 'red')}, {colored('[y/n]', 'green')}", 'blue')).lower() == "y":
            print(request.json["text"])
            print()
        else:
            print(colored("Cancelled", "green"))
    except:
         abort(400)
    return jsonify({"status": "sent"})


if __name__ == "__main__":
    if is_PASSWORD:
        print(colored("##################################################", "cyan"))
        print(colored(f"Password is: {password}", "green"))
        print(colored("Use this link with the password pre inputed: ", "blue") + colored(f"https://{HOST}:{str(PORT)}/?p={urllib.parse.quote(password)}", "red"))
        print(colored("##################################################", "cyan"))
    app.run(host=HOST, port=PORT, ssl_context="adhoc")
