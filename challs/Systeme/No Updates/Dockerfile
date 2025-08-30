FROM debian:latest

USER root

RUN echo 'CYBN{Mak3_SUr3_T0_uPD4T3_yOuR_SYst3m_4Nd_PAck4G35}' > /root/flag.txt

COPY configure.sh /configure.sh
RUN /configure.sh
RUN rm -f /configure.sh

# WORKDIR /tmp
# RUn git config --global http.sslVerify false
# RUN git clone https://github.com/sudo-project/sudo/
# WORKDIR /tmp/sudo
# RUN git checkout 4d331e6026cc717b1472d4c3044d9885339e8cd4
# RUN ./configure && make && make check && make install
# RUN cd /
# RUN rm -rf /tmp/sudo

# Setup default command and/or parameters.
EXPOSE 2222
CMD ["/usr/bin/sudo", "/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"]