ARG GO_VERSION=1.26.1
ARG ALPINE_VERSION=3.20

FROM golang:${GO_VERSION}-alpine${ALPINE_VERSION} AS build
ARG SERVICE_PATH
ARG SERVICE_BINARY

RUN apk add --no-cache alpine-sdk

WORKDIR /workspace

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=1 GOOS=linux go build -o /out/${SERVICE_BINARY} ./${SERVICE_PATH}

FROM alpine:${ALPINE_VERSION} AS runtime
ARG SERVICE_BINARY

WORKDIR /app

COPY --from=build /out/${SERVICE_BINARY} /app/${SERVICE_BINARY}

CMD ["/bin/sh", "-lc", "exec /app/${SERVICE_BINARY}"]
