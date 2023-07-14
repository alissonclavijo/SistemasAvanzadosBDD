package main

import (
	"log"
	"time"

	"github.com/alissonclavijo/migracion/config"
	"github.com/alissonclavijo/migracion/db"
	"github.com/alissonclavijo/migracion/schemas"
)

func main() {
	// Configuración de PostgreSQL
	pgDB, err := db.Connect(config.GetPostgresConfig())
	if err != nil {
		log.Fatalf("Error al conectar a la base de datos: %v", err)
	}
	defer db.Close(pgDB)
	// Obtener una instancia del cliente de Firestore
	fsClient, err := db.NewFirestoreClient()
	if err != nil {
		log.Fatalf("Error al inicializar el cliente de Firestore: %v", err)
	}
	defer fsClient.Close()

	// Configuración de MongoDB
	mgoDB, err := db.SetupMongoDB()
	if err != nil {
		log.Fatal(err)
	}

	// Ejecutar la función
	for {
		err = schemas.MigrateReservaciones(pgDB, fsClient, mgoDB)
		if err != nil {
			log.Fatal(err)
		}

		// Esperar un tiempo antes de ejecutar la función nuevamente
		time.Sleep(time.Minute) // Puedes ajustar el intervalo según tus necesidades
	}
}
