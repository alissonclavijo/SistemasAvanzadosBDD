package schemas

import (
	"context"
	"database/sql"
	"log"

	"cloud.google.com/go/firestore"
	"github.com/alissonclavijo/migracion/models"
	"github.com/globalsign/mgo"
)

func MigrateReservaciones(pgDB *sql.DB, fsClient *firestore.Client, mgoDB *mgo.Database) error {
	// Consultar datos de la tabla Reservacion en PostgreSQL
	rows, err := pgDB.Query("SELECT * FROM reservacion")
	if err != nil {
		return err
	}
	defer rows.Close()

	// Migrar datos a Firebase Firestore y MongoDB
	for rows.Next() {
		var reservacion models.Reservacion
		err := rows.Scan(
			&reservacion.ID,
			&reservacion.Cedula,
			&reservacion.Estado,
			&reservacion.Detalles,
		)
		if err != nil {
			return err
		}

		// Migrar a Firebase Firestore
		_, err = fsClient.Collection("reservaciones").Doc(reservacion.ID).Set(context.Background(), reservacion)
		if err != nil {
			return err
		}

		// Migrar a MongoDB
		err = mgoDB.C("reservaciones").Insert(reservacion)
		if err != nil {
			log.Printf(err.Error())
		}
	}

	return nil
}
