from shutil import which
from os import path
from flask import Flask, jsonify

import config
from converter import PeriodConverter


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


cli = CLI(**app.config)

# Actual setting
app.url_map.converters['period'] = PeriodConverter


@app.route('/period/<period:start_date>/<period:end_date>/', methods=['GET'])
def index(start_date, end_date):
    return jsonify('lel')


if __name__ == '__main__':
    app.run()
