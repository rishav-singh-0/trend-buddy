import http from "node:http";

import { createApplication } from "./app.js";

const DEFAULT_PORT = Number(process.env.PORT ?? 3000);

function sendJson(response, statusCode, payload) {
  response.writeHead(statusCode, { "Content-Type": "application/json; charset=utf-8" });
  response.end(JSON.stringify(payload, null, 2));
}

function parseBody(request) {
  return new Promise((resolve, reject) => {
    let raw = "";

    request.on("data", (chunk) => {
      raw += chunk;
    });

    request.on("end", () => {
      if (!raw) {
        resolve({});
        return;
      }

      try {
        resolve(JSON.parse(raw));
      } catch (error) {
        reject(new Error("Request body must be valid JSON."));
      }
    });

    request.on("error", reject);
  });
}

export function createHttpServer({ port = DEFAULT_PORT, configOverrides = {} } = {}) {
  const app = createApplication({ configOverrides });
  const server = http.createServer(async (request, response) => {
    const url = new URL(request.url ?? "/", `http://${request.headers.host ?? "localhost"}`);
    const method = request.method ?? "GET";

    if (url.pathname === "/health") {
      sendJson(response, 200, {
        status: "ok",
        service: app.config.appName,
        environment: app.config.environment
      });
      return;
    }

    try {
      const payload = method === "GET" ? Object.fromEntries(url.searchParams) : await parseBody(request);
      const result = await app.handleRequest({
        route: url.pathname,
        method,
        payload
      });

      sendJson(response, 200, result);
    } catch (error) {
      const statusCode = error.message.startsWith("Unsupported route") ? 404 : 400;
      sendJson(response, statusCode, {
        error: error.message
      });
    }
  });

  return {
    app,
    server,
    start() {
      return new Promise((resolve) => {
        server.listen(port, () => {
          resolve({ port });
        });
      });
    }
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const httpServer = createHttpServer();
  httpServer.start().then(({ port }) => {
    process.stdout.write(`Trend Buddy API listening on port ${port}\n`);
  });
}
