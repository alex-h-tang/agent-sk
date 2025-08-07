# Sales Copilot MCP

## Overview

This is a custom modular Python Model Context Protocol (MCP) server for interacting with CommScope's Dataverse, providing plugin-based APIs for accounts, leads, opportunities, orders, products, quotes, and users. It is built with FastAPI and FastMCP, and designed for Azure deployment, and subsequent integration as a Copilot Studio MCP Server connector.

 <br>

## 1. Objective

The objective of this project is to create a library of tools (through MCP) available for an AI agent to interact with a Microsoft Dataverse environment, supporting the sales team.

  

This project serves as the bridge between an agent and CommScope's complex CRM database. Instead of forcing the agent to construct raw database queries, which it does with Microsoft's prebuilt Dataverse MCP, this library provides a set of high-level, business-aware functions. These tools allow the agent to perform a range of tasks, with more accuracy and effeciency compared to the prebuilt server.

<br>

## 2. How It Works

The server operates in two main stages: the tools exposed in modular "plugins", in the `servers` folder, which are in fact FastMCP servers, mounted onto the `fastmcp_server.py` file. The reason for the lack of actual "plugins" is that FastMCP has replaced the concept with servers, as I had previously created plugins with Semantic Kernel and LangChain.

  

The `config.py` file contains the logic for initializing the `DataverseClient`, which is then imported into each plugin for use. It also contains the read operations used to access data through authenticated HTTP requests to the Dataverse Web API, using Python's `requests` library. Each tool's logic constructs OData query strings (`$filter`, `$select`, `$expand`) which are appended to the request URL.

  

Access to Dataverse is secured via Microsoft Entra ID. The file uses the `azure-identity` library to validate credentials.

  

For local development and testing, it uses `AzureDeveloperCliCredential` (from the Azure CLI). When deployed in Azure, it uses `ManagedIdentityCredential` to authenticate. A bearer token is acquired from this credential and injected into the headers of all API requests.

<br>  

## 3. Project Design  
<br>

**Modular Plugins**

  

Instead of a single monolithic FastMCP file, the logic is separated by Dataverse tables into distinct servers, found in the `servers` folder.

  

This makes the project easy to navigate, maintain, and extend. Adding tools for a new table (e.g., Tasks) would simply involve creating a new `tasks.py` server.

  

Existing plugins listed below:

- Accounts

- Competitors

- Contacts

- Invoices

- Leads

- Opportunities

- Orders

- Products

- Quotes

- Teams

- Users

<br>  

**Dataverse Client**

  

The `DataverseClient` class from `config.py` is imported into every server for access to the Microsoft Dataverse. It only handles the raw communication with the Dataverse API; all business logic should be separated.

<br>  

**Server Tools**

  

Tools are designed to be realtively high-level, business aware functions for accessing data or other calculations.

  

They are named based on business use (e.g., `list_account_opportunities`), and should contain a docstring describing their use. This makes them easier for an agent to understand and use correctly.

<br>

## 4. Azure App Service

  

This server is deployed as a web app through Microsoft's Azure App Service. The GitHub Actions workflow in `.github/workflows/main_dataversemcp.yml` automates build and deployment. A client secret from the Azure app must be added to repository settings for the workflow to work. A managed identity for the app must be setup, so the app can access Microsoft Dataverse.

Startup command for Azure
```sh
uvicorn fastmcp_server:app --host 0.0.0.0 --port 8000
```

 <br>

## 5. Local Testing

  

_**Necessary imports are listed in requirements.txt.**_

_**.env file must contain DATAVERSE_URL, as well as AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT_NAME, AZURE_OPENAI_API_VERSION.**_


Debug with MCPInspector 
```sh
fastmcp dev fastmcp_server.py
```


To locally test responses and chat with the agent, use the console after running this

```sh

python fastmcp_test.py

```
 
