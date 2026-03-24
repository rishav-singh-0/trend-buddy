FROM node:20-alpine

WORKDIR /app

COPY package.json ./
COPY apps ./apps
COPY packages ./packages

EXPOSE 3000

CMD ["npm", "run", "start"]
