import os
import json
import boto3
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

session = boto3.Session()
region = session.region_name
iotdata_client = boto3.client('iot-data')


def lambda_handler(event, context):
    logger.info(event)

    mqtt_topic = event['topic']
    logger.info(mqtt_topic)

    if (len(mqtt_topic) == 0):
        return {"error": 'invalid topic: ' + str(mqtt_topic), }
        
    message = event['payload']

    response = iotdata_client.publish(
        topic=mqtt_topic,
        qos=0,
        payload=json.dumps(message)
    )

    logger.info(response)
    return {
        "message": "Command sent successfully!",
    } 

