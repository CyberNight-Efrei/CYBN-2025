# ====== Base image ======
FROM python:3.12-slim

# ====== Set workdir ======
WORKDIR /app

# ====== Copy source code ======
COPY src/ ./

# ====== Expose port ======
EXPOSE 31337

# ====== Set environment variables ======
ENV PYTHONUNBUFFERED=1
ENV FLAG="CYBN{4V3C_T0uT_l3_R3SP3cT}"

# ====== Run the app with gunicorn ======
CMD ["python3", "app.py"]