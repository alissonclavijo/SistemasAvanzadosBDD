package config

import "github.com/alissonclavijo/migracion/db"

func GetPostgresConfig() db.Config {
	return db.Config{
		Host:     "localhost",
		Port:     5433,
		User:     "hamed",
		Password: "123456",
		DBName:   "hamed",
	}
}
