import json

from datetime import datetime, date


class XeroJSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.strftime('%Y-%m-%dT%H:%M:%S')
        elif isinstance(o, date):
            return o.isoformat()
        else:
            return super().default(o)


def to_xero_json(data):
    return json.dumps(data, cls=XeroJSONEncoder)
