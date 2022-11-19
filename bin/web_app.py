import report_racing as rr
from flask import Flask, request, jsonify
from flask import render_template, make_response
from flask_restful import Resource, Api
from flasgger import Swagger
from flask import url_for

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)
app.config['DEBUG'] = True
app.config['STATIC_FOLDER'] = 'data'


def sort_asc_desc(folder, key):
    """
    import sort function from report_racing packege and return sort dict by key asc or desc
    """
    return rr.sort_report(rr.error_code_and_zero(rr.build_report(folder)), key)


class Report(Resource):
    def get(self):

        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')

        return jsonify(report)



api.add_resource(Report, '/api/v1/report')
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
