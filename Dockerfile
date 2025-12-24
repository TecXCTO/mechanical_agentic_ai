FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if any are needed (e.g., for specific CAD/CAE tools)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     <your-package> \
#     && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY notebooks/ ./notebooks/
COPY data/ ./data/
COPY tests/ ./tests/

# Install the project as a package (optional but good for imports)
RUN pip install .

# Expose ports if your application runs a server (e.g., for web UI)
# EXPOSE 8000

# Define environment variables (optional)
# ENV MY_VARIABLE=my_value

# Command to run the application
# This is a placeholder. You'd typically have a script to start the agent or a web server.
# CMD ["python", "src/main.py"]
CMD ["bash"] # Default command to keep container running for debugging
