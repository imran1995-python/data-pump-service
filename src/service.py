import json
import os
import boto3
import requests
import time
import logging

logging.basicConfig(filename='service.log',
                            filemode='a',
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger=logging.getLogger(__name__)
logger.addHandler(ch)

class PumpData():
    def __init__(self):
        self.frequency= os.environ["frequency"] if os.getenv("frequency") is not None else os.environ["default_frequency"]
        self.boto_client=boto3.client('sqs',aws_access_key_id=os.environ["aws_access_key_id"],
                                      aws_secret_access_key=os.environ["aws_secret_access_key"],
                                      region_name=os.environ["aws_region"])
    def start(self):
        try:
            logger.info(f"Getting messages count from SQS queue {os.environ['sqs_queue_url']}")
            _queue=self.boto_client.get_queue_attributes(QueueUrl=os.environ["sqs_queue_url"],
                                                         AttributeNames=['ApproximateNumberOfMessages'])
            _message_count=_queue['Attributes']['ApproximateNumberOfMessages']
            logger.info(f"{_message_count} messages found in the queue")
        except Exception as ex:
            logger.error("Data was not fetched from SQS queue successfully")
            logger.error(f"Exception: {ex}")
            logger.info('Service failed')
            return

        self.post_data(_message_count)


    def post_data(self,data):
        try:
            logger.info(f"Calling webhook {os.environ['webhook_url']}")
            headers={
                'x-editor-id':'test_editor_id',
                'Content-Type':'application/json'
            }
            data={
                'entity_id':'test_entity_id',
                'properties':[{'current_value':data}]
            }
            requests.put(os.environ["webhook_url"],data=json.dumps(data),headers=headers)
            logger.info("Data sent to webhook")
        except Exception as ex:
            logger.error("Data was not sent to webhook")
            logger.error(f"Exception: {ex}")
            logger.info('Service failed')
            return

        logger.info('Service successful')


if __name__=="__main__":
    service=PumpData()
    while True:
        logger.info("Starting service...")
        service.start()
        logger.info("Service ended")
        time.sleep(float(service.frequency) * 60)
