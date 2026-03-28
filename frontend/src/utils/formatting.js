export function formatLabel(value) {
  return `${value ?? ""}`
    .replace(/_/g, " ")
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

export function formatDuration(milliseconds) {
  if (milliseconds === null || milliseconds === undefined) {
    return "--";
  }

  if (milliseconds < 1000) {
    return `${Math.round(milliseconds)} ms`;
  }

  return `${(milliseconds / 1000).toFixed(2)} s`;
}

export function formatTimestamp(value) {
  if (!value) {
    return "Pending";
  }

  return new Intl.DateTimeFormat(undefined, {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    day: "2-digit",
    month: "short",
  }).format(new Date(value));
}

export function formatRelativeTime(value) {
  if (!value) {
    return "Awaiting first sweep";
  }

  const deltaSeconds = Math.max(0, Math.round((Date.now() - value) / 1000));

  if (deltaSeconds < 5) {
    return "just now";
  }

  if (deltaSeconds < 60) {
    return `${deltaSeconds}s ago`;
  }

  const deltaMinutes = Math.round(deltaSeconds / 60);

  if (deltaMinutes < 60) {
    return `${deltaMinutes}m ago`;
  }

  const deltaHours = Math.round(deltaMinutes / 60);
  return `${deltaHours}h ago`;
}

export function formatJson(value) {
  if (value === null || value === undefined || value === "") {
    return "Awaiting response payload...";
  }

  if (typeof value === "string") {
    return value;
  }

  return JSON.stringify(value, null, 2);
}

export function formatPercentage(successCount, totalCount) {
  if (!totalCount) {
    return "--";
  }

  return `${Math.round((successCount / totalCount) * 100)}%`;
}
