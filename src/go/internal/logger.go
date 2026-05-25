package internal

import (
	"os"

	"github.com/sirupsen/logrus"
)

var log *logrus.Logger

func InitLogger(level string) {
	log = logrus.New()
	log.SetFormatter(&logrus.JSONFormatter{})
	log.SetOutput(os.Stdout)

	lvl, err := logrus.ParseLevel(level)
	if err != nil {
		lvl = logrus.InfoLevel
	}
	log.SetLevel(lvl)
}

func GetLogger() *logrus.Logger {
	if log == nil {
		InitLogger("info")
	}
	return log
}
