from flask import request

from matsuo.haiku_service.solver import create_haiku
from matsuo.service_base.service import HostedService
import json


def generate_haiku(*wargs, **kwargs):
    if 'keywords' not in request.args:
        for arg in request.args:
            if 'keywords' in arg:
                keywords = arg['keywords']
                break
    else:
        keywords = request.args['keywords']

    if not isinstance(keywords, list) and not isinstance(keywords, tuple):
        keywords = list(word[1:-1] for word in keywords.strip('[').strip(']').strip(',').split(', '))
    haiku = create_haiku(keywords)
    return json.dumps({
        'text': str(haiku)
    })


class HaikuService(HostedService):

    SERVICE_NAME = 'Haiku Generator'

    def __init__(self, **kwargs):
        super().__init__(HaikuService.SERVICE_NAME, kwargs=kwargs)

    def start(self):
        self.host.add_endpoint('generate_haiku', 'generate_haiku', generate_haiku, methods=['GET'])
        self.host.start()
