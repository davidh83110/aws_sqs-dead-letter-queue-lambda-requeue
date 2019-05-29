import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# logger.setLevel(logging.DEBUG)

class DLQ():
    
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        self.dead_letter_queue_name = 'DLQ-message-center-production-high-priority'
        
    def get_queue(self, queue_name):
        queue = self.sqs.get_queue_by_name(
            QueueName=queue_name
        )
        
        return queue
    
    def send_messages_to_source_queue(self, message_id, message_body):
        
        source_queue_name = self.dead_letter_queue_name.replace('DLQ-', '')
        logger.info('Source Queue: ' + source_queue_name)
        
        res = self.get_queue(source_queue_name).send_messages(
            Entries=[
                {
                    'Id': message_id,
                    'MessageBody': message_body
                }
            ]
        )
        
        logger.info('Send Message Response: ' + res)
        return True
    
    def delete_message_from_dlq(self, message_id, message_receipt_handle):
        
        res = self.get_queue(self.dead_letter_queue_name).delete_messages(
            Entries=[
                {
                    'Id': message_id,
                    'ReceiptHandle': message_receipt_handle
                }
            ]
        )
        
        logger.info('Send Message Response: ' + res)
        return True
        
        
    def requeue_all(self):
        
        messages = self.get_queue(self.dead_letter_queue_name).receive_messages(
            MaxNumberOfMessages=10, 
            WaitTimeSeconds=20
        )
        
        logger.info('Message Length: '+ str(len(messages)))
        
        for msg in messages:
            logger.info('Message: ' + str(msg))
            logger.info('Message ID: ' + str(msg.message_id))
            logger.info('Message Body: ' + str(msg.body))
            logger.info('Message Receipt Handle: ' + str(msg.receipt_handle))
            
            logger.info('Sending message back to source queue...')
            if self.send_messages_to_source_queue(msg.message_id, msg.body):
                logger.info('Message is backed to source queue.')
            else:
                logger.warn('Message sent to source queue failed.')
                
            logger.info('Deleteing message on DLQ...')
            if self.delete_message_from_dlq(msg.message_id, msg.receipt_handle):
                logger.info('Message deleted.')
            else:
                logger.warn('Message delete failed.')
                
            
            
        return 200

def lambda_handler(context, event):
    logger.info('Event Body: ' + event)

if __name__ == '__main__':
    DLQ().requeue_all()