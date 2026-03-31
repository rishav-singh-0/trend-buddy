ARG NODE_VERSION=20

FROM node:${NODE_VERSION}-slim AS build
WORKDIR /app

COPY apps/web/package*.json ./
RUN npm config set registry https://artifactory.arm.com/artifactory/api/npm/mirrors.npmjs_org
RUN npm install

COPY apps/web ./
RUN npm run build

FROM node:${NODE_VERSION}-slim AS runtime
WORKDIR /app

RUN npm config set registry https://artifactory.arm.com/artifactory/api/npm/mirrors.npmjs_org
RUN npm install -g serve

COPY --from=build /app/dist /app/dist

CMD ["serve", "-s", "/app/dist", "-l", "5173"]
