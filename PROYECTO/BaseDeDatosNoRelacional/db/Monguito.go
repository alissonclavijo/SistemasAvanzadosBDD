package db

import (
	"github.com/globalsign/mgo"
)

func SetupMongoDB() (*mgo.Database, error) {
	// Configuración de MongoDB
	mgoSession, err := mgo.Dial("mongodb://localhost:27017")
	if err != nil {
		return nil, err
	}

	// Establecer opciones y configuraciones adicionales si es necesario

	// Obtener el objeto Database
	mgoDB := mgoSession.DB("hamed")

	return mgoDB, nil
}
