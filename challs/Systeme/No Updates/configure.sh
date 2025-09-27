apt-get -qq update \
    && apt-get -qq --no-install-recommends install sudo \
    && apt-get -qq --no-install-recommends install gcc \
    && apt-get -qq --no-install-recommends install libc6-dev \
    && apt-get -qq --no-install-recommends install make \
    && apt-get -qq --no-install-recommends install git \
    && apt-get -qq --no-install-recommends install libssl-dev \
    && apt-get -qq --no-install-recommends install nano \
    && apt-get -qq --no-install-recommends install vim \
    && apt-get -qq --no-install-recommends install openssh-server \
    && apt-get -qq clean    \
    && rm -rf /var/lib/apt/lists/*

useradd -rm -d /home/user -s /bin/bash user
echo 'user:user' | chpasswd

echo 'Be careful to never update the server, because internet is dangerous! Stay disconnected!!!' > /root/warning.txt

echo "
sudo cat /root/warning.tkt
sudo --version
sudo cat /root/warning.txt
ls
ls -al
cd ..
exit
" > /home/user/.bash_history

# Define marches as recgnised ssh marches
echo 'Match User user' >> /etc/sshd_config
echo 'Port 2222' >> /etc/ssh/sshd_config

echo "user ALL=(ALL) NOPASSWD: /bin/cat /root/warning.txt" >> /etc/sudoers

# Remove read and executable permissions for the users.
chmod go-rx /usr/bin/passwd
chmod go-rx /usr/sbin/chpasswd

cd /tmp
git config --global http.sslVerify false
git clone https://github.com/sudo-project/sudo/
cd sudo
git checkout 4d331e6026cc717b1472d4c3044d9885339e8cd4
./configure && make && make check && make install
cd /
rm -rf /tmp/sudo*
