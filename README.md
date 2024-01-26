# Web-File-Sharing
This is a python flask app that can share files and text using the https protocol. This uses the flask adhoc certificate so you will have to install pyopenssl. The point of having this and not using the alternatives like airdrop or nearby share which have not been adopted universally, we decided to use the http protocol which is already widespread. By default the flask app is using https because if  you don't then copying to the clipboard is not allowed, this also mean that the site can only be access using `https://`.

***This program might fail if a VPN is used***

1. Install the dependencies
   run `pip install flask ; pip install html ; pip install pyopenssl ; pip install "qrcode[pil]" ; pip install termcolor ; pip install psutil` Note that you might have problems installing `html`, but chances are that the problem is not related to it, test to programm before troubleshooting `pip install html`.
2. Go to the file named webFileShare.py and change the variables `file_location` and `text_copy` to what they correspond.
   * `file_location`: the directory starting from where the file is run until the file you want to share.
   * `text_copy`: the text you want them to recieve or copy.
   * Remember to keep in mind if one of them is left empty they will not show up to the user.
   * `is_PASSWORD`: set this to `True` if you want passwords enabled, if no password is specified then a integer from 0 to 9999 is assigned.
   * `password`: This variable is the passowrd you want to assign, if it is empty then a random one is assigned.
3. Run the webFileShare.py file using python3, for example `python3 webFileShare`
   * The terminal will output modified flask interface, look for the link and share this url with the person you want to share with, you can enter the link and you will see a qrcode to share.
   * Don't forget to share the password if enabled, if you do share the password add it as a parameter in the url, for example `localhost:8000?p=9999`, but if you use the qrcode the password is pre-inputed.

