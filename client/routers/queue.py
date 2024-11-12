from fastapi import APIRouter
from azure.servicebus import ServiceBusClient, ServiceBusMessage
from fastapi import HTTPException
from client.config import config
from client.logger import logger
from client.models import Person

router = APIRouter()


@router.post("/messages")
def create_message_endpoint(person: Person) -> dict:
    """
    This endpoint allows you to send a new message to an Azure Service Bus Queue. The message is added to the queue
    in the order it was received (FIFO - First In, First Out).


    :param person:
        The content of the message to be added to the queue. It is expected to conform to the Person
        schema, which will be serialized into the message content to be sent to the Azure Service Bus Queue.

    :returns:
        Message indicating that the message transmission was successful. It is to be noted that the
        "send_message" function associated with the queue *DOES NOT* return anything. If transmission fails, an
        exception will be triggered.
    """
    try:
        # Initialize the ServiceBusClient
        client = ServiceBusClient.from_connection_string(config.CONNECTION_STRING)
        queue_name = config.QUEUE_NAME

        # Serialize the message content as a JSON string
        message_content = person.json()

        with client:
            # Get a sender for the queue
            sender = client.get_queue_sender(queue_name=queue_name)

            with sender:
                # Create a ServiceBusMessage
                message = ServiceBusMessage(message_content)

                # Send the message - note that this function does NOT have a return value
                sender.send_messages(message)

                # Log that the message was sent
                logger.info("Message successfully sent to Service Bus Queue.")

                # Return success message
                return {"status": "Message sent successfully to the queue."}

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
