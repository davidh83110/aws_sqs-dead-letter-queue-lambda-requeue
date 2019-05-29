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
        
#         res = self.get_queue(source_queue_name).send_messages(
#             Entries=[
#                 {
#                     'Id': message_id,
#                     'MessageBody': message_body
#                 }
#             ]
#         )
        
#         logger.info('Send Message Response: ' + res)
        return True
    
    def delete_message_from_dlq(self, message_id, message_receipt_handle):
        
#         res = self.get_queue(self.dead_letter_queue_name).delete_messages(
#             Entries=[
#                 {
#                     'Id': message_id,
#                     'ReceiptHandle': message_receipt_handle
#                 }
#             ]
#         )
        
#         logger.info('Send Message Response: ' + res)
        return True
        
        
    def requeue_all(self):
        
        messages = self.get_queue(self.dead_letter_queue_name).receive_messages(
            MaxNumberOfMessages=10, 
            WaitTimeSeconds=20
        )
        
        logger.info('Message Length: '+ str(len(messages)))
        
        for i, msg in enumerate(messages):
            
            logger.info('Index:[%s], Message ID: %s', str(i), msg.message_id)
            logger.info('Index:[%s], Message Body: %s', str(i), str(msg.body))
            logger.info('Index:[%s], Message Receipt Handle: %s', str(i), str(msg.receipt_handle))
            
            
            logger.info('Index:[%s], Sending message back to source queue...', str(i))
            if self.send_messages_to_source_queue(msg.message_id, msg.body):
                logger.info('Index:[%s], Message is backed to source queue.', str(i))
            else:
                logger.warn('Index:[%s], Message sent to source queue failed.', str(i))

                
                
            logger.info('Index:[%s], Deleteing message on DLQ...', str(i))
            if self.delete_message_from_dlq(msg.message_id, msg.receipt_handle):
                logger.info('Index:[%s], Message deleted.', str(i))
            else:
                logger.warn('Index:[%s], Message delete failed.', str(i))
                
            logger.info('Index:[%s], Job done requeue.', str(i))
                
            
            
        return 200

def lambda_handler(context, event):
    logger.info('Event Body: ' + event)

if __name__ == '__main__':
    DLQ().requeue_all()