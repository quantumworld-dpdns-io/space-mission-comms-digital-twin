package internal

import "os"

type Config struct {
	GRPCPort     string
	PythonAPIURL string
	LogLevel     string
}

func LoadConfig() *Config {
	return &Config{
		GRPCPort:     getEnv("GO_GRPC_PORT", "50051"),
		PythonAPIURL: getEnv("PYTHON_API_URL", "http://localhost:8000"),
		LogLevel:     getEnv("LOG_LEVEL", "info"),
	}
}

func getEnv(key, fallback string) string {
	if val := os.Getenv(key); val != "" {
		return val
	}
	return fallback
}
