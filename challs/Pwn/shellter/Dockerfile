FROM debian:trixie-slim

RUN apt update && \
    apt install -y --no-install-recommends \
        fastfetch \
        gcc \
        build-essential \
        make \
        socat 

WORKDIR /app

COPY src/ /app/src/
COPY flag.txt /app/flag.txt
COPY Makefile /app/

RUN make

EXPOSE 23458

CMD ["socat", "TCP-LISTEN:23458,reuseaddr,fork", "EXEC:/app/main,pty,raw,stderr"]


