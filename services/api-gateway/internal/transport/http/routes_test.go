package transporthttp

import (
	"io"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHandler(t *testing.T) {
	handler := NewHandler(nil)
	req, err := http.NewRequest(http.MethodGet, "/", nil)
	if err != nil {
		t.Fatalf("error making request to server. Err: %v", err)
	}
	resp := httptest.NewRecorder()
	http.HandlerFunc(handler.helloWorldHandler).ServeHTTP(resp, req)

	if resp.Code != http.StatusOK {
		t.Errorf("expected status OK; got %v", resp.Code)
	}
	expected := "{\"message\":\"Hello World\"}"
	body, err := io.ReadAll(resp.Result().Body)
	if err != nil {
		t.Fatalf("error reading response body. Err: %v", err)
	}
	if expected+"\n" != string(body) {
		t.Errorf("expected response body to be %v; got %v", expected, string(body))
	}
}
