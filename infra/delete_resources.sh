#!/bin/bash

echo "Starting Azure Service Bus deletion script..."

# Load values from infra_config.env
CONFIG_FILE="$(dirname "$0")/infra_config.env"
if [ -f "$CONFIG_FILE" ]; then
  echo "Loading configuration from $CONFIG_FILE..."
  source "$CONFIG_FILE"
else
  echo "Configuration file $CONFIG_FILE not found!"
  exit 1
fi

echo -e "\nSetting subscription context to $SUBSCRIPTION_ID..."
az account set --subscription "$SUBSCRIPTION_ID"
if [ $? -ne 0 ]; then
  echo "Failed to set subscription context."
  exit 1
fi
echo "Subscription context set successfully."

# Delete the Service Bus queue
echo -e "\nDeleting Service Bus queue: $QUEUE_NAME in namespace $SERVICE_BUS_NAMESPACE..."
az servicebus queue delete --resource-group "$RESOURCE_GROUP_NAME" --namespace-name "$SERVICE_BUS_NAMESPACE" --name "$QUEUE_NAME"
if [ $? -ne 0 ]; then
  echo "Failed to delete Service Bus queue: $QUEUE_NAME."
else
  echo "Service Bus queue $QUEUE_NAME deleted successfully."
fi

# Delete the Service Bus namespace
echo -e "\nDeleting Service Bus namespace: $SERVICE_BUS_NAMESPACE in resource group $RESOURCE_GROUP_NAME..."
az servicebus namespace delete --name "$SERVICE_BUS_NAMESPACE" --resource-group "$RESOURCE_GROUP_NAME"
if [ $? -ne 0 ]; then
  echo "Failed to delete Service Bus namespace: $SERVICE_BUS_NAMESPACE."
else
  echo "Service Bus namespace $SERVICE_BUS_NAMESPACE deleted successfully."
fi

# Delete the resource group
echo -e "\nDeleting resource group: $RESOURCE_GROUP_NAME..."
az group delete --name "$RESOURCE_GROUP_NAME" --yes --no-wait
if [ $? -ne 0 ]; then
  echo "Failed to delete resource group: $RESOURCE_GROUP_NAME."
else
  echo "Resource group $RESOURCE_GROUP_NAME deletion initiated."
fi

echo -e "\n\n - - - - | ALL RESOURCES WERE SUCCESSFULLY DELETED OR DELETION INITIATED | - - - - \n\n"
