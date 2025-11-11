package main

import (
	"fmt"
	"io"
	"net"
	"net/http"
	"net/url"
	"strings"
	"time"

	"golang.org/x/net/http2"
)

func main() {
	baseURL := "http://127.0.0.1:5000/" //"http://127.0.0.1:5000"

	// Transport optimisé : keep-alive, pool de connexions, HTTP/2
	tr := &http.Transport{
		DialContext: (&net.Dialer{
			Timeout:   5 * time.Second,
			KeepAlive: 30 * time.Second,
		}).DialContext,
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 100,
		IdleConnTimeout:     90 * time.Second,
		DisableCompression:  true,
	}

	_ = http2.ConfigureTransport(tr)

	client := &http.Client{
		Transport: tr,
		Timeout:   5 * time.Second,
	}

	// Préparer les chaînes de corps de requête à l'avance
	emails := []string{"test@test.test", "admin@sandwicherie.fr", "test@test.test"}
	requestBodies := make([]string, len(emails))
	for i, e := range emails {
		form := url.Values{"email": {e}}
		requestBodies[i] = form.Encode()
	}

	startTotal := time.Now()
	for i, bodyStr := range requestBodies {
		// Créer un Reader à chaque itération
		reqBody := strings.NewReader(bodyStr)

		req, err := http.NewRequest("POST", baseURL+"/reset-request", reqBody)
		if err != nil {
			fmt.Printf("req %d error: %v\n", i, err)
			continue
		}
		req.Header.Set("Content-Type", "application/x-www-form-urlencoded")

		startReq := time.Now()
		resp, err := client.Do(req)
		duration := time.Since(startReq)

		if err != nil {
			fmt.Printf("req %d (%s) failed: %v\n", i, emails[i], err)
			continue
		}

		io.Copy(io.Discard, resp.Body)
		resp.Body.Close()

		fmt.Printf("req %d (%s) -> status %d, duration %v\n", i, emails[i], resp.StatusCode, duration)
	}

	fmt.Printf("Total elapsed: %v\n", time.Since(startTotal))
}
