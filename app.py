import sys
from shutil import which
import os
from os import path, getcwd

from flask import Flask, request, jsonify
from flask_cors import CORS

import config
from util import read_csv_file, parse_date, is_git_dir
from cli import CLI


working_dir = sys.argv[1] if len(sys.argv) > 1 else getcwd()


app = Flask(__name__)
CORS(app)
app.config.from_object(config)
app.config['GIT_DIR'] = working_dir

# Check setting
if not which(app.config['JAVA_COMMAND']):
    raise AssertionError("Java command, %s, does not exist." %
                         app.config['JAVA_COMMAND'])

if not which(app.config['GIT_COMMAND']):
    raise AssertionError("Git command, %s, does not exist." %
                         app.config['GIT_COMMAND'])

if not path.isfile(app.config['CODE_MAAT_JAR_FILE']):
    raise AssertionError("Code Maat jar file, %s, does not exist." %
                         app.config['CODE_MAAT_JAR_FILE'])

if not is_git_dir(working_dir):
    raise AssertionError("Directory, %s, is not a git repo." %
                         app.config['GIT_DIR'])


# Object
cli = CLI(
    code_maat_jar_file=app.config['CODE_MAAT_JAR_FILE'],
    git_command=app.config['GIT_COMMAND'],
    java_command=app.config['JAVA_COMMAND'],
    git_dir=app.config['GIT_DIR'])


# Routing
@app.route('/api/', methods=['GET'])
def blank():
    pass


@app.route('/api/commits', methods=['GET'])
def commit_entries():
    return jsonify(cli.get_commits())


def delete_dir_files(cache_dir):
    filelist = [f for f in os.listdir(cache_dir)]
    for f in filelist:
        os.remove(path.join(cache_dir, f))


@app.route('/api/code-maat', methods=['DELETE'])
def clear_log_files():
    cache_dir = cli.log_dir
    delete_dir_files(cache_dir)
    return jsonify({
        "message": "Log directory is now cleared.",
        "logDir": cache_dir
    })

@app.route('/api/code-maat', methods=['GET'])
def log_file():
    analysis = request.args.get('analysis')
    start_date = request.args.get('start-date')
    end_date = request.args.get('end-date')

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
    elif analysis == 'revision':
        return jsonify(read_csv_file(cli.generate_revision_file(log_file)))
    elif analysis == 'coupling':
        return jsonify(read_csv_file(cli.generate_coupling_file(log_file)))
    elif analysis == 'age':
        return jsonify(read_csv_file(cli.generate_age_file(log_file)))
    elif analysis == 'abs-churn':
        return jsonify(
            read_csv_file(cli.generate_absolute_churn_file(log_file)))
    elif analysis == 'author-churn':
        return jsonify(
            read_csv_file(cli.generate_author_churn_file(log_file)))
    elif analysis == 'entity-churn':
        return jsonify(
            read_csv_file(cli.generate_entity_churn_file(log_file)))
    elif analysis == 'entity-ownership':
        return jsonify(
            read_csv_file(cli.generate_entity_ownership_file(log_file)))
    elif analysis == 'entity-effort':
        return jsonify(
            read_csv_file(cli.generate_entity_effort_file(log_file)))
    else:
        return ("ERROR: Analysis type not in selection.", 400)


app_port = 30080

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app_port)
