from flask import Flask, render_template, jsonify, send_file
app = Flask(__name__)

import os


def format_report_name(raw_report_name):
    """

    :param raw_report_name:
    :return:
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
def hello():

    import ipdb
    # ipdb.set_trace()

    reports = os.listdir('BenchmarkDB/foo')

    report_list = list()

    for report in reports:

        if not report.startswith('.') and not report.startswith('markdown'):

            formatted_name = format_report_name(report)

            report_list.append(
                (formatted_name, report)
            )

    return render_template('index.html', reports=report_list)

@app.route("/<report_url>/")
def render_report_template(report_url):

    return render_template('report.html')


@app.route("/<report_url>/images/<image_url>")
def return_image(report_url, image_url):

    filename = "Benchmarkdb/foo/{report}/images/{image}".format(
        report=report_url,
        image=image_url,
    )

    return send_file(filename, mimetype='image/png')

@app.route("/<report_url>/view")
def display_report(report_url):

    print('fooooo')

    file = 'BenchmarkDB/foo/{url}/{url}.md'.format(
        url=report_url,
    )

    with open(file, 'r') as infile:

        report_content_raw = infile.read()

    report_content_lines = report_content_raw.split('\n')

    report_content = str()

    for line in report_content_lines:

        report_content += "'{line}'\\\n".format(line=line)

    # import ipdb
    # ipdb.set_trace()

    json = jsonify(document=report_content_raw)

    return json



if __name__ == "__main__":
    app.debug = True
    app.run()