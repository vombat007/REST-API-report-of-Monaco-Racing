import report_racing as rr
from flask import Flask, request
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


class Home(Resource):
    def get(self):
        return make_response(render_template("base.html", title="WEB Report of Monaco 2018 Racing"))


api.add_resource(Home, '/')


@app.route("/report")
def report():
    """
    create report page and return html template with return table with shows common statistic
    """
    context = {
        "title": "common statistic",
        "test_name": "Report",
        "report": sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')
    }
    return render_template("report.html", **context)


@app.route("/report/drivers")
def drivers():
    """
    create page and return html template with return  code and name table
    """
    context = {
        "title": "Driver",
        "test_name": "Report",
        "report": sort_asc_desc(app.config.get('STATIC_FOLDER'), 'asc')
    }
    return render_template("drivers.html", **context)


@app.route("/report/drivers/")
def driver_links():
    """
    create page and return html template with return info driver or desc report
    """
    driver_id = request.args.get('driver_id')
    order = request.args.get('order')
    context = {
        "report": sort_asc_desc(app.config.get('STATIC_FOLDER'), 'desc'),
        "driver": driver_id
    }
    if order == 'desc':
        return render_template('report.html', **context)
    else:

        return render_template('driver_id.html', **context, title='Info About Driver')


if __name__ == "__main__":
    app.run(debug=True)
