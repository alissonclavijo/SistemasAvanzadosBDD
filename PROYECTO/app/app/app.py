from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from psycopg2.errors import ForeignKeyViolation
import psycopg2
import uvicorn

class HotelCreate(BaseModel):
    id_hotel: str
    ubicacion_hotel: str
    numerohabitaciones_hotel: int
    categoria_hotel: str
    nombre_hotel: str


# Modelo de datos para la tabla Habitacion
class Habitacion(BaseModel):
    id_habitacion: str
    id_hotel: str
    tipo_habitacion: str
    precio_habitacion: float
    disponibilidad_habitacion: bool
    
app = FastAPI()

#hacer la coneccion en los 2 puertos, si uno se cae el otro debe levantar
connection = psycopg2.connect(
    host="gestionhotelesbdd",
    port=5432,
    user="hamed",
    password="123456",
    database="hamed"
)

# Ruta para obtener todos los hoteles
@app.get("/hoteles")
def get_hoteles():
    cursor = None  # Declarar cursor con valor inicial None
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener todos los hoteles de la base de datos
        select_query = "SELECT * FROM HOTEL"
        cursor.execute(select_query)
        hoteles = cursor.fetchall()
        hoteles_dict = []
        for hotel in hoteles:
            hotel_dict = {
                "id_hotel": hotel[0],
                "ubicacion_hotel": hotel[1],
                "numerohabitaciones_hotel": hotel[2],
                "categoria_hotel": hotel[3],
                "nombre_hotel": hotel[4]
            }
            hoteles_dict.append(hotel_dict)

        return {"hoteles": hoteles_dict}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener los hoteles: {str(error)}"}
    finally:
        if cursor is not None:  # Verificar si cursor no es None antes de cerrarlo
            cursor.close()

# Ruta para obtener todos los clientes
@app.get("/clientes")
def get_clientes():
    cursor = None  # Declarar cursor con valor inicial None
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener todos los clientes de la base de datos
        select_query = "SELECT * FROM CLIENTE"
        cursor.execute(select_query)
        clientes = cursor.fetchall()
        clientes_dict = []
        for cliente in clientes:
            cliente_dict = {
                "cedula_cliente": cliente[0],
                "apellidos_cliente": cliente[1],
                "nombres_cliente": cliente[2],
                "direccion_cliente": cliente[3],
                "telefono_cliente": cliente[4],
                "email_cliente": cliente[5],
                "numcuenta_cliente": cliente[6]
            }
            clientes_dict.append(cliente_dict)

        return {"clientes": clientes_dict}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener los clientes: {str(error)}"}
    finally:
        if cursor is not None:  # Verificar si cursor no es None antes de cerrarlo
            cursor.close()

# Ruta para obtener un hotel por su ID
@app.get("/hoteles/{id_hotel}")
def get_hotel(id_hotel: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener el hotel por su ID de la base de datos
        select_query = "SELECT * FROM HOTEL WHERE ID_HOTEL = %s"
        cursor.execute(select_query, (id_hotel,))
        hotel = cursor.fetchone()

        if not hotel:
            raise HTTPException(status_code=404, detail="Hotel no encontrado")

        return {"hotel": hotel}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener el hotel: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para obtener un cliente por su ID
@app.get("/clientes/{id_cliente}")
def get_cliente(id_cliente: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener el cliente por su ID de la base de datos
        select_query = "SELECT * FROM CLIENTE WHERE CEDULA_CLIENTE = %s"
        cursor.execute(select_query, (id_cliente,))
        cliente = cursor.fetchone()

        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Convertir el resultado en un diccionario
        cliente_dict = {
            "cedula": cliente[0],
            "apellidos": cliente[1],
            "nombres": cliente[2],
            "direccion": cliente[3],
            "telefono": cliente[4],
            "email": cliente[5],
            "num_cuenta": cliente[6]
        }

        return {"cliente": cliente_dict}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener el cliente: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para actualizar un hotel
@app.put("/hoteles/{id_hotel}")
def update_hotel(id_hotel: str, hotel: HotelCreate):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Actualizar el hotel en la base de datos
        update_query = """
        UPDATE HOTEL SET UBICACION_HOTEL = %s, NUMEROHABITACIONES_HOTEL = %s, CATEGORIA_HOTEL = %s, NOMBRE_HOTEL = %s
        WHERE ID_HOTEL = %s
        """
        cursor.execute(
            update_query,
            (hotel.ubicacion_hotel, hotel.numerohabitaciones_hotel, hotel.categoria_hotel, hotel.nombre_hotel, id_hotel)
        )

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Hotel actualizado exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al actualizar el hotel: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()
        
# Definir el modelo de datos del cliente
class ClienteUpdate(BaseModel):
    apellidos: str
    nombres: str
    direccion: str
    telefono: str
    email: str
    num_cuenta: float

# Ruta para actualizar un cliente
@app.put("/clientes/{id_cliente}")
def update_cliente(id_cliente: str, cliente: ClienteUpdate):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Actualizar el cliente en la base de datos
        update_query = """
        UPDATE CLIENTE SET APELLIDOS_CLIENTE = %s, NOMBRES_CLIENTE = %s, DIRECCION_CLIENTE = %s,
        TELEFONO_CLIENTE = %s, EMAIL_CLIENTE = %s, NUMCUENTA_CLIENTE = %s
        WHERE CEDULA_CLIENTE = %s
        """
        cursor.execute(
            update_query,
            (
                cliente.apellidos, cliente.nombres, cliente.direccion, cliente.telefono,
                cliente.email, cliente.num_cuenta, id_cliente
            )
        )

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Cliente actualizado exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al actualizar el cliente: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()
        
# si hotel esta en uso
def is_hotel_in_use(id_hotel):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Verificar si el ID_HOTEL está siendo utilizado en la tabla HABITACION
        cursor.execute("SELECT ID_HOTEL FROM HABITACION WHERE ID_HOTEL = %s", (id_hotel,))
        existing_habitaciones = cursor.fetchall()

        if existing_habitaciones:
            return True  # El ID_HOTEL está siendo utilizado en la tabla HABITACION
        else:
            return False  # El ID_HOTEL no está siendo utilizado

    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al verificar el uso del ID_HOTEL: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para eliminar un hotel
@app.delete("/hoteles/{id_hotel}")
def delete_hotel(id_hotel: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Verificar si el hotel está siendo utilizado por alguna habitación
        cursor.execute("SELECT ID_HOTEL FROM HABITACION WHERE ID_HOTEL = %s", (id_hotel,))
        existing_habitacion = cursor.fetchone()

        if existing_habitacion:
            return {"message": "No se puede eliminar, el hotel está siendo utilizado por una habitación"}

        # Eliminar el hotel de la base de datos
        delete_query = "DELETE FROM HOTEL WHERE ID_HOTEL = %s"
        cursor.execute(delete_query, (id_hotel,))

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Hotel eliminado exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al eliminar el hotel: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para eliminar un Cliente
@app.delete("/clientes/{cedula_cliente}")
def delete_cliente(cedula_cliente: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Verificar si la cédula del cliente está siendo utilizada en la tabla RESERVACION
        cursor.execute("SELECT CEDULA_CLIENTE FROM RESERVACION WHERE CEDULA_CLIENTE = %s", (cedula_cliente,))
        existing_reservacion = cursor.fetchone()

        if existing_reservacion:
            return {"message": "No se puede eliminar, la cédula del cliente está siendo utilizada en una reservación"}

        # Eliminar el cliente de la base de datos
        delete_query = "DELETE FROM CLIENTE WHERE CEDULA_CLIENTE = %s"
        cursor.execute(delete_query, (cedula_cliente,))

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Cliente eliminado exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al eliminar el cliente: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

#########################

# Crear un nuevo Hotel
@app.post("/hoteles")
def create_hotel(hotel: HotelCreate):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        cursor.execute("SELECT ID_HOTEL FROM HOTEL WHERE ID_HOTEL = %s", (hotel.id_hotel,))
        existing_hotel = cursor.fetchone()

        if existing_hotel:
            return {"message": "No se puede crear, ID de hotel ya existe"}

        # Validar la longitud del ID_HOTEL
        if len(hotel.id_hotel) > 5:
            return {"message": "El ID de hotel no puede tener más de 5 dígitos"}

        # Insertar el nuevo hotel en la base de datos
        insert_query = """
        INSERT INTO HOTEL (ID_HOTEL, UBICACION_HOTEL, NUMEROHABITACIONES_HOTEL, CATEGORIA_HOTEL, NOMBRE_HOTEL)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (hotel.id_hotel, hotel.ubicacion_hotel, hotel.numerohabitaciones_hotel, hotel.categoria_hotel, hotel.nombre_hotel)
        )

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Hotel creado exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al crear el hotel: {str(error)}"}
    finally:
        # Cerrar la conexión y el cursor
        cursor.close()

##########################

class ClienteCreate(BaseModel):
    cedula_cliente: str
    apellidos_cliente: str
    nombres_cliente: str
    direccion_cliente: str
    telefono_cliente: str
    email_cliente: str
    numcuenta_cliente: float = None

# Crear un nuevo Cliente
@app.post("/clientes")
def create_cliente(cliente: ClienteCreate):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Validar la longitud de la cédula del cliente
        if len(cliente.cedula_cliente) != 10:
            return {"message": "La cédula del cliente debe tener 10 dígitos"}

        # Validar la longitud del número de teléfono del cliente
        if len(cliente.telefono_cliente) > 10:
            return {"message": "El número de teléfono del cliente no puede tener más de 10 dígitos"}

        # Validar que todos los campos estén llenos
        if not all(vars(cliente).values()):
            return {"message": "Todos los campos son obligatorios"}

        cursor.execute("SELECT CEDULA_CLIENTE FROM CLIENTE WHERE CEDULA_CLIENTE = %s", (cliente.cedula_cliente,))
        hotel = cursor.fetchone()

        if hotel:
            return {"message": "No se puede crear, cédula ya existe"}

        # Insertar el nuevo cliente en la base de datos
        insert_query = """
        INSERT INTO CLIENTE (CEDULA_CLIENTE, APELLIDOS_CLIENTE, NOMBRES_CLIENTE, DIRECCION_CLIENTE, TELEFONO_CLIENTE, EMAIL_CLIENTE, NUMCUENTA_CLIENTE)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                cliente.cedula_cliente,
                cliente.apellidos_cliente,
                cliente.nombres_cliente,
                cliente.direccion_cliente,
                cliente.telefono_cliente,
                cliente.email_cliente,
                str(cliente.numcuenta_cliente)  # Convertir a cadena de caracteres
            )
        )

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Cliente creado exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al crear el cliente: {str(error)}"}
    finally:
        # Cerrar el cursor
      cursor.close()


# Ruta para obtener todas las habitaciones
@app.get("/habitaciones")
def get_habitaciones():
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener todas las habitaciones de la base de datos
        select_query = "SELECT * FROM HABITACION"
        cursor.execute(select_query)
        habitaciones = cursor.fetchall()

        # Convertir los resultados en una lista de diccionarios
        habitaciones_list = []
        for habitacion in habitaciones:
            habitacion_dict = {
                "id_habitacion": habitacion[0],
                "id_hotel": habitacion[1],
                "tipo_habitacion": habitacion[2],
                "precio_habitacion": habitacion[3],
                "disponibilidad_habitacion": habitacion[4]
            }
            habitaciones_list.append(habitacion_dict)

        return {"habitaciones": habitaciones_list}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener las habitaciones: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()


# Ruta para obtener una habitación por su ID
@app.get("/habitaciones/{id_habitacion}")
def get_habitacion(id_habitacion: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener la habitación por su ID de la base de datos
        select_query = "SELECT * FROM HABITACION WHERE ID_HABITACION = %s"
        cursor.execute(select_query, (id_habitacion,))
        habitacion = cursor.fetchone()

        if not habitacion:
            raise HTTPException(status_code=404, detail="Habitación no encontrada")

        # Convertir el resultado en un diccionario
        habitacion_dict = {
            "id_habitacion": habitacion[0],
            "id_hotel": habitacion[1],
            "tipo_habitacion": habitacion[2],
            "precio_habitacion": habitacion[3],
            "disponibilidad_habitacion": habitacion[4]
        }

        return habitacion_dict
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener la habitación: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para crear una nueva habitación
@app.post("/habitaciones")
def create_habitacion(habitacion: Habitacion):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Verificar si la habitación ya existe
        cursor.execute("SELECT ID_HABITACION FROM HABITACION WHERE ID_HABITACION = %s", (habitacion.id_habitacion,))
        existing_habitacion = cursor.fetchone()

        if existing_habitacion:
            return {"message": "No se puede crear, la habitación ya existe"}

        # Validar la longitud del campo ID_HABITACION
        if len(habitacion.id_habitacion) > 10:
            return {"message": "El ID_HABITACION no puede tener más de 10 dígitos"}

        # Validar que todos los campos estén llenos
        if not habitacion.id_habitacion or not habitacion.id_hotel or not habitacion.tipo_habitacion or not habitacion.precio_habitacion or not habitacion.disponibilidad_habitacion:
            return {"message": "Todos los campos deben estar llenos"}

        # Validar el campo PRECIO_HABITACION
        try:
            precio_habitacion = float(habitacion.precio_habitacion)
            if precio_habitacion <= 0:
                return {"message": "El PRECIO_HABITACION debe ser mayor que cero"}
        except ValueError:
            return {"message": "El PRECIO_HABITACION debe ser un número válido"}

        # Verificar si el ID_HOTEL existe en la tabla HOTEL
        cursor.execute("SELECT ID_HOTEL FROM HOTEL WHERE ID_HOTEL = %s", (habitacion.id_hotel,))
        existing_hotel = cursor.fetchone()

        if not existing_hotel:
            return {"message": "Ese hotel no está registrado"}

        # Insertar la nueva habitación en la base de datos
        insert_query = """
        INSERT INTO HABITACION (ID_HABITACION, ID_HOTEL, TIPO_HABITACION, PRECIO_HABITACION, DISPONIBILIDAD_HABITACION)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            insert_query,
            (
                habitacion.id_habitacion,
                habitacion.id_hotel,
                habitacion.tipo_habitacion,
                habitacion.precio_habitacion,
                habitacion.disponibilidad_habitacion
            )
        )

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Habitación creada exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al crear la habitación: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()


# Ruta para actualizar una habitación existente
@app.put("/habitaciones/{id_habitacion}")
def update_habitacion(id_habitacion: str, habitacion: Habitacion):
    with connection.cursor() as cur:
        cur.execute(
            "UPDATE HABITACION SET ID_HOTEL = %s, TIPO_HABITACION = %s, "
            "PRECIO_HABITACION = %s, DISPONIBILIDAD_HABITACION = %s "
            "WHERE ID_HABITACION = %s",
            (habitacion.id_hotel, habitacion.tipo_habitacion, habitacion.precio_habitacion,
             habitacion.disponibilidad_habitacion, id_habitacion)
        )
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Habitación no encontrada")
    connection.commit()
    return habitacion

# Ruta para eliminar una habitación
@app.delete("/habitaciones/{id_habitacion}")
def delete_habitacion(id_habitacion: str):
    with connection.cursor() as cur:
        cur.execute("DELETE FROM HABITACION WHERE ID_HABITACION = %s", (id_habitacion,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Habitación no encontrada")
    connection.commit()
    return {"message": "Habitación eliminada correctamente"}

# Ruta para obtener un pago por su ID de reserva
@app.get("/reserva/{id_reserva}")
def get_pago(id_reserva: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener el pago por su ID de reserva de la base de datos
        select_query = "SELECT * FROM PAGO WHERE ID_RESERVACION = %s"
        cursor.execute(select_query, (id_reserva,))
        pago = cursor.fetchone()

        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        # Convertir el resultado en un diccionario
        pago_dict = {
            "id_reservacion": pago[0],
            "id_habitacion": pago[1],
            "monto_pago": pago[2],
            "fecha_pago": pago[3].strftime("%Y-%m-%d") if pago[3] else None
        }

        return {"reserva": pago_dict}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener el reserva: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para obtener todas las reservaciones
@app.get("/reservaciones")
def get_reservaciones():
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener todas las reservaciones de la base de datos
        select_query = "SELECT * FROM RESERVACION"
        cursor.execute(select_query)
        reservaciones = cursor.fetchall()

        reservaciones_dict = []
        for reservacion in reservaciones:
            reservacion_dict = {
                "ID_RESERVACION": reservacion[0],
                "CEDULA_CLIENTE": reservacion[1],
                "ESTADO_RESERVACION": reservacion[2],
                "DETALLES_RESERVACION": reservacion[3].strftime("%Y-%m-%d")
            }
            reservaciones_dict.append(reservacion_dict)

        return {"reservaciones": reservaciones_dict}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al obtener las reservaciones: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()



# Ruta para crear una nueva reservación
@app.post("/reservaciones")
def create_reservacion(reservacion: dict):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Obtener los datos de la nueva reservación
        id_reservacion = reservacion.get("ID_RESERVACION")
        cedula_cliente = reservacion.get("CEDULA_CLIENTE")
        estado_reservacion = reservacion.get("ESTADO_RESERVACION")
        detalles_reservacion = reservacion.get("DETALLES_RESERVACION")

        # Verificar si el ID_RESERVACION ya existe en la base de datos
        cursor.execute("SELECT ID_RESERVACION FROM RESERVACION WHERE ID_RESERVACION = %s", (id_reservacion,))
        result = cursor.fetchone()
        if result:
            return {"message": "No se puede crear, ID_RESERVACION ya existe"}

        # Validar que la fecha de la reservación esté designada
        if not detalles_reservacion:
            return {"message": "La fecha de la reservación no está designada"}

        # Verificar si la cédula del cliente existe
        cursor.execute("SELECT CEDULA_CLIENTE FROM CLIENTE WHERE CEDULA_CLIENTE = %s", (cedula_cliente,))
        result = cursor.fetchone()
        if not result:
            return {"message": "La cédula del cliente no está registrada"}

        # Insertar la nueva reservación en la base de datos
        insert_query = "INSERT INTO RESERVACION (ID_RESERVACION, CEDULA_CLIENTE, ESTADO_RESERVACION, DETALLES_RESERVACION) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (id_reservacion, cedula_cliente, estado_reservacion, detalles_reservacion))

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Reservación creada exitosamente"}
    except ForeignKeyViolation:
        return {"message": "La cédula del cliente no está registrada"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al crear la reservación: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

# Ruta para eliminar una reservación por su ID
@app.delete("/reservaciones/{id_reservacion}")
def delete_reservacion(id_reservacion: str):
    try:
        # Crear un cursor
        cursor = connection.cursor()

        # Eliminar la reservación de la base de datos
        delete_query = "DELETE FROM RESERVACION WHERE ID_RESERVACION = %s"
        cursor.execute(delete_query, (id_reservacion,))

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Reservación eliminada exitosamente"}
    except (Exception, psycopg2.Error) as error:
        return {"message": f"Error al eliminar la reservación: {str(error)}"}
    finally:
        # Cerrar el cursor
        cursor.close()

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.get("/IndexClientes")
async def get_index():
    return FileResponse("IndexClientes.html")

@app.get("/IndexHabitacion")
async def get_index():
    return FileResponse("IndexHabitacion.html")

@app.get("/IndexReservacion")
async def get_index():
    return FileResponse("IndexReservacion.html")

@app.get("/IndexTotal")
async def get_index():
    return FileResponse("IndexTotal.html")

# Cerrar la conexión a la base de datos al finalizar la aplicación
@app.on_event("shutdown")
def shutdown():
    connection.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir acceso desde todos los dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



