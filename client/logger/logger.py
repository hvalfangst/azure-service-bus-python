import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# In order to get rid of service bus link information one has to increase logging from INFO to WARNING
logging.getLogger("azure.servicebus").setLevel(logging.WARNING)
logging.getLogger("azure").setLevel(logging.WARNING)

logger = logging.getLogger("logger")
