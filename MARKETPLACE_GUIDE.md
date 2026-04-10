# Guide: Bringing Your A2A + MCP Agent to Gemini Enterprise Marketplace

This guide outlines the architecture, security, and steps required for an ISV to list an AI agent on the Google Cloud Marketplace that fronts an existing MCP (Model Context Protocol) server.

## 1. End-to-End Runtime Architecture & Flow

The following diagram showcases how the stack works at runtime, focusing on the technical execution and security handshakes.

```mermaid
graph TD
    subgraph Google Cloud (Customer Tenant)
        User([🧑‍💻 End User])
        GE[🤖 Gemini Enterprise]
    end

    subgraph ISV Tenant
        subgraph Cloud Run Container
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

## 2. What the MCP Server Does

The **MCP Server** in this architecture acts as the **Data and Action Gateway** for your specific domain. While the A2A Agent handles the conversational interface and high-level orchestration, the MCP server does the heavy lifting of interacting with your proprietary systems:

*   **Asset Retrieval**: It fetches project details, layouts, and audience segments from your databases.
*   **Action Execution**: In a full implementation, it would trigger the actual generation of images, text, or campaigns using your backend APIs.
*   **Context Grounding**: It provides the specific context (e.g., "Here are the approved brand guidelines for Project X") that the A2A agent needs to generate high-quality, compliant content.

By separating this into an MCP server, you can reuse these same tools across different agent interfaces (e.g., a web UI, a Slack bot, or Gemini Enterprise) without rewriting the core business logic.

## 3. How it is Secured & Consumed

### The Setup (Dynamic Client Registration)
To avoid manual exchange of API keys, the system uses **DCR**:
*   Gemini Enterprise calls your agent's DCR endpoint with a Google-signed JWT.
*   Your agent validates this request and automatically creates a new OAuth client ID and secret for that specific GE instance.

### The Runtime (OAuth 2.0 + A2A)
1.  **User Request**: A user asks Gemini Enterprise to generate a campaign.
2.  **Authentication**: GE redirects the user to your Identity Provider (IdP) to log in and grant permission (scopes like `agent:campaign`).
3.  **Execution**: GE receives a short-lived access token and sends it along with the message to your A2A Agent.
4.  **Orchestration**: Your A2A Agent receives the request, validates the token, and decides which tools to call on the MCP server to fulfill the request.
5.  **Delivery**: The result is returned to GE and displayed to the user.

## 5. Hosting Recommendation

As shown in the diagram, we recommend hosting the **A2A Agent** and the **MCP Server** in the **same Cloud Run container**:
*   **Communication**: They talk via local `stdio` pipes, which is fast and secure.
*   **Security**: The MCP server is not exposed to the internet; only the A2A agent is publicly accessible via authenticated A2A protocol calls.
