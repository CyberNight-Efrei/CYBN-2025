FROM node:22

# Create app directory
WORKDIR /usr/src/app

# Copy over package.json and pnpm-lock.yaml
COPY src/package.json src/pnpm-lock.yaml ./

# Install app dependencies
RUN npm install -g pnpm
RUN pnpm install

# Copy app source code that is in src, in the main workdir and not workdir/src
COPY src ./

EXPOSE 8000
CMD [ "pnpm", "start" ]