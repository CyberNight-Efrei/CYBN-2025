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

ENV JWT_SECRET="mq9DKA520sVdp5UOPKMe0TNxfOD8Ht0OE"
ENV FLAG="CYBN{J_41_gLyPs3_Ch3f!}"

EXPOSE 8000
CMD [ "pnpm", "start" ]