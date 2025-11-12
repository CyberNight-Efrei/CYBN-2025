FROM python:3.11-slim
WORKDIR /app
RUN pip install pycryptodome
COPY src/fastafboi_server.py /app/
EXPOSE 2222
CMD ["python", "/app/fastafboi_server.py"]
