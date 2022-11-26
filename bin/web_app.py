import report_racing as rr
from flask import Flask, request, jsonify
from flask import render_template, make_response
from flask_restful import Resource, Api, reqparse
from flasgger import Swagger, swag_from
from flask import url_for
import json
import config


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'API Report Racing',
    'uiversion': 3,
    "specs_route": "/swagger/"
}

swagger = Swagger(app)
app.config.from_object(config.Config)
api = Api(app)
app.config['DEBUG'] = True
app.config['JSON_SORT_KEYS'] = False
app.config['STATIC_FOLDER'] = 'data'


def sort_asc_desc(folder, key):
    """
    import sort function from report_racing package and return sort dict by key asc or desc
    """
    return rr.sort_report(rr.error_code_and_zero(rr.build_report(folder)), key)


class Report(Resource):
    @swag_from('docs/report.yaml', endpoint='report')
    def get(self):
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')
        request_format = request.args.get('format', type=str)

        if request_format == "json":
            return jsonify(report)

        else:
            return 'Error Wrong format', 400


class DriverID(Resource):
    # @swag_from('swagger/report_id.yml', endpoint='report_id')
    def get(self, driver_id):
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')

        if driver_id in report.keys():

            return jsonify(report[driver_id])

        else:
            return 'Error Wrong format', 400


api.add_resource(Report, '/api/v1/report/', endpoint='report')
api.add_resource(DriverID, '/api/v1/report/<driver_id>', endpoint='report_id')
# api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
