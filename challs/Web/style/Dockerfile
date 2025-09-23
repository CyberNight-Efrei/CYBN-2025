FROM node:18

# Create app directory
WORKDIR /usr/src/app

# Copy over package.json and yarn.lock
COPY src/package*.json src/yarn.lock ./

# Install app dependencies
RUN yarn install

# Copy app source code that is in src, in the main workdir and not workdir/src
COPY src ./

EXPOSE 3000
CMD [ "yarn", "start" ]