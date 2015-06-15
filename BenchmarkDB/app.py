"""
DB Benchmarking Application
===========================

App.py

This file houses a simple flask app to serve rendered benchmark reports to a
web browser.

"""

from flask import Flask, render_template, jsonify, send_file

app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static',
)

import os


def format_report_name(raw_report_name):
    """ This function takes the raw report names and splits it appropriately
    to pull the different pieces of important information contained therein

    :param str raw_report_name: The name of the report to be split

    :return str formatted_name: A more hum-readable version of the report name
    """
    raw_report_split = raw_report_name.split('-')

    db_name = raw_report_split[0]
    date_month = raw_report_split[1]
    date_year = raw_report_split[2]
    time_hour = raw_report_split[4]
    time_minute = raw_report_split[5]

    formatted_name = '{db}, from {month}, {year}, at {hour}:{minute}'.format(
        db=db_name,
        month=date_month,
        year=date_year,
        hour=time_hour,
        minute=time_minute,
    )

    return formatted_name


@app.route("/")
def index():
    """ The index of the app, which displays all reports that are available
    for viewing

    :return render_template_obj template: The rendered index page template
    """
    reports = os.listdir('foo')

    report_list = list()

    for report in reports:

        if not report.startswith('.') and not report.startswith('markdown'):

            formatted_name = format_report_name(report)

            report_list.append(
                (formatted_name, report)
            )

    template = render_template('index.html', reports=report_list)

    return template


@app.route("/<report_url>/")
def render_report_template(report_url):
    """ Renders the report template page

    :param str report_url: The path of the report to render, which is un-used

    :return render_template_obj: the rendered template object
    """
    template = render_template('report.html')

    return template


@app.route("/static/<filename>")
def return_static_file(filename):
    """ This function returns a static file for use in the browser

    :param str filename: the name of the static file to be served

    :return static_file file: the static file to be returned
    """
    file = app.send_static_file(filename)

    return file


@app.route("/<report_url>/images/<image_url>")
def return_image(report_url, image_url):
    """ Returns the appropriate benchmarking metric plot from the appropriate
    report directory

    :param str report_url: the url of the report for the image
    :param str image_url: the name of the image to be served

    :return send_file_obj: the image to be served
    """
    filename = "foo/{report}/images/{image}".format(
        report=report_url,
        image=image_url,
    )

    return send_file(filename, mimetype='image/png')

@app.route("/<report_url>/view")
def retrieve_report(report_url):
    """ Retrieves the appropriate report based on the url and then returns it
     in a json object

    :param str report_url: the url for the report to be retrieved

    :return dict json: the json object containing the report
    """
    file = 'foo/{url}/{url}.md'.format(
        url=report_url,
    )

    with open(file, 'r') as infile:

        report_content_raw = infile.read()

    json = jsonify(document=report_content_raw)

    return json


if __name__ == "__main__":

    app.debug = True
    app.run()