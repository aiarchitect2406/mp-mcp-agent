# A2A + MCP Agent Sample for Typeface

This repository contains a sample implementation demonstrating how Typeface can front an existing **Model Context Protocol (MCP)** server with an **Agent-to-Agent (A2A)** layer to integrate with **Gemini Enterprise**.

This directly addresses the concern about orchestration shifting to the A2A layer by showcasing how the A2A agent handles multi-step reasoning and tool execution internally.

## 1. Architecture Overview

The following diagram showcases how the stack works, from procurement to consumption, including the security handshakes.

```mermaid
graph TD
    subgraph Google Cloud (Customer Tenant)
        User([🧑‍💻 End User])
        GE[🤖 Gemini Enterprise]
        MP[🛒 Google Cloud Marketplace]
    end

    subgraph ISV (Typeface) Tenant
        subgraph Cloud Run Container
            A2A[🤖 A2A Agent Head]
            MCP[🛠️ MCP Server]
        end
        IdP[🔐 Identity Provider / Auth]
        DB[(Typeface Data & APIs)]
    end

    %% Procurement Flow
    User -->|1. Procures Agent| MP
    MP -->|2. Notifies Entitlement| A2A
    
    %% Setup Flow (DCR)
    GE -->|3. Dynamic Client Registration| A2A
    A2A -->|4. Returns Credentials| GE

    %% Consumption & Security Flow
    User -->|5. Prompts 'Generate Campaign'| GE
    GE -->|6. OAuth Auth Code Flow| IdP
    IdP -->|7. Returns Access Token| GE
    GE -->|8. A2A SendMessage + Token| A2A
    A2A -->|9. Validates Token| IdP
    A2A -->|10. Calls Tools via stdio| MCP
    MCP -->|11. Fetches Assets| DB
    A2A -->|12. Returns Campaign| GE
    GE -->|13. Displays to User| User

    style A2A fill:#f9f,stroke:#333,stroke-width:2px
    style MCP fill:#bbf,stroke:#333,stroke-width:2px
    style GE fill:#dfd,stroke:#333,stroke-width:2px
    style MP fill:#fdd,stroke:#333,stroke-width:2px
```

## 2. Key Concepts

*   **A2A Agent (ADK)**: The public-facing gateway built with Google ADK. It receives high-level requests from Gemini Enterprise and orchestrates the calls to internal tools.
*   **MCP Server**: The tools layer that interacts with Typeface's internal data (resolving projects, layouts, and audiences).
*   **Co-location**: We recommend running both the A2A Agent and MCP Server in the same Cloud Run container, communicating via `stdio` for maximum security and performance.

## 3. Repository Structure

- `a2a_agent.py`: The A2A head agent with orchestration logic.
- `mcp_server.py`: Simulated MCP server exposing tools.
- `agent.json`: The Agent Card for discovery.
- `Dockerfile`: Packages the stack for Cloud Run.
- `terraform/`: Infrastructure as Code to deploy to GCP.
- `test_agent_card.py`: Test script to validate the Agent Card.
- `test_e2e_simulation.py`: Test script to simulate end-to-end orchestration with robustness scenarios.

## 4. Getting Started

For detailed instructions on how to build, deploy, and test this sample, please refer to the:
👉 **[USER_GUIDE.md](USER_GUIDE.md)**

For more details on security (OAuth, DCR) and Marketplace listing, see:
👉 **[MARKETPLACE_GUIDE.md](MARKETPLACE_GUIDE.md)**
