from flask import Flask, send_file, request, abort
import html
import random

# VARIABLES
# If empty string then it will be disabled
file_location = ""
text_copy = ""
#PASSWORD, True or False, password is a string
is_PASSWORD = True
password = "" # If left blank a 4 digit password will be generated

if is_PASSWORD and not password:
    password = f"{str(round(random.randint(0, 9999))):0>4}"

def is_file_location():
    if file_location.strip():
        return """
    <legend>Attachment: </legend>
    <div class="codeSnippet" onclick="window.open('file', '_blank');">
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
            return ""

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
            var text = document.getElementById("code").innerHTML;
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

if __name__ == "__main__":
    if is_PASSWORD:
        print(f"Password is: {password}")
    app.run(host="0.0.0.0", port=8000, ssl_context="adhoc")