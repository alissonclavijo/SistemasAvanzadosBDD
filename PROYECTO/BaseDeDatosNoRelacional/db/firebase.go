package db

import (
	"context"
	"log"

	"cloud.google.com/go/firestore"
	"google.golang.org/api/option"
)

// FirestoreClient representa el cliente de Firestore.
type FirestoreClient struct {
	client *firestore.Client
}

// NewFirestoreClient crea una nueva instancia del cliente de Firestore.
func NewFirestoreClient() (*firestore.Client, error) {
	ctx := context.Background()
	projectID := "gestionhotelesexamen"
	credentialFile := "credential.json"
	opt := option.WithCredentialsFile(credentialFile)
	client, err := firestore.NewClient(ctx, projectID, opt)
	if err != nil {
		return nil, err
	}

	return client, nil
}

// Close cierra la conexión con Firestore.
func (fc *FirestoreClient) Close() {
	err := fc.client.Close()
	if err != nil {
		log.Printf("Error al cerrar la conexión con Firestore: %v", err)
	}
}


