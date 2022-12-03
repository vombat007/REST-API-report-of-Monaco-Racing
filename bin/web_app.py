import report_racing as rr
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import config
from simplexml import dumps
import json

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
app.json.sort_keys = False
app.config['STATIC_FOLDER'] = 'data'


@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(json.dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp


@api.representation('application/xml')
def output_xml(data, code, headers=None):
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp


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
        request_order = request.args.get('order', type=str)

        if request_format == "json" and request_order == "asc":
            return jsonify(report)

        if request_format == "json" and request_order == "desc":
            report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'desc')
            return jsonify(report)

        if request_format == "xml" and request_order == "asc":
            return report

        if request_format == "xml" and request_order == "desc":
            report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'desc')
            return report

        else:
            return 'Error Wrong format', 400


class DriverID(Resource):
    @swag_from('docs/report_id.yml', endpoint='report_id')
    def get(self, driver_id):
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')

        if driver_id in report:
            return report[driver_id]

        else:
            return 'Error Wrong format', 400


api.add_resource(Report, '/api/v1/report/', endpoint='report')
api.add_resource(DriverID, '/api/v1/report/<driver_id>/', endpoint='report_id')


if __name__ == "__main__":
    app.run(debug=True)
