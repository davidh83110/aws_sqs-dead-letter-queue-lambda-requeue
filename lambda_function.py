import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DLQ():
    
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        self.queue_name = 'DLQ-message-center-production-high-priority'
        
    def get_queue(self):
        queue = self.sqs.get_queue_by_name(
            QueueName=self.queue_name
        )
        
        return queue
    
    def send_message(self):
        pass
    
    def delete_message(self):
        pass
        
        
    def receive_msg_from_dlq(self):
        
        queue=self.get_queue()
        
        messages = queue.receive_messages(
            AttributeNames=['All']
        )
        
        logger.info('Message Length: '+ str(len(messages)))
        
        for msg in messages:
            logger.info('Message: ' + str(msg))
            
            ## send this msg back to source queue
            ## delete this msg
            
            
        return messages

def lambda_handler(context, event):
    logger.info('Event Body: ' + event)

