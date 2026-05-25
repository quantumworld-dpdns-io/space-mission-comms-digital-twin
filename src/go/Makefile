.PHONY: build test lint clean proto

build:
	go build ./...

test:
	go test ./... -v

lint:
	golangci-lint run ./...

proto:
	protoc --go_out=. --go-grpc_out=. proto/*.proto

clean:
	rm -rf bin/
	go clean -cache
