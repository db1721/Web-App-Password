# Lab 8 - Password
# Author: Dan Beck
# Date: May 9, 2020
# 

from flask import Flask, request, redirect, render_template
import csv

#********Main variables********
#Configures app
app = Flask(__name__)
# request.environ['REMOTE_ADDR']
# response = DbIpCity.get()

#Reads the file for common passwords
file = open("CommonPassword.txt", "r")
reader = csv.reader(file)
COMMONPASSWORDS = list(reader)

userfile = open("store_users.csv", "r")
read = csv.reader(userfile)
USERNAMES = {}
for row in read:
    USERNAMES[row[0]] = row[1]

#********The web pages********
@app.route("/")
def index():
    return render_template("index.html")

#This is just for testing
@app.route("/registered")
def registered():
    file = open("store_users.csv", "r")
    reader = csv.reader(file)
    users = list(reader)
    file.close()
    return render_template("registered.html", users=users)

@app.route("/register", methods=["POST"])
#@limiter.limit('15 per day')
def register():
    name = request.form.get("name")
    password = request.form.get("password")
    
    #Verify that the username and password are valid
    if not name or not password:
        return render_template("NoInput.html")
    elif name in USERNAMES.keys():
        #test if the password matches the user name
        if USERNAMES.get(name) == password:
            return render_template("success.html")
        else:
            return render_template("UserAlreadyExsists.html")
    elif len(password) < 8:
        return render_template("PassTooShort.html")
    elif len(password) > 64:
        return render_template("PassTooLong.html")
    elif any(i[0]==password for i in COMMONPASSWORDS):
        return render_template("TooCommon.html")

    #After validation, stores the user name and password
    file = open("store_users.csv", "a", newline='')
    writer = csv.writer(file)
    writer.writerow((name, password))
    file.close()
    return render_template("success.html")

@app.route("/ChangePassForm", methods=["POST"])
def changepass():
    name = request.form.get("name")
    password = request.form.get("change_password")
    
    if not password:
        return render_template("NoInput.html")
    elif len(password) < 8:
        return render_template("PassTooShort.html")
    elif len(password) > 64:
        return render_template("PassTooLong.html")
    elif any(i[0]==password for i in COMMONPASSWORDS):
        return render_template("TooCommon.html")
    else:
        USERNAMES[name] = password
        #After validation, stores the user name and password
        file = open("store_users.csv", "w", newline='')
        writer = csv.writer(file)
        for key, value in USERNAMES.items():
            writer.writerow([key,value])
        file.close()
    return render_template("success.html")

#********Leave at the end! Allows for debugging********
if __name__ == '__main__':
    app.run(debug=True)