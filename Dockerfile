# build front-end
FROM node:lts-alpine AS frontend

RUN npm install pnpm -g

WORKDIR /app

COPY ./package.json /app

COPY ./pnpm-lock.yaml /app

RUN pnpm install

COPY . /app

RUN pnpm run build

# build backend
FROM node:lts-alpine as backend

RUN npm install pnpm -g

WORKDIR /app

COPY /service/node/package.json /app

COPY /service/node/pnpm-lock.yaml /app

RUN pnpm install

COPY /service/node /app

RUN pnpm build

# service
FROM node:lts-alpine

RUN npm install pnpm -g

WORKDIR /app

COPY /service/node/package.json /app

COPY /service/node/pnpm-lock.yaml /app

RUN pnpm install --production && rm -rf /root/.npm /root/.pnpm-store /usr/local/share/.cache /tmp/*

COPY /service/node /app

COPY --from=frontend /app/dist /app/public

COPY --from=backend /app/build /app/build

EXPOSE 9000

CMD ["pnpm", "run", "prod"]
