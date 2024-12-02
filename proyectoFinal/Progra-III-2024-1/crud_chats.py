import crud_proyectofinal

db = crud_proyectofinal.crud()

class crud_chats:
    def __init__(self):
        self.db = crud_proyectofinal.crud()  # Instancia de la conexión a la base de datos

    def agregar_contacto(self, user_sender, user_receiver):
        # Verificar si el contacto ya existe en la tabla de mensajes
        sql_verificar = """
            SELECT * FROM messages 
            WHERE (user_sender = %s AND user_receiver = %s)
               OR (user_sender = %s AND user_receiver = %s)
            LIMIT 1
        """
        valores_verificar = (user_sender, user_receiver, user_receiver, user_sender)
        resultado = self.db.consultar(sql_verificar, valores_verificar)

        if resultado:
            return "El contacto ya existe en el chat"

        # Si no existe, agregar un nuevo registro en la tabla de mensajes para establecer el contacto
        sql_agregar = """
            INSERT INTO messages (user_sender, user_receiver, message) 
            VALUES (%s, %s, 'Hola, Estoy Interesado')
        """
        valores_agregar = (user_sender, user_receiver)
        resultado_agregar = self.db.procesar_consultas(sql_agregar, valores_agregar)

        if resultado_agregar == "ok":
            return "Contacto agregado al chat"
        else:
            return f"Error al agregar contacto: {resultado_agregar}"

    def obtener_mensajes(self, user_sender, user_receiver):
        # Obtener los mensajes entre los dos usuarios
        sql = """
            SELECT * FROM messages 
            WHERE (user_sender = %s AND user_receiver = %s)
               OR (user_sender = %s AND user_receiver = %s)
            ORDER BY timestamp ASC
        """
        valores = (user_sender, user_receiver, user_receiver, user_sender)
        mensajes = self.db.consultar(sql, valores)

        return mensajes

    def enviar_mensaje(self, user_sender, user_receiver, mensaje):
        # Insertar un nuevo mensaje en la tabla de mensajes
        sql = """
            INSERT INTO messages (user_sender, user_receiver, message) 
            VALUES (%s, %s, %s)
        """
        valores = (user_sender, user_receiver, mensaje)
        resultado = self.db.procesar_consultas(sql, valores)

        if resultado == "ok":
            return "Mensaje enviado"
        else:
            return f"Error al enviar mensaje: {resultado}"
        
    def obtener_contactos(self, user_id):
        sql = """
            SELECT DISTINCT
                CASE
                    WHEN user_sender = %s THEN user_receiver
                    ELSE user_sender
                END AS contacto_id,
                users.NombreCompleto,
                users.imgPerfilUsuario
            FROM messages
            JOIN users ON users.user_id = CASE
                                            WHEN user_sender = %s THEN user_receiver
                                            ELSE user_sender
                                          END
            WHERE user_sender = %s OR user_receiver = %s
        """
        valores = (user_id, user_id, user_id, user_id)
        return self.db.consultar(sql, valores)