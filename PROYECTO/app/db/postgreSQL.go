package db

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
)

// Config contiene la configuración de la conexión a la base de datos PostgreSQL.
type Config struct {
	Host     string
	Port     int
	User     string
	Password string
	DBName   string
}

// Connect establece una conexión a la base de datos PostgreSQL.
func Connect(config Config) (*sql.DB, error) {
	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		config.Host, config.Port, config.User, config.Password, config.DBName)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, fmt.Errorf("error al abrir la conexión a la base de datos: %v", err)
	}

	err = db.Ping()
	if err != nil {
		return nil, fmt.Errorf("error al conectar a la base de datos: %v", err)
	}

	log.Println("Conexión a la base de datos PostgreSQL establecida")

	return db, nil
}

// Close cierra la conexión a la base de datos PostgreSQL.
func Close(db *sql.DB) {
	err := db.Close()
	if err != nil {
		log.Printf("Error al cerrar la conexión a la base de datos: %v", err)
	} else {
		log.Println("Conexión a la base de datos PostgreSQL cerrada")
	}
}
