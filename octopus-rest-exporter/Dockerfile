FROM python:3.11-slim

WORKDIR /app

# Install required packages
RUN pip install requests prometheus_client flask

# Copy the exporter script
COPY octopus_exporter.py .

# Expose port
EXPOSE 9120

# Run the exporter
CMD ["python", "octopus_exporter.py"]
