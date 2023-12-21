from flask import Flask, send_file, request, abort
import html
import random
import qrcode
import psutil
import urllib.parse
from io import BytesIO
from termcolor import colored

# VARIABLES
# If empty string then it will be disabled
file_location = "webFileShare.py"
text_copy = "Hello world! Special Characters >>> !@#$%^&*()_+-={}:\"<<?:\\"
#PASSWORD, True or False, password is a string
is_PASSWORD = True
password = "" # If left blank a 4 digit password will be generated

# Hosting configuration
HOST = "0.0.0.0" # Just in case no host is found, if no host is found then you can not use qr codes
for i in [addr.address for interface, addrs in psutil.net_if_addrs().items() for addr in addrs if addr.family == 2]:
            if i != "127.0.0.1":
                HOST = i
PORT = 8000

if is_PASSWORD and not password:
    password = f"{str(round(random.randint(0, 9999))):0>4}"

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
    img.save(buffer, format='PNG')
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')

if __name__ == "__main__":
    if is_PASSWORD:
        print(colored("##################################################", "cyan"))
        print(colored(f"Password is: {password}", "green"))
        print(colored("User this link with the password pre inputed: ", "blue") + colored(f"https://{HOST}:{str(PORT)}/?p={urllib.parse.quote(password)}", "red"))
        print(colored("##################################################\n", "cyan"))
    app.run(host=HOST, port=PORT, ssl_context="adhoc")