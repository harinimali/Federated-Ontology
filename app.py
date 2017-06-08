from flask import Flask, request, render_template
from common.globalfunct import json_decode, respond_json
from server.jena import query_apache_jena

application = Flask(__name__, )


@application.route('/')
def app_home():
    return render_template('index.html')


@application.route('/query', methods=['POST'])
def app_query_jena():
    query_fields = json_decode(str(request.form['data']))
    result, status = query_apache_jena(**(query_fields['request']))
    return respond_json(status, result=result)


if __name__ == '__main__':
    application.run(host='localhost', port=5000, debug=True)
