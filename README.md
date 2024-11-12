# Python API integrated with Azure Service Bus Queue

## Requirements

- **Platform**: x86-64, Linux/WSL
- **Programming Language**: [Python 3](https://www.python.org/downloads/)
- **Cloud Account**: [Azure](https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account)
- **Resource provisioning**: [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/)


## Allocate resources

The shell script [provision_resources](infra/provision_resources.sh) creates Azure resources by calling the Azure CLI, which in turn
makes HTTP calls to the resource-specific API on Azure. 

It will create the following hierarchy of resources:

```mermaid
graph TD
    A[Subscription]
    A --> B[Resource Group]
    B --> C[Service Bus Namespace]
    C --> E[Service Bus Queue]

    A -->|Contains| B
    B -->|Contains| C
    C -->|Contains| E
```

For this script to work it is necessary to have a configuration file named **infra_config.env** in your [infra](infra) directory. It contains sensitive information
such as tenant and subscription id as well as information used to reference resources. The file has been added to our [.gitignore](.gitignore) so that you don't accidentally commit it.
### Structure of 'infra/infra_config.env'
```bash
TENANT_ID={TO_BE_SET_BY_YOU_MY_FRIEND}
SUBSCRIPTION_ID={TO_BE_SET_BY_YOU_MY_FRIEND}
LOCATION=northeurope
RESOURCE_GROUP_NAME=hvalfangstresourcegroup
SERVICE_BUS_NAMESPACE=hvalfangstservicebusnamespace
QUEUE_NAME=hvalfangstqueue
```

## Deallocate resources

The shell script [delete_resources](infra/delete_resources.sh) deletes our Azure service bus queue, namespace and resource group.

## Client config

Once you have provisioned the Azure resources, there is one last configuration file which has to be created. The file **service_bus_config.env** is expected to exist in the
[client](client) directory. It is used by our service bus [configuration](client/config/service_bus.py) class, which reads values from aforementioned files and maps them to it accordingly.
It contains the means to reach our Service Bus Namespace.

### Structure of 'client/service_bus_config.env'
```bash
CONNECTION_STRING={TO_BE_SET_BY_YOU_MY_FRIEND}
QUEUE_NAME=hvalfangstqueue
```

You can get hold of the namespace connection string either by peeking in your terminal logs as it was actually echoed (yes, I know) as part of our [infrastructure provisioning](infra/provision_resources.sh)
OR you can go for **ClickOps** approach and copy it from the **Shared access policies** under your **Service Bus Namespace** on Azure - as the screenshot below illustrates.

![img.png](images/service_bus_namespace_sas.png)


## Running API

The shell script [run_client](client/run_client.sh) creates a new virtual environment based on our [requirements](client/requirements.txt) file and serves our
API on port 8000 using uvicorrn.



A [Postman Collection](client/postman) has been provided,
which contains example requests for interacting with our [queue](client/routers/queue.py).
