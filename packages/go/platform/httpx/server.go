package httpx

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os/signal"
	"syscall"
	"time"
)

// NewServer creates an HTTP server with the shared timeout defaults.
func NewServer(port int, handler http.Handler) *http.Server {
	return &http.Server{
		Addr:         fmt.Sprintf(":%d", port),
		Handler:      handler,
		IdleTimeout:  time.Minute,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 30 * time.Second,
	}
}

// ListenAndServe runs the server and performs graceful shutdown on SIGINT/SIGTERM.
func ListenAndServe(server *http.Server) error {
	done := make(chan error, 1)

	go func() {
		ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
		defer stop()

		<-ctx.Done()
		log.Println("shutting down gracefully, press Ctrl+C again to force")
		stop()

		shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		done <- server.Shutdown(shutdownCtx)
	}()

	err := server.ListenAndServe()
	if err != nil && err != http.ErrServerClosed {
		return err
	}

	shutdownErr := <-done
	if shutdownErr != nil {
		return shutdownErr
	}

	log.Println("graceful shutdown complete")
	return nil
}
