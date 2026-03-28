FROM node:20 AS build
WORKDIR /app

COPY package*.json ./
RUN npm config set registry https://artifactory.arm.com/artifactory/api/npm/mirrors.npmjs_org
RUN npm install

COPY . .
RUN npm run build

FROM node:23-slim AS runtime
WORKDIR /app

RUN npm config set registry https://artifactory.arm.com/artifactory/api/npm/mirrors.npmjs_org
RUN npm install -g serve

COPY --from=build /app/dist /app/dist

EXPOSE 5173
CMD ["serve", "-s", "/app/dist", "-l", "5173"]
