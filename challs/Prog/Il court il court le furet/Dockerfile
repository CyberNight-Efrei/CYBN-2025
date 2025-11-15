FROM python:3.11-alpine

LABEL authors="onelots"
ENV LANG="fr_FR.UTF-8"

# Challenge directory setup
## Switch working environment
WORKDIR /app
## Add application
COPY challenge .

# Python setup
## Upgrade pip
RUN python -m pip install --upgrade pip
## Install dependencies
RUN pip install -r requirements.txt
## Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# Expose port the server is reachable on
EXPOSE 8000

# Set flag
ENV FLAG="CYBN{FUR3T_U1TR4_R4P1D3_D3_Z1NZ1N}"

# Run Gunicorn on port 8002
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
