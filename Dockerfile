# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install uv for fast dependency management
RUN pip install uv

# Install dependencies
# We use --system to install into the system Python environment in the container
RUN uv pip install --system google-adk[a2a]>=1.21.0 fastapi uvicorn mcp

# Expose the port the app runs on (Cloud Run defaults to 8080)
EXPOSE 8080

# Run the A2A server when the container launches
# This will serve the agent defined in a2a_agent.py
CMD ["adk", "api_server", "--a2a", "--port", "8080", "."]
