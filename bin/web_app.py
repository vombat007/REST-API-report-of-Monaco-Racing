import report_racing as rr
from flask import Flask, request, jsonify
from flask import render_template, make_response
from flask_restful import Resource, Api
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
        # """
        # This examples uses FlaskRESTful Resource
        # It works also with swag_from, schemas and spec_dict
        # ---
        # parameters:
        #   - in: path
        #     name: report
        #     format:
        #     type: string
        #     required: true
        # responses:
        #   200:
        #     description: A single user item
        #     schema:
        #       id: User
        #       properties:
        #         username:
        #           type: string
        #           description: The name of the user
        #           default: Steven Wilson
        # """
        report = sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')
        report = json.dumps(report)

        return report


api.add_resource(Report, '/report', endpoint='report')
# api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
