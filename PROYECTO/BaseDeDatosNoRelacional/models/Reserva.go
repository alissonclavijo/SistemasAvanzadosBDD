package models

type Reservacion struct {
	ID       string `json:"id" bson:"_id" firestore:"id"`
	Cedula   string `json:"cedula" bson:"cedula" firestore:"cedula"`
	Estado   string `json:"estado" bson:"estado" firestore:"estado"`
	Detalles string `json:"detalles" bson:"detalles" firestore:"detalles"`
}
