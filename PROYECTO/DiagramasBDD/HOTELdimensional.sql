/*==============================================================*/
/* DBMS name:      PostgreSQL 8                                 */
/* Created on:     15/06/2023 12:59:09 p. m.                    */
/*==============================================================*/


drop index CLIENTE_PK;

drop table CLIENTE;

drop index TIENE_FK;

drop index HABITACION_PK;

drop table HABITACION;

drop index HOTEL_PK;

drop table HOTEL;

drop index INCLUYE2_FK;

drop index INCLUYE_FK;

drop index INCLUYE_PK;

drop table PAGO;

drop index HACE_FK;

drop index RESERVACION_PK;

drop table RESERVACION;

/*==============================================================*/
/* Table: CLIENTE                                               */
/*==============================================================*/
create table CLIENTE (
   CEDULA_CLIENTE       VARCHAR(10)          not null,
   APELLIDOS_CLIENTE    VARCHAR(50)          not null,
   NOMBRES_CLIENTE      VARCHAR(50)          not null,
   DIRECCION_CLIENTE    VARCHAR(50)          not null,
   TELEFONO_CLIENTE     VARCHAR(10)          not null,
   EMAIL_CLIENTE        VARCHAR(50)          not null,
   NUMCUENTA_CLIENTE    NUMERIC(50)          null,
   constraint PK_CLIENTE primary key (CEDULA_CLIENTE)
);

/*==============================================================*/
/* Index: CLIENTE_PK                                            */
/*==============================================================*/
create unique index CLIENTE_PK on CLIENTE (
CEDULA_CLIENTE
);

/*==============================================================*/
/* Table: HABITACION                                            */
/*==============================================================*/
create table HABITACION (
   ID_HABITACION        VARCHAR(50)          not null,
   ID_HOTEL             VARCHAR(50)           not null,
   TIPO_HABITACION      VARCHAR(50)          not null,
   PRECIO_HABITACION    NUMERIC(9,2)         not null,
   DISPONIBILIDAD_HABITACION BOOL                 not null,
   constraint PK_HABITACION primary key (ID_HABITACION)
);

/*==============================================================*/
/* Index: HABITACION_PK                                         */
/*==============================================================*/
create unique index HABITACION_PK on HABITACION (
ID_HABITACION
);

/*==============================================================*/
/* Index: TIENE_FK                                              */
/*==============================================================*/
create  index TIENE_FK on HABITACION (
ID_HOTEL
);

/*==============================================================*/
/* Table: HOTEL                                                 */
/*==============================================================*/
create table HOTEL (
   ID_HOTEL             VARCHAR(50)           not null,
   UBICACION_HOTEL      VARCHAR(50)          not null,
   NUMEROHABITACIONES_HOTEL INT4                 not null,
   CATEGORIA_HOTEL      VARCHAR(50)          not null,
   NOMBRE_HOTEL         VARCHAR(50)          not null,
   constraint PK_HOTEL primary key (ID_HOTEL)
);

/*==============================================================*/
/* Index: HOTEL_PK                                              */
/*==============================================================*/
create unique index HOTEL_PK on HOTEL (
ID_HOTEL
);

/*==============================================================*/
/* Table: PAGO                                                  */
/*==============================================================*/
create table PAGO (
   ID_RESERVACION       VARCHAR(50)          not null,
   ID_HABITACION        VARCHAR(50)          not null,
   MONTO_PAGO           DECIMAL(4,4)         null,
   FECHA_PAGO           DATE                 null,
   constraint PK_PAGO primary key (ID_RESERVACION, ID_HABITACION)
);

/*==============================================================*/
/* Index: INCLUYE_PK                                            */
/*==============================================================*/
create unique index INCLUYE_PK on PAGO (
ID_RESERVACION,
ID_HABITACION
);

/*==============================================================*/
/* Index: INCLUYE_FK                                            */
/*==============================================================*/
create  index INCLUYE_FK on PAGO (
ID_RESERVACION
);

/*==============================================================*/
/* Index: INCLUYE2_FK                                           */
/*==============================================================*/
create  index INCLUYE2_FK on PAGO (
ID_HABITACION
);

/*==============================================================*/
/* Table: RESERVACION                                           */
/*==============================================================*/
create table RESERVACION (
   ID_RESERVACION       VARCHAR(50)          not null,
   CEDULA_CLIENTE       VARCHAR(10)          not null,
   ESTADO_RESERVACION   CHAR(3)              not null
      constraint CKC_ESTADO_RESERVACIO_RESERVAC check (ESTADO_RESERVACION in ('Conf','Canc','Pend')),
   DETALLES_RESERVACION DATE                 not null,
   constraint PK_RESERVACION primary key (ID_RESERVACION)
);

comment on column RESERVACION.DETALLES_RESERVACION is
'se refierere a la fecha y hora de entrada, reseva y salida del hotel ';

/*==============================================================*/
/* Index: RESERVACION_PK                                        */
/*==============================================================*/
create unique index RESERVACION_PK on RESERVACION (
ID_RESERVACION
);

/*==============================================================*/
/* Index: HACE_FK                                               */
/*==============================================================*/
create  index HACE_FK on RESERVACION (
CEDULA_CLIENTE
);

alter table HABITACION
   add constraint FK_HABITACI_TIENE_HOTEL foreign key (ID_HOTEL)
      references HOTEL (ID_HOTEL)
      on delete restrict on update restrict;

alter table PAGO
   add constraint FK_PAGO_PAGO_RESERVAC foreign key (ID_RESERVACION)
      references RESERVACION (ID_RESERVACION)
      on delete restrict on update restrict;

alter table PAGO
   add constraint FK_PAGO_PAGO2_HABITACI foreign key (ID_HABITACION)
      references HABITACION (ID_HABITACION)
      on delete restrict on update restrict;

alter table RESERVACION
   add constraint FK_RESERVAC_HACE_CLIENTE foreign key (CEDULA_CLIENTE)
      references CLIENTE (CEDULA_CLIENTE)
      on delete restrict on update restrict;

