from shutil import which
from os import path

from flask import Flask, request, jsonify

import config
from util import read_csv_file, parse_date
from cli import CLI


app = Flask(__name__)
app.config.from_object(config)


# Check setting
if not which(app.config['JAVA_COMMAND']):
    raise AssertionError("Java command, %s, does not exist." %
                         app.config['JAVA_COMMAND'])

if not which(app.config['GIT_COMMAND']):
    raise AssertionError("Git command, %s, does not exist." %
                         app.config['GIT_COMMAND'])

if not path.isfile(app.config['CODE_MAAT_JAR_FILE']):
    raise AssertionError("Code Maat jar file, %s, doesnot exist." %
                         app.config['CODE_MAAT_JAR_FILE'])


# Object
cli = CLI(**app.config)


# Routing
@app.route('/api', methods=['GET'])
def log_file():
    analysis = request.args.get('analysis')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Parameter
    try:
        start_date = parse_date(start_date)
    except:
        return ("ERROR: Start date can't be parsed by YYYY-MM-DD format.", 400)

    try:
        end_date = parse_date(end_date)
    except:
        return ("ERROR: End date can't be parsed by YYYY-MM-DD format.", 400)

    # Validate
    if start_date > end_date:
        return ("ERROR: Start date can't be ahead of the end date.", 400)

    # Logic
    log_file = cli.generate_log_file(start_date, end_date)

    if analysis is None or analysis == 'summary':
        return jsonify(read_csv_file(cli.generate_summary_file(log_file)))
    elif analysis == 'coupling':
        return jsonify(read_csv_file(cli.generate_coupling_file(log_file)))
    else:
        return ("ERROR: Analysis type not in selection.", 400)


if __name__ == '__main__':
    app.run()
