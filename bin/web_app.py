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
app.config['STATIC_FOLDER'] = 'data'


def sort_asc_desc(folder, key):
    """
    import sort function from report_racing packege and return sort dict by key asc or desc
    """
    return rr.sort_report(rr.error_code_and_zero(rr.build_report(folder)), key)


class Report(Resource):
    @swag_from('report.yaml', endpoint='report')
    def get(self):
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')

        if request.args.get('format') == "json":
            return jsonify(report)
        else:
            return 'Error Wrong args'


api.add_resource(Report, '/api/v1/report/', endpoint='report')

# api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
