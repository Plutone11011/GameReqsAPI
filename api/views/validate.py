import json
from flask import Response


def validate(messages: dict):
    problem = {
        'type': 'https://tools.ietf.org/html/rfc7807#section-3',
        'title': 'Your request parameters weren\'t valid.',
        'invalid-params': []
    }

    for name, reason in messages.items():
        problem['invalid-params'].append({
            'name': name,
            'reason': reason
        })

    if len(problem['invalid-params']):
        return Response(json.dumps(problem), status=400, mimetype='application/problem+json')
    else:
        return None
