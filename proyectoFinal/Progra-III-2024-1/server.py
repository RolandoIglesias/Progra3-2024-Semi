from flask import Flask, request, session, redirect, url_for, render_template, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import crud_auto
import crud_chats
import random
import json
import pickle
import numpy as np
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
import nltk
import unicodedata


if not os.path.exists('imagenes'):
    os.makedirs('imagenes')

app = Flask(__name__)

lemmatizer = WordNetLemmatizer()

app.secret_key = 'your_secret_key'  # Clave secreta para manejar sesiones

crudAuto = crud_auto.crud_auto()

crudChats = crud_chats.crud_chats()

intents = json.loads(open('intents.json', 'r', encoding='utf-8').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.h5')

# Ruta para el login (será lo primero que se mostrará al acceder a la app)
@app.route('/', methods=['GET', 'POST'])

   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')  # Obtener el correo del cuerpo de la solicitud
        password = request.json.get('password')  # Obtener la contraseña del cuerpo de la solicitud

        # Verificar si los campos no están vacíos
        if not username or not password:
            return jsonify({"msg": "Por favor, ingresa ambos campos (Correo y Contraseña)"}), 400

        # Verificar usuario en la base de datos
        usuarios = crudAuto.consultar()  # Asumiendo que 'consultar' obtiene todos los usuarios
        user_found = next((u for u in usuarios if u['username'] == username and u['password'] == password), None)

        # Validar ambos campos
        if not user_found:
            return jsonify({"msg": "Usuario o contraseña incorrectos"}), 400  # Mensaje único para error


        # Si las credenciales son correctas, guardar en la sesión y redirigir
        session['username'] = user_found['username']
        session['NombreCompleto'] = user_found['NombreCompleto']
        session['user_id'] = user_found['user_id']
        session['NumeroTelefono'] = user_found['NumeroTelefono']

        return jsonify({"msg": "ok"}), 200  # Login exitoso

    return render_template('login.html')  # Si es GET, mostrar el formulario de login

# Página principal que se muestra después de iniciar sesión
@app.route('/home')
def home():
    if 'username' in session:  # Verificamos si el usuario está logueado
        username = session.get('username', 'usuario')
        NombreCompleto = session.get('NombreCompleto', 'usuario')
        NumeroTelefono = session.get('NumeroTelefono', 'usuario')
        user_id = session.get('user_id', 'usuario')
        return render_template('home.html', NombreCompleto=NombreCompleto, NumeroTelefono=NumeroTelefono, username=username, user_id=user_id)  # Mostrar la página principal si está logueado
    else:
        return redirect(url_for('login'))  # Si no está logueado, redirigir al login

@app.route('/logout')
def logout():
    session.pop('username', None)  # Eliminar la sesión del usuario
    return redirect(url_for('login'))  # Redirigir al login

@app.route('/chats')
def chats():
    if 'username' in session:
        session_user_id = session.get('user_id')
        return render_template('chats.html', session_user_id=session_user_id)
    else:
        return redirect(url_for('login'))

@app.route('/agregar_contacto_chat', methods=['POST'])
def agregar_contacto_chat():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    data = request.get_json()
    user_receiver = data.get('user_id')
    user_sender = session.get('user_id')

    if not user_receiver:
        return jsonify({'error': 'Faltan datos'}), 400

    resultado = crudChats.agregar_contacto(user_sender, user_receiver)
    return jsonify({'msg': resultado})

# Ruta para obtener la lista de contactos del chat
@app.route('/obtener_contactos', methods=['GET'])
def obtener_contactos():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    user_id = session.get('user_id')
    contactos = crudChats.obtener_contactos(user_id)

    # Agregar una URL predeterminada si no hay imagen de perfil
    for contacto in contactos:
        if not contacto.get('imgPerfilUsuario'):
            contacto['imgPerfilUsuario'] = "/static/images/default-profile.png"

    return jsonify(contactos)

# Ruta para enviar un mensaje en el chat
@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    data = request.get_json()
    user_sender = session.get('user_id')
    user_receiver = data.get('user_receiver')
    mensaje = data.get('mensaje')

    if not all([user_sender, user_receiver, mensaje]):
        return jsonify({'error': 'Faltan datos para enviar el mensaje'}), 400

    resultado = crudChats.enviar_mensaje(user_sender, user_receiver, mensaje)
    return jsonify({'msg': resultado})

# Ruta para obtener los mensajes entre dos usuarios
@app.route('/obtener_mensajes', methods=['GET'])
def obtener_mensajes():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuario no autenticado'}), 403

    user_sender = session.get('user_id')
    user_receiver = request.args.get('user_receiver')

    if not user_receiver:
        return jsonify({'error': 'Faltan datos'}), 400

    mensajes = crudChats.obtener_mensajes(user_sender, user_receiver)
    return jsonify(mensajes)
    
def clean_up_sentence(sentence):
    # Convertir a minúsculas y eliminar tildes
    sentence = ''.join(
    c for c in unicodedata.normalize('NFD', sentence)
    if unicodedata.category(c) != 'Mn'
    )
    # Tokenizar la oración
    sentence_words = nltk.word_tokenize(sentence)
    # Lematizar las palabras
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i]=1
    return np.array(bag)

def predict_class(sentence, threshold=0.3):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    print("Predicciones:", res)
    
    # Revisa si alguna predicción supera el umbral
    max_prob = np.max(res)
    if max_prob < threshold:
        return "no_entendido"  # Una categoría genérica para entradas no claras
    
    max_index = np.argmax(res)
    category = classes[max_index]
    return category

def get_response(tag, intents_json):
    list_of_intents = intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            break
    return result

@app.route('/ia', methods=['GET', 'POST'])
def ia():
    if 'username' in session:  # Verificamos si el usuario está logueado
        return render_template('IA.html')  # Mostrar la página de IA si está logueado
    else:
        return redirect(url_for('login'))  # Si no está logueado, redirigir al login

# Ruta para obtener la respuesta del chatbot
@app.route("/get_response", methods=["POST"])
def chatbot_response():
    message = request.json['message']
    ints = predict_class(message)
    res = get_response(ints, intents)
    return jsonify({"response": res})


@app.route('/profile')
def profile():
    user_id = session.get('user_id')  # Obtener el user_id de la sesión

    if user_id:
        # Obtener datos del usuario
        user = crudAuto.obtener_usuario_por_id(user_id)

        # Obtener las publicaciones del usuario actual
        publicaciones = crudAuto.mostrar_publicacion_perfil(user_id)  # Pasar user_id

        if user:
            return render_template(
                'profile.html', 
                user=user, 
                user_logueado=user_id, 
                publicacion_perfil=publicaciones  # Publicaciones filtradas
            )
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))
        



@app.route('/eliminar_publicacion', methods=['POST'])
def eliminar_publicacion():
    
        data = request.get_json()
        publicacion_id = data.get('publicacion_id')
        print(f"ID de la publicación a eliminar: {publicacion_id}")

        # Crear un diccionario con el ID de la publicación
        datos = {"publicacion_id": publicacion_id}
        print(f"Datos a enviar: {datos}")

        # Lógica para eliminar la publicación en la base de datos
        crudAuto.eliminar_publicacion(publicacion_id) 

        return jsonify({'msg': 'Publicación eliminada exitosamente'})




@app.route('/quitar_favorito/<int:idPublicacion>', methods=['POST'])
def quitar_favorito(idPublicacion):
    user_id = session['user_id']  # Suponiendo que usas Flask-Login para manejar sesiones
   # Instancia de la clase crud_auto
    
    # Llama al método para quitar el favorito
    try:
        crudAuto.quitar_de_favoritos(user_id, idPublicacion)
        total_likes = crudAuto.contar_likes(idPublicacion)  # Actualiza el total de likes para sincronizar

        return jsonify({'msg': 'Publicación eliminada de favoritos.', 'total_likes': total_likes})
    except Exception as e:
        return jsonify({'msg': f'Error al eliminar favorito: {str(e)}'}), 400

        
        

       
    



@app.route('/edit_profile/<int:user_id>', methods=['GET', 'POST'])
def edit_profile(user_id):
    
    if request.method == 'GET':
        user = crudAuto.obtener_usuario_por_id(user_id)
        if user:
            return render_template('edit_profile.html', user=user)
        else:
            return "Usuario no encontrado", 404

    elif request.method == 'POST':
        user = crudAuto.obtener_usuario_por_id(user_id)
        if not user:
            return "Usuario no encontrado", 404

        username = request.form.get('username') or user['username']
        telefono = request.form.get('NumeroTelefono') or user['NumeroTelefono']
       



        # Manejar las imágenes
        profile_picture = request.files.get('profile_picture')
        background_image = request.files.get('background_image')
        

        upload_folder = 'static/imagenes/'
        profile_path = None
        background_path = None

        try:
            if profile_picture:
                profile_filename = secure_filename(profile_picture.filename)
                profile_path = os.path.join(upload_folder, profile_filename)
                profile_picture.save(profile_path)
                profile_path = f'/static/imagenes/{profile_filename}'
               

            if background_image:
                background_filename = secure_filename(background_image.filename)
                background_path = os.path.join(upload_folder, background_filename)
                background_image.save(background_path)
                background_path = f'/static/imagenes/{background_filename}'
                

        except Exception as e:
            print("Error al guardar las imágenes:", str(e))
            mensaje = "Ocurrió un error al intentar guardar las imágenes. Intente nuevamente."
            return render_template('edit_profile.html', user=user, mostrar_modal=True, mensaje=mensaje)

        # Actualizar el usuario en la base de datos
        crudAuto.actualizar_usuario(
            user_id,
            username,
            telefono,
            profile_path if profile_picture else None,
            background_path if background_image else None
        )

        # Actualizar los datos del usuario en la sesión
        user['username'] = username
        user['NumeroTelefono'] = telefono
        

            # Asegúrate de actualizar los datos antes de renderizar
        user['imgPerfilUsuario'] = profile_path if profile_path else user.get('imgPerfilUsuario')
        user['imgFondoUsuario'] = background_path if background_path else user.get('imgFondoUsuario')
       

        mensaje = "Sus datos se actualizaron correctamente."
        return render_template('edit_profile.html', user=user, mostrar_modal=True, mensaje=mensaje)
    
@app.route('/publicaciones_favoritas')
def publicaciones_favoritas():
    return render_template('publicaciones_favoritas.html')

@app.route('/RegistrarseLogin', methods=['GET', 'POST'])
def RegistrarseLogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        NombreCompleto = request.form['NombreCompleto']
        NumeroTelefono = request.form['NumeroTelefono']

        usuarios = crudAuto.consultar()

        for usuario in usuarios:
            if usuario['username'] == username:
                flash('El usuario ya existe')
                return render_template('RegistrarseLogin.html')

        # Crear un diccionario con los datos del usuario
        datos_usuario = {
            'username': username,
            'password': password,
            'NombreCompleto': NombreCompleto,
            'NumeroTelefono': NumeroTelefono
        }

        result = crudAuto.InsertarUsuario(datos_usuario)  # Pasar el diccionario a InsertarUsuario

        if result == "ok":
            flash('Usuario registrado exitosamente')
            return redirect(url_for('login'))
        else:
            flash(f'Error al registrar el usuario: {result}')
            return render_template('RegistrarseLogin.html')

    return render_template('RegistrarseLogin.html')



#Codigo para publicaciones: 

@app.route('/publicaciones')
def publicaciones():

    user_id = session.get('user_id', 'usuario')
    return render_template('publicaciones.html', user_id=user_id)  # Usa render_template en lugar de send_static_file

# Ruta para obtener las publicaciones en formato JSON
@app.route('/get_publicaciones')
def get_publicaciones():
    publicaciones = crudAuto.consultar_vehiculos()  # Obtener todas las publicaciones
    return jsonify(publicaciones)

# Ruta para servir imágenes
@app.route('/imagenes/<path:filename>')
def imagenes(filename):
    return send_from_directory('imagenes', filename)

@app.route('/EllenImagen/<path:filename>')
def ellen_imagen(filename):
    return send_from_directory('EllenImagen', filename)

# Ruta para manejar el envío de publicaciones

#aqui voy a comenzar :



@app.route('/subir_publicacion', methods=['POST'])
def subir_publicacion():
    user_id = session['user_id']
    nombre_vehiculo = request.form.get('nombre_vehiculo')
    precio = request.form.get('precio')
    descripcion = request.form.get('descripcion')
    comentario = request.form.get('Comentario')
    
    latitud = request.form.get('latitud')  
    longitud = request.form.get('longitud')  
    maps_url = request.form.get('maps_url')  
    map_image = request.form.get('map_image')  
    user_id = session.get('user_id')
    marca = request.form.get('marca')

    img_file1 = request.files.get('imgVehiculo')
    img_file2 = request.files.get('imgVehiculo2')

    # Validación de campos obligatorios
    if not (nombre_vehiculo and precio and descripcion and img_file1):
        return jsonify({'error': 'Faltan datos o imágenes requeridos'}), 400

    # Guardar las imágenes en el servidor
    img_filename1 = f"{nombre_vehiculo.replace(' ', '_')}_1.jpg"
    img_file1.save(os.path.join('imagenes', img_filename1))

    img_filename2 = None
    if img_file2:
        img_filename2 = f"{nombre_vehiculo.replace(' ', '_')}_2.jpg"
        img_file2.save(os.path.join('imagenes', img_filename2))

    # Insertar el registro en la base de datos
    datos = {
        'nombre_vehiculo': nombre_vehiculo,
        'precio': precio,
        'descripcion': descripcion,
        'Comentario': comentario,
        'imgVehiculo': img_filename1,
        'imgVehiculo2': img_filename2 if img_filename2 else '',
        'latitud': latitud,  # Asegúrate de que latitud esté definida
        'longitud': longitud,  # Asegúrate de que longitud esté definida
        'maps_url': maps_url, # Asegúrate de que maps_url esté definida
        'map_image': map_image,
        'user_id': user_id,
        'marca': marca
        
    }

    # Suponiendo que crudBD es una instancia de tu clase crud_BD
    resp = crudAuto.insertar_vehiculo(datos)

    return jsonify({'msg': 'Publicación agregada exitosamente'})

    
    
        


# Ruta para agregar un comentario
# Ruta para agregar un comentario
@app.route('/agregar_comentario', methods=['POST'])
def agregar_comentario():
    data = request.get_json()
    print(f"Datos recibidos: {data}")  # Agregar logging para depuración
    id_publicacion = data.get('id_publicacion')
    comentario = data.get('comentario')

    print(f"ID Publicación: {id_publicacion}, Comentario: {comentario}")  # Agrega esta línea


    if not (id_publicacion and comentario):
        return jsonify({'error': 'Faltan datos para el comentario'}), 400

    try:
        crudAuto.agregar_comentario(id_publicacion, comentario)
    except Exception as e:
        return jsonify({'error': f'Error al agregar comentario: {str(e)}'}), 500

    return jsonify({'msg': 'Comentario agregado exitosamente'})

# Ruta para editar un comentario
@app.route('/editar_comentario', methods=['POST'])
def editar_comentario():
    data = request.get_json()
    id_comentario = data.get('id_comentario')
    nuevo_comentario = data.get('nuevo_comentario')

    if not (id_comentario and nuevo_comentario):
        return jsonify({'error': 'Faltan datos para editar el comentario'}), 400

    try:
        crudAuto.editar_comentario(id_comentario, nuevo_comentario)  # Verifica que este método funcione
    except Exception as e:
        return jsonify({'error': f'Error al editar comentario: {str(e)}'}), 500

    return jsonify({'msg': 'Comentario editado exitosamente'})

# Ruta para eliminar un comentario
@app.route('/eliminar_comentario', methods=['POST'])
def eliminar_comentario():
    data = request.get_json()
    id_comentario = data.get('id_comentario')

    if not id_comentario:
        return jsonify({'error': 'Faltan datos para eliminar el comentario'}), 400

    try:
        crudAuto.eliminar_comentario(id_comentario)
    except Exception as e:
        return jsonify({'error': f'Error al eliminar comentario: {str(e)}'}), 500

    return jsonify({'msg': 'Comentario eliminado exitosamente'})



#Likes en las publicaciones:

@app.route('/like/<int:Id_Publicacion>', methods=['POST'])
def like_post(Id_Publicacion):
    user_id = session['user_id']  # Asume que el usuario está logueado y su ID está en la sesión
    like_status = request.json.get('like_status')  # True para dar like, False para quitar like

    # Verificar si el usuario ya ha dado like a esta publicación
    if like_status:
        # Dar like
        crudAuto.dar_like(user_id=user_id, Id_Publicacion=Id_Publicacion)
    else:
        # Quitar like
        crudAuto.quitar_like(user_id=user_id, Id_Publicacion=Id_Publicacion)

    # Retornar el número actualizado de likes
    total_likes = crudAuto.contar_likes(Id_Publicacion)

    return jsonify({'total_likes': total_likes})



#Ver el perfil del usuario:

@app.route('/ver_perfil/<int:user_id>')
def ver_perfil(user_id):
    user = crudAuto.obtener_usuario_por_id(user_id)  # Obtiene los datos del usuario
    publicaciones = crudAuto.mostrar_publicacion_perfil(user_id)  # Obtiene las publicaciones del usuario
    user_logueado = session.get('user_id')  # Usuario que inició sesión
    
    print(f"Usuario viendo: {user}, Usuario logueado: {user_logueado}")
    if user:
        # Renderiza el perfil con datos del usuario y sus publicaciones
        return render_template(
            'profile.html', 
            user=user, 
            user_logueado=user_logueado, 
            publicacion_perfil=publicaciones  # Publicaciones del usuario que estás viendo
        )
    else:
        return 'Usuario no encontrado'
    
@app.route('/get_favoritas', methods=['GET'])
def get_favoritas():
    try:
        user_id = session.get('user_id')  # Obtén el user_id de la sesión
        if not user_id:
            return jsonify({"error": "Usuario no autenticado"}), 401

        publicaciones_favoritas = crudAuto.obtener_publicaciones_favoritas(user_id)
        return jsonify(publicaciones_favoritas)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    

    
@app.route('/actualizar_comentarios', methods=['POST'])
def actualizar_comentarios():
    try:
        data = request.get_json()
        id_publicacion = data.get('id_publicacion')
        
        if not id_publicacion:
            return jsonify({"error": "Falta el id_publicacion"}), 400

        # Llamamos a la función para consultar los comentarios y demás datos de la publicación
        resultados = crudAuto.consultar_vehiculos()  # Esto devuelve los resultados de la consulta

        # Aquí puedes hacer algún procesamiento adicional si lo necesitas
        comentarios_data = []
        for publicacion in resultados:
            if publicacion['Id_Publicacion'] == id_publicacion:
                comentarios_data.append({
                    "comentarios": publicacion['Comentarios'],  # Esto es un ejemplo
                    "fechas": publicacion['Fechas'],  # Otro ejemplo
                    # Agrega más campos según lo que necesites
                })
        
        # Enviar los comentarios actualizados al frontend
        return jsonify({"comentarios": comentarios_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500




# Iniciar el servidor Flask

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002, debug= True)




