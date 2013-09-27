#!/usr/bin/python

from flask import Flask, g, render_template, request, jsonify, Response
import re
import json
import socket

app = Flask(__name__, static_url_path='')

@app.before_request
def get_basics():
    g.response = {
        'ip':         request.remote_addr,
        'user_agent': str(request.user_agent),
        'platform':   request.user_agent.platform,
        'browser':    request.user_agent.browser,
        'accepts':    str(request.accept_mimetypes),
        'cookies':    request.cookies,
      }

@app.route('/')
def index(format=None):
    format = request.args.get('format')

    # If the user-agent is curl, just return the public IP address
    if re.search('curl', str(g.response['user_agent'])):
        return Response(g.response['ip'], mimetype='text/plain')

    # We don't set this with global because it actually requires time to do
    # the reverse lookup
    g.response['public_hostname'] = str(socket.gethostbyaddr(request.remote_addr)[1][0])

    if format == 'json':
        return jsonify(g.response)

    # No valid format found, return just HTML
    return render_template('index.jinja.html', values=g.response)

if __name__ == '__main__':
  app.run()
