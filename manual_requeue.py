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

    def receive_messages_from_dlq(self):
        messages = self.get_queue(self.dead_letter_queue_name).receive_messages(
            MaxNumberOfMessages=10, 
            WaitTimeSeconds=20
        )

        logger.info('Message Length: %s', str(len(messages)))
        return messages
    
    def send_messages_to_source_queue(self, retry_count, message_id, message_body):
        
        source_queue_name = self.dead_letter_queue_name.replace('DLQ-', '')
        logger.info('Source Queue: %s', source_queue_name)

        retry_count += 1
        
        self.get_queue(source_queue_name).send_messages(Entries=[
                {
                    'Id': message_id,
                    'MessageBody': message_body,
                    'MessageAttributes': {
                        'retryCount': {
                            'StringValue': str(retry_count),
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
        
    def requeue_all(self, retry_count):

        total_moved_job = 0
        
        while True:
            messages = self.receive_messages_from_dlq()
            
            if len(messages) == 0:
                break
            else:
                for i, msg in enumerate(messages):
                    
                    logger.info('Index:[%s], Message ID/Body: %s / %s', str(i), msg.message_id, str(msg.body))
                    
                    logger.info('Index:[%s], Sending message back to source queue...', str(i))
                    self.send_messages_to_source_queue(retry_count, msg.message_id, msg.body)
                        
                    logger.info('Index:[%s], Deleteing message on DLQ...', str(i))
                    self.delete_message_from_dlq(msg.message_id, msg.receipt_handle)

            total_moved_job += len(messages)

            if total_moved_job > 60:
                break

        logger.info('Total Moved Job: %s', total_moved_job)
            

def lambda_handler(context, event):
    logger.info('Event Body: \n' + str(event))
    dlq_name = event['Records'][0]['eventSourceARN'].split(':')[5]
    # dlq_name = 'dlq-demo-queue' #Test queue name when without Lambda Trigger

    retry_count = event['Records'][0]['messageAttributes']['retryCount']['stringValue']

    if retry_count > 3:
        logger.error('This task is retrying over 3 time. function end.')
        return 200
    
    DLQ(dlq_name).requeue_all(retry_count)

    return 200

if __name__ == '__main__':
    lambda_handler(context='', event='')