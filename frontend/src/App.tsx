import { useCallback, useMemo, useState } from "react";
import "./App.css";

type ApiSuccess = {
  message?: string;
};

type HealthResponse = Record<string, unknown>;

type RequestState =
  | { status: "idle" }
  | { status: "loading"; endpoint: string }
  | { status: "success"; endpoint: string; data: unknown }
  | { status: "error"; endpoint: string; code?: number; message: string };

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.trim() || "http://localhost:8081";

function App() {
  const [requestState, setRequestState] = useState<RequestState>({
    status: "idle",
  });

  const rootEndpoint = useMemo(() => `${API_BASE_URL}/`, []);
  const healthEndpoint = useMemo(() => `${API_BASE_URL}/health`, []);

  const requestJson = useCallback(async <T,>(endpoint: string): Promise<T> => {
    setRequestState({ status: "loading", endpoint });

    try {
      const response = await fetch(endpoint, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });

      const rawBody = await response.text();
      let parsedBody: unknown = null;

      if (rawBody) {
        try {
          parsedBody = JSON.parse(rawBody);
        } catch {
          parsedBody = rawBody;
        }
      }

      if (!response.ok) {
        const message =
          typeof parsedBody === "string"
            ? parsedBody
            : (parsedBody as { message?: string } | null)?.message ||
              response.statusText ||
              "Request failed";

        setRequestState({
          status: "error",
          endpoint,
          code: response.status,
          message,
        });

        throw new Error(message);
      }

      setRequestState({
        status: "success",
        endpoint,
        data: parsedBody,
      });

      return parsedBody as T;
    } catch (error) {
      if (error instanceof Error) {
        setRequestState((current) =>
          current.status === "error"
            ? current
            : {
                status: "error",
                endpoint,
                message: error.message || "Network request failed",
              },
        );
      } else {
        setRequestState({
          status: "error",
          endpoint,
          message: "Unexpected error",
        });
      }

      throw error;
    }
  }, []);

  const checkApi = useCallback(async () => {
    await requestJson<ApiSuccess>(rootEndpoint);
  }, [requestJson, rootEndpoint]);

  const checkHealth = useCallback(async () => {
    await requestJson<HealthResponse>(healthEndpoint);
  }, [requestJson, healthEndpoint]);

  const statusTone =
    requestState.status === "success"
      ? "success"
      : requestState.status === "error"
        ? "error"
        : requestState.status === "loading"
          ? "loading"
          : "idle";

  return (
    <main
      style={{
        minHeight: "100vh",
        display: "grid",
        placeItems: "center",
        padding: "2rem",
        boxSizing: "border-box",
      }}
    >
      <section
        style={{
          width: "100%",
          maxWidth: 760,
          background: "var(--bg)",
          border: "1px solid var(--border)",
          borderRadius: 16,
          padding: "2rem",
          boxShadow: "var(--shadow)",
          textAlign: "left",
        }}
      >
        <div style={{ display: "grid", gap: "0.75rem" }}>
          <p
            style={{
              margin: 0,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              fontSize: 12,
              fontWeight: 700,
              color: "var(--accent)",
            }}
          >
            Trend Buddy
          </p>

          <h1 style={{ margin: 0 }}>API status dashboard</h1>

          <p style={{ fontSize: 16, lineHeight: 1.6 }}>
            This UI replaces the broken starter demo and gives you a safe way to
            verify whether the backend is responding or returning a 500 error.
          </p>
        </div>

        <div
          style={{
            marginTop: "1.5rem",
            display: "grid",
            gap: "1rem",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
          }}
        >
          <button
            onClick={checkApi}
            disabled={requestState.status === "loading"}
            style={buttonStyle}
          >
            Check root endpoint
          </button>

          <button
            onClick={checkHealth}
            disabled={requestState.status === "loading"}
            style={buttonStyle}
          >
            Check health endpoint
          </button>
        </div>

        <div
          style={{
            marginTop: "1.5rem",
            padding: "1rem",
            borderRadius: 12,
            border: `1px solid ${
              statusTone === "success"
                ? "rgba(34, 197, 94, 0.35)"
                : statusTone === "error"
                  ? "rgba(239, 68, 68, 0.35)"
                  : statusTone === "loading"
                    ? "rgba(59, 130, 246, 0.35)"
                    : "var(--border)"
            }`,
            background:
              statusTone === "success"
                ? "rgba(34, 197, 94, 0.08)"
                : statusTone === "error"
                  ? "rgba(239, 68, 68, 0.08)"
                  : statusTone === "loading"
                    ? "rgba(59, 130, 246, 0.08)"
                    : "transparent",
          }}
        >
          <h2 style={{ marginTop: 0 }}>Current status</h2>

          {requestState.status === "idle" && (
            <p>
              No request has been made yet. Use one of the buttons above to test
              the backend.
            </p>
          )}

          {requestState.status === "loading" && (
            <p>
              Checking <code>{requestState.endpoint}</code>...
            </p>
          )}

          {requestState.status === "success" && (
            <div style={{ display: "grid", gap: "0.75rem" }}>
              <p>
                Request to <code>{requestState.endpoint}</code> completed
                successfully.
              </p>
              <pre style={preStyle}>
                {JSON.stringify(requestState.data, null, 2)}
              </pre>
            </div>
          )}

          {requestState.status === "error" && (
            <div style={{ display: "grid", gap: "0.75rem" }}>
              <p style={{ margin: 0, color: "#ef4444", fontWeight: 700 }}>
                {requestState.code
                  ? `HTTP ${requestState.code}`
                  : "Request failed"}
              </p>
              <p style={{ margin: 0 }}>
                Endpoint: <code>{requestState.endpoint}</code>
              </p>
              <p style={{ margin: 0 }}>{requestState.message}</p>
            </div>
          )}
        </div>

        <div
          style={{
            marginTop: "1.5rem",
            display: "grid",
            gap: "0.5rem",
          }}
        >
          <h2 style={{ marginBottom: 0 }}>Configuration</h2>
          <p>
            Backend base URL: <code>{API_BASE_URL}</code>
          </p>
          <p style={{ fontSize: 14, opacity: 0.8 }}>
            You can override this with <code>VITE_API_BASE_URL</code>.
          </p>
        </div>
      </section>
    </main>
  );
}

const buttonStyle: React.CSSProperties = {
  appearance: "none",
  border: "1px solid var(--border)",
  borderRadius: 12,
  padding: "0.9rem 1rem",
  fontSize: 16,
  fontWeight: 600,
  cursor: "pointer",
  background: "var(--accent)",
  color: "#fff",
};

const preStyle: React.CSSProperties = {
  margin: 0,
  padding: "1rem",
  borderRadius: 12,
  overflowX: "auto",
  background: "var(--code-bg)",
  color: "var(--text-h)",
  fontSize: 14,
  lineHeight: 1.5,
};

export default App;
