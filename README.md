# A2A + MCP Agent Sample

This repository contains a sample implementation demonstrating how an ISV can front an existing **Model Context Protocol (MCP)** server with an **Agent-to-Agent (A2A)** layer to integrate with **Gemini Enterprise**.

## Table of Contents
- [1. End-to-End Architecture](#1-end-to-end-architecture)
- [2. Multi-Tenancy Patterns](#2-multi-tenancy-patterns)
  - [Pattern A: Shared Instance with Context Passing (Simpler)](#pattern-a-shared-instance-with-context-passing-simpler)
  - [Pattern B: Gateway + Dedicated Tenant Servers (Enterprise-Grade)](#pattern-b-gateway--dedicated-tenant-servers-enterprise-grade)
- [3. Prescriptive Guidance: Orchestration & MCP](#3-prescriptive-guidance-orchestration--mcp)
  - [Orchestration at the A2A Layer](#orchestration-at-the-a2a-layer)
  - [Local vs. MCP Tools](#local-vs-mcp-tools)
  - [MCP Tool Registration & Request Flow](#mcp-tool-registration--request-flow)
  - [Agent Card (agent.json)](#agent-card-agentjson)
  - [Error & Interrupt Handling](#error--interrupt-handling)
- [4. Getting Started](#4-getting-started)

## 1. End-to-End Architecture

The following diagram showcases the standard runtime flow, focusing on the technical execution and security handshakes.

```mermaid
graph TD
    subgraph "Google Cloud (Customer Tenant)"
        User([🧑‍💻 End User])
        GE[🤖 Gemini Enterprise]
    end

    subgraph "ISV Tenant"
        subgraph "Cloud Run Container"
            A2A[🤖 A2A Agent Head]
            MCP[🛠️ MCP Server]
        end
        IdP[🔐 Identity Provider / Auth]
        DB[(ISV Data & APIs)]
    end

    %% Setup Flow (DCR)
    GE -->|1. Dynamic Client Registration| A2A
    A2A -->|2. Returns Credentials| GE

    %% Consumption & Security Flow (Runtime)
    User -->|3. Prompts 'Generate Campaign'| GE
    GE -->|4. OAuth Auth Code Flow| IdP
    IdP -->|5. Returns Access Token| GE
    GE -->|6. A2A SendMessage + Token| A2A
    A2A -->|7. Validates Token| IdP
    A2A -->|8. Calls Tools via stdio| MCP
    MCP -->|9. Fetches Assets| DB
    A2A -->|10. Returns Campaign| GE
    GE -->|11. Displays to User| User

    style A2A fill:#f9f,stroke:#333,stroke-width:2px
    style MCP fill:#bbf,stroke:#333,stroke-width:2px
    style GE fill:#dfd,stroke:#333,stroke-width:2px
```

## 2. Multi-Tenancy Patterns

When exposing this stack to multiple customers, you must choose an isolation strategy. Here are the two main patterns:

### Pattern A: Shared Instance with Context Passing (Simpler)
A single A2A agent handles all customers. Isolation is managed at the software level by passing the Tenant ID.

```mermaid
graph TD
    GE[🤖 Gemini Enterprise] -->|Request + Token| A2A[🤖 Shared A2A Agent]
    A2A -->|Extract Tenant ID| A2A
    A2A -->|Pass Tenant ID| MCP[🛠️ MCP Server]
    MCP -->|Query with Tenant Filter| DB[(Shared DB with Tenant Isolation)]
```
- **Pros**: Low cost, simple to deploy.
- **Cons**: Risk of cross-tenant data leakage if code has bugs.

### Pattern B: Gateway + Dedicated Tenant Servers (Enterprise-Grade)
A stateless gateway routes requests to isolated, tenant-specific server instances.

```mermaid
graph TD
    subgraph Google Cloud
        GE[🤖 Gemini Enterprise]
    end

    subgraph ISV Control Plane
        GW[🌐 A2A Proxy Gateway]
        TR[(Tenant Registry)]
    end

    subgraph "Tenant A Project (Isolated)"
        subgraph Cloud Run A
            A2A_A[🤖 Agent A]
            MCP_A[🛠️ MCP A]
        end
        DB_A[(Data A)]
    end

    subgraph "Tenant B Project (Isolated)"
        subgraph Cloud Run B
            A2A_B[🤖 Agent B]
            MCP_B[🛠️ MCP B]
        end
        DB_B[(Data B)]
    end

    GE -->|1. Request + Token| GW
    GW -->|2. Lookup Tenant| TR
    GW -->|3. Route to Tenant A| A2A_A
    GW -->|3. Route to Tenant B| A2A_B
    A2A_A --> MCP_A
    A2A_B --> MCP_B
```
- **Pros**: Strict isolation, high security, data residency compliance.
- **Cons**: Higher infrastructure cost and management complexity.

## 3. Prescriptive Guidance: Orchestration & MCP

During our development and testing, we addressed common questions regarding agent orchestration and MCP integration:

### Orchestration at the A2A Layer
When fronting your services with an A2A agent, the orchestration burden shifts to the A2A agent. It receives the user prompt from Gemini Enterprise, breaks it down, and calls the necessary tools (local or remote via MCP) to gather context before generating the final response. This gives you full control over business logic and error handling.

### Local vs. MCP Tools
- In this sample (`a2a_agent.py`), tools are exposed via a real **MCP Server** (`mcp_server.py`) and consumed by the agent using the native Google ADK `McpToolset`.
- This demonstrates a production-grade setup where the agent communicates with the tool server via standard I/O (stdio).

### MCP Tool Registration & Request Flow

Here is how MCP tools are registered and how requests resolve to them in this native integration setup.

#### 1. Registration & Discovery
The agent uses `McpToolset` and `StdioServerParameters` to connect to the MCP server (`mcp_server.py`). At runtime, ADK queries the MCP server via `ListToolsRequest` to discover available tools and exposes them to the LLM as function declarations.

#### 2. Request Flow Sequence
The following sequence diagram illustrates how an incoming request resolves to MCP tools:

```mermaid
sequenceDiagram
    participant User as 🧑‍💻 User (Test Runner)
    participant ADK as 🤖 ADK Framework (Runner)
    participant Gemini as 🧠 Gemini Model (Vertex AI)
    participant MCP as 🛠️ MCP Server (mcp_server.py)

    User->>ADK: Sends Prompt ("Generate campaign for Product Launch...")
    ADK->>ADK: Initializes session & loads tools from McpToolset
    ADK->>Gemini: Sends Prompt + Tool Definitions
    Note over Gemini: Model decides it needs more info<br/>and selects a tool.
    Gemini->>ADK: Returns Function Call (e.g., get_project_details)
    ADK->>ADK: Intercepts call & routes to McpToolset
    ADK->>MCP: Sends 'CallToolRequest' via stdio pipe
    Note over MCP: Runs Python function<br/>get_project_details()
    MCP->>ADK: Returns structured result ("Project resolved...")
    ADK->>Gemini: Sends tool result back to model
    Note over Gemini: Model continues reasoning<br/>or generates final answer.
    Gemini->>ADK: Returns final text response
    ADK->>User: Yields final response to user
```

### Agent Card (`agent.json`)

The `agent.json` file at the root is the **Agent Card** (Discovery Document) required by the A2A protocol. It describes the agent's name, description, and skills. Gemini Enterprise reads this file at `.well-known/agent.json` to discover the agent's capabilities during Dynamic Client Registration.

### Error & Interrupt Handling
Review `test_e2e_simulation.py` for examples of how the agent should handle:
- **Missing Information**: Graceful degradation when the user prompt lacks required details.
- **Invalid Input**: Error handling when tools return errors (e.g., project not found).

## 4. Getting Started

For detailed instructions on how to build, deploy, and test this sample, please refer to the:

👉 **[USER_GUIDE.md](USER_GUIDE.md)**

For more details on security (OAuth, DCR) and Marketplace listing, see:
👉 **[MARKETPLACE_GUIDE.md](MARKETPLACE_GUIDE.md)**
