FROM node:22-bullseye

WORKDIR /app

# Install pnpm via volta
# Note: In Docker, we can install pnpm directly or use corepack, but sticking to requested tools if possible.
# However, simpler for dev container to just use corepack or npm to install pnpm globally.
# Let's use corepack which is standard in Node images now.
RUN corepack enable && corepack prepare pnpm@9.15.0 --activate

COPY package.json pnpm-lock.yaml ./
RUN pnpm install

CMD ["pnpm", "dev"]
