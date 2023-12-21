# Web-File-Sharing
This is a python flask app that can share files and text using the https protocol. This uses the flask adhoc certificate so you will have to install pyopenssl. The point of having this and not using the alternatives like airdrop or nearby share which have not been adopted universally, we decided to use the http protocol which is already widespread. 

1. Install the dependencies
   run `pip install flask html pyopenssl`
2. Go to the file named webFileShare.py and change the variables `file_location` and `text_copy` to what they correspond.
   * `file_location`: the directory starting from where the file is run until the file you want to share.
   * `text_copy`: the text you want them to recieve or copy.
   * Remember to keep in mind if one of them is left empty they will not show up to the user.
3. Run the webFileShare.py file using python3, for example `python3 webFileShare`
   * The terminal will output the classical flask interface, look for the one that is not your localhost (usually 127.0.0.1) and share this url with the person you want to share with.

