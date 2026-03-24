import { createApplication } from "./app.js";

export function startServer({ configOverrides = {} } = {}) {
  const app = createApplication({ configOverrides });

  return {
    app,
    async request(route, method, payload) {
      return app.handleRequest({ route, method, payload });
    }
  };
}
