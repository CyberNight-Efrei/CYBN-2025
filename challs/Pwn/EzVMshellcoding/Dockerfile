FROM ubuntu:20.04

# Add 32-bit support and install tools
RUN dpkg --add-architecture i386 && \
    apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y gcc-multilib build-essential socat

WORKDIR /app

# Copy source, flag, Makefile
COPY src/ /app/src/
COPY flag.txt /app/flag.txt
COPY Makefile /app/

# Compile inside the container
RUN make

# Expose the port
EXPOSE 23457

# Run your binary through socat
CMD socat TCP-LISTEN:23457,reuseaddr,fork EXEC:"/app/vm",pty,stderr

