FROM node:18

# install MongoDB annoying dep...
RUN wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.1_1.1.1f-1ubuntu2_amd64.deb
RUN dpkg -i libssl1.1_1.1.1f-1ubuntu2_amd64.deb
# install MongoDB
RUN curl -fsSL https://www.mongodb.org/static/pgp/server-4.4.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/mongodb-archive-keyring.gpg] https://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update && apt-get install -y mongodb-org

# create MongoDB data directory
RUN mkdir -p /data/db

# create app directory
WORKDIR /usr/src/app

# copy over package.json and yarn.lock
COPY src/package*.json src/yarn.lock ./

RUN yarn install

# copy app source code that is in src, in the main workdir and not workdir/src
COPY src ./

ENV NODE_ENV=production \
    DATABASE=mongodb://localhost:27017/place \
    PORT=3000 \
    ONLY_LISTEN_LOCAL=true

# startup script
RUN echo '#!/bin/bash\n\
mongod --fork --logpath /var/log/mongodb.log --dbpath /data/db\n\
sleep 5\n\
yarn start\n' > /usr/src/app/start.sh

RUN chmod +x /usr/src/app/start.sh

EXPOSE 3000

CMD ["/usr/src/app/start.sh"]