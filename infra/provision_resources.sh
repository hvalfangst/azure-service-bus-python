#!/bin/bash

echo "Starting Azure Service Bus provisioning script..."

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

# Create the resource group
echo -e "\nCreating resource group: $RESOURCE_GROUP_NAME in location $LOCATION..."
az group create --name "$RESOURCE_GROUP_NAME" --location "$LOCATION"
if [ $? -ne 0 ]; then
  echo "Failed to create resource group: $RESOURCE_GROUP_NAME."
  exit 1
fi
echo "Resource group $RESOURCE_GROUP_NAME created successfully."

# Create the Service Bus namespace
echo -e "\nCreating Service Bus namespace: $SERVICE_BUS_NAMESPACE in resource group $RESOURCE_GROUP_NAME..."
az servicebus namespace create --name "$SERVICE_BUS_NAMESPACE" --resource-group "$RESOURCE_GROUP_NAME" --location "$LOCATION" --sku Standard
if [ $? -ne 0 ]; then
  echo "Failed to create Service Bus namespace: $SERVICE_BUS_NAMESPACE."
  exit 1
fi
echo "Service Bus namespace $SERVICE_BUS_NAMESPACE created successfully."

# Create the Service Bus queue
echo -e "\nCreating Service Bus queue: $QUEUE_NAME in namespace $SERVICE_BUS_NAMESPACE..."
az servicebus queue create --resource-group "$RESOURCE_GROUP_NAME" --namespace-name "$SERVICE_BUS_NAMESPACE" --name "$QUEUE_NAME"
if [ $? -ne 0 ]; then
  echo "Failed to create Service Bus queue: $QUEUE_NAME."
  exit 1
fi
echo "Service Bus queue $QUEUE_NAME created successfully."

# Retrieve and display the connection string for the Service Bus namespace
echo -e "\nRetrieving connection string for Service Bus namespace $SERVICE_BUS_NAMESPACE..."
CONNECTION_STRING=$(az servicebus namespace authorization-rule keys list --resource-group "$RESOURCE_GROUP_NAME" --namespace-name "$SERVICE_BUS_NAMESPACE" --name "RootManageSharedAccessKey" --query "primaryConnectionString" -o tsv)
if [ $? -ne 0 ]; then
  echo "Failed to retrieve connection string for Service Bus namespace: $SERVICE_BUS_NAMESPACE."
  exit 1
fi

echo -e "\n\n - - - - | ALL RESOURCES WERE SUCCESSFULLY PROVISIONED | - - - - \n\n"

# Display the connection string (ONLY for local use - do not blindly deploy this script)
echo -e "\nService Bus namespace connection string: \n\n$CONNECTION_STRING"

