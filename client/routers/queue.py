import json

from azure.servicebus import ServiceBusClient, ServiceBusMessage
from fastapi import APIRouter
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

        # Serialize the message content as a JSON string
        message_content = person.json()

        with client:
            # Get a sender for the queue
            sender = client.get_queue_sender(queue_name=config.QUEUE_NAME)

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


@router.get("/messages")
async def receive_messages_endpoint():
    """
    Endpoint to receive, process and delete messages from the Azure Service Bus Queue.

    :returns: A list of formatted messages or that the queue was empty
    """
    try:
        # Initialize the ServiceBusClient with the connection string
        client = ServiceBusClient.from_connection_string(conn_str=config.CONNECTION_STRING)

        # Create the receiver for the queue
        with client:
            receiver = client.get_queue_receiver(queue_name=config.QUEUE_NAME)

            with receiver:
                logger.info(f"Starting to receive messages from queue: {config.QUEUE_NAME}")

                # Receive messages
                received_msgs = receiver.receive_messages(max_wait_time=5, max_message_count=20)

                # Early return if no messages were received; this means that the queue is empty
                if not received_msgs:
                    logger.info("No messages received from the queue.")
                    return {"message": "Queue is empty"}
                else:
                    logger.info(f"Received {len(received_msgs)} message(s) from the queue.")

                # Initialize a list to store the messages to be output
                output_messages = []

                # Process, store and remove each received message
                for msg in received_msgs:
                    try:
                        logger.info(f"Processing message: ID={msg.message_id}, "
                                    f"Sequence={msg.sequence_number}, Content={msg}")
                        if msg.body:
                            try:
                                # Decode the JSON payload
                                message_json = json.loads(next(msg.body).decode('utf-8'))
                                logger.info(f"Decoded Message JSON:\n{json.dumps(message_json, indent=2)}")

                                # Append formatted message to our list of output messaged
                                output_messages.append({
                                    "message_id": msg.message_id,
                                    "sequence_number": msg.sequence_number,
                                    "content": message_json
                                })

                                # Remove the message from queue
                                receiver.complete_message(msg)
                                logger.info(f"Message with ID {msg.message_id} has been completed.")

                                return {"messages": output_messages}

                            except json.JSONDecodeError as e:
                                logger.error(f"Error decoding JSON: {e}")
                    except Exception as msg_error:
                        logger.error(f"Error while processing message {msg.message_id}: {msg_error}")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
