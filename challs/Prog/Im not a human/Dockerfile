# ====== Base image ======
FROM python:3.12-slim

# ====== Set workdir ======
WORKDIR /app

# ====== Install dependencies ======
COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# ====== Copy source code ======
COPY src/ ./

# ====== Expose port ======
EXPOSE 5000

# ====== Set environment variables ======
ENV FLASK_ENV=production
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1
ENV FLAG="CYBN{C0ngr4tul4t10n_Y0u'r_N0t_4_Hum4n}"

# ====== Run the app with gunicorn ======
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "1", "--threads", "1"]
