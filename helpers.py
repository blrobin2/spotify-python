import csv
from flask import make_response
from io import StringIO


def to_csv_response(data, filename):
    si = StringIO()
    cw = csv.writer(si)
    cw.writerows(data)
    output = make_response(si.getvalue())
    output.headers['Content-Disposition'] = f"attachment; filename={filename}.csv"
    output.headers['Content-Type'] = "text/csv"
    return output
