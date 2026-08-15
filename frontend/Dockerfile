FROM node:24-alpine

WORKDIR /app

# chokidar-cli (used by watch:api-client) needs $SHELL set to run its command; Alpine's
# node image doesn't set one by default.
ENV SHELL=/bin/sh

RUN corepack enable

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

EXPOSE 3000

CMD ["pnpm", "dev"]
