from matsuo.service_base.service import HostedService
import boto3
import os
import regex as re
import json

bucket_name='uottahack18'


def get_keywords(args):
    filename = args['data']
    size = os.path.getsize(filename)
    if(size>5*2**20):
        raise FileSizeLimitExceededError(filename)
    client = boto3.client('rekognition',region_name='us-east-1')
    with open(filename,'rb') as imgb:
        img = imgb.read()
        details = {'Bytes':img}
    response = client.detect_labels(Image=details,MaxLabels=10,MinConfidence=60)
    sresponse = sorted(response['Labels'], key=lambda k: k['Confidence'])
    keywords = []
    for item in response['Labels']:
        keywords.append(item['Name'])
    print(keywords)
    return json.dumps({'keywords': keywords})


class DescribeService(HostedService):
    SERVICE_NAME = 'Describe'

    def __init__(self, **kwargs):
        super().__init__(DescribeService.SERVICE_NAME, kwargs=kwargs)

    def start(self):
        self.host.add_endpoint('get_keywords', 'get_keywords', get_keywords, methods=['GET'])
        self.host.start()


class FileSizeLimitExceededError(LookupError):
    '''Files must be less that 5MB'''
