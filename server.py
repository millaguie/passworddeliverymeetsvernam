#!/usr/bin/env python
from __future__ import print_function
from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from subprocess import call
import json
import yaml
import os
import sys
import tempfile

app = Flask(__name__)

@app.route('/v1.0/passwords', methods=['GET'])
def get_passwords():
    passwordsFile = ("passwords.yaml")
    if not os.path.exists(passwordsFile):
        print("Could not find passwords File")
        sys.exit(10)
    passwords = yaml.load(open(passwordsFile,'r'))
    users = []
    for password in passwords:
        for user in password.keys():
            users.append(user)
    return jsonify(users)

@app.route('/v1.0/password/<password>',methods=['GET'])
def show_password(password):
    passwordsFile = ("passwords.yaml")
    if not os.path.exists(passwordsFile):
        print("Could not find passwords File")
        sys.exit(10)
    passwords = yaml.load(open(passwordsFile,'r'))
    for passw in passwords:
        if passw.has_key(password):
            passwordfile = tempfile.NamedTemporaryFile(delete=False)
            passwordfile.write(passw[password])
            passwordfile.close()
            command = "python -m vernam -e -i {} -o  {}crypt -k keyfile".format(passwordfile.name,passwordfile.name)

            exitcode = call(command.split(), shell=False)
            if exitcode == 101:
                os.unlink(passwordfile.name)
                return json.dumps({ "error": "Do not have enough unused key to complete this action" }), 500
            elif exitcode != 0:
                os.unlink(passwordfile.name)
                return json.dumps({ "error": "Vernam error {}".format(exitcode)}), 500


            headers = {"Content-Disposition": "attachment; filename=passwordfile"}
            with open(passwordfile.name+"crypt", 'r') as f:
                body = f.read()
            os.unlink(passwordfile.name)
            os.unlink(passwordfile.name+"crypt")
            return make_response((body, headers))
    abort(404)

if __name__ == '__main__':
    app.run(app.run(host='0.0.0.0', port=8180, debug=True))

