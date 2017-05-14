from werkzeug.routing import BaseConverter

from datetime import datetime


class PeriodConverter(BaseConverter):
    _period_format = "%Y%m%d"

    def to_python(self, text):
        return datetime.strptime(text, PeriodConverter._period_format)

    def to_url(self, date):
        return datetime.strftime(date, PeriodConverter._period_format)
