FROM node:22-alpine

WORKDIR /workspace/apps/frontend

COPY package.json ./
RUN npm config set registry https://artifactory.arm.com/artifactory/api/npm/mirrors.npmjs_org
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
