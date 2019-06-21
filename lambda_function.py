import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DLQ:
    
    def __init__(self, queue_name):
        self.sqs = boto3.resource('sqs')
        self.dead_letter_queue_name = queue_name
        
    def get_queue(self, queue_name):
        queue = self.sqs.get_queue_by_name(
            QueueName=queue_name
        )
        return queue
    
    def send_messages_to_source_queue(self, retry_count, message_id, message_body):
        
        source_queue_name = self.dead_letter_queue_name.replace('DLQ-', '')
        logger.info('Source Queue: %s', source_queue_name)

        to_send_retry_count = int(retry_count) + 1
        
        self.get_queue(source_queue_name).send_messages(Entries=[
                {
                    'Id': message_id,
                    'MessageBody': message_body,
                    'MessageAttributes': {
                        'retryCount': {
                            'StringValue': str(to_send_retry_count),
                            'DataType': 'String'
                        }
                    }
                }
            ]
        )
    
    def delete_message_from_dlq(self, message_id, message_receipt_handle):
        
        self.get_queue(self.dead_letter_queue_name).delete_messages(Entries=[
                {
                    'Id': message_id,
                    'ReceiptHandle': message_receipt_handle
                }
            ]
        )
            

def lambda_handler(event, context):
    logger.info('Event Body: \n' + str(event))
    
    for i, msg in enumerate(event['Records']):

        logger.info('Index:[%s], starting requeue...', str(i))

        dlq_name = msg['eventSourceARN'].split(':')[5]
        message_id = msg['messageId']
        message_receipt_handle = msg['receiptHandle']
        message_body = msg['body']
        retry_count = msg['messageAttributes']['retryCount']['stringValue']

        if retry_count > 3:
            logger.warning('Index:[%s], Times:[%s], ID: %s. This task is retrying over 3 time. function end.', str(i), str(retry_count), str(message_id))
            logger.info('Index:[%s], Deleteing message on DLQ...', str(i))
            DLQ(dlq_name).delete_message_from_dlq(message_id, message_receipt_handle)
            return 200

        logger.info('Index:[%s], Sending message back to source queue...', str(i))
        DLQ(dlq_name).send_messages_to_source_queue(retry_count, message_id, message_body)

        logger.info('Index:[%s], Deleteing message on DLQ...', str(i))
        DLQ(dlq_name).delete_message_from_dlq(message_id, message_receipt_handle)

    return 200