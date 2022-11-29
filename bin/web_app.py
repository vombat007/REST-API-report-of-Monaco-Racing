import report_racing as rr
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
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
app.json.sort_keys = False
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
    @swag_from('docs/report_id.yml', endpoint='report_id')
    def get(self, driver_id):
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')

        if driver_id in report:
            return jsonify(report[driver_id])

        else:
            return 'Error Wrong format', 400


class ReportOrder(Resource):
    @swag_from('docs/order.yml', endpoint='order')
    def get(self):
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'desc')

        return jsonify(report)


api.add_resource(Report, '/api/v1/report/', endpoint='report')
api.add_resource(DriverID, '/api/v1/report/<driver_id>/', endpoint='report_id')
api.add_resource(ReportOrder, '/api/v1/report/order/', endpoint='order')

# api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
