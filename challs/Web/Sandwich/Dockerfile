FROM python:3.13-alpine

WORKDIR /app

COPY src /app
RUN pip3 install -r requirements.txt --break-system-packages

RUN chmod +x start.sh

ENV FLAG="CYBN{1_pR3f3r_cH3e53_S4ndWIcH_Th4N_Uu1D_S4nDW1Ch}"
ENV SECRET_KEY="yUmfY1OcnsaQsjq4FwjgkrUnKBQzssLFH2Q4xWNoy7aNgFtoEHzBfpiYoMWdFyGs8saLuSuZEkqW1qsQTZ8wbw"
ENV ADMIN_PASSWORD="o5itVhuDTvHNqZze2hJKrEjMoRXpTxbB"
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1


EXPOSE 8000

CMD ["./start.sh"]