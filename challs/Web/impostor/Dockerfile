FROM mongo:4.4.29

# install latest nodejs (22) and yarn
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - && \
    echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list && \
    apt-get update && apt-get install -y yarn

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