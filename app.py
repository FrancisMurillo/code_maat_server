from flask import Flask, jsonify

from converter import PeriodConverter


app = Flask(__name__)

app.url_map.converters['period'] = PeriodConverter


@app.route('/period/<period:start_date>/<period:end_date>', methods=['GET'])
def index(start_date, end_date):
    return jsonify('lel')


@app.route('/period/<period:start_date>/<period:end_date>/', methods=['GET'])
def index(start_date, end_date):
    return jsonify('lel')


if __name__ == '__main__':
    app.run(debug=True)
