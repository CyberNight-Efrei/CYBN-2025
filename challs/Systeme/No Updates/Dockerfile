FROM debian:latest

USER root

RUN echo 'CYBN{Mak3_SUr3_T0_uPD4T3_yOuR_SYst3m_4Nd_PAck4G35}' > /root/flag.txt

COPY configure.sh /configure.sh
RUN chmod +x /configure.sh
RUN /configure.sh
RUN rm -f /configure.sh

# Setup default command and/or parameters.
EXPOSE 2222
CMD ["/usr/bin/sudo", "/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"]
