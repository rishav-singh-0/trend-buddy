export function createLogger({ service }) {
  return {
    info(message, context = {}) {
      return { level: "info", service, message, context };
    },
    warn(message, context = {}) {
      return { level: "warn", service, message, context };
    },
    error(message, context = {}) {
      return { level: "error", service, message, context };
    }
  };
}
