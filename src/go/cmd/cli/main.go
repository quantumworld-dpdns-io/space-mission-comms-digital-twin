package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "sct-go",
	Short: "Space Comms Twin Go CLI",
	Long:  "Go-based CLI for the Space Mission Communications Digital Twin",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Space Comms Twin Go CLI v0.1.0")
	},
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
