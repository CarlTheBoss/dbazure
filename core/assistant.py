import datetime
import wikipedia
import webbrowser
import os
import pywhatkit
from textblob import TextBlob
from core.database import get_db_connection

# Configuración inicial
wikipedia.set_lang("es")

def procesar_comando(query):
    """
    Procesa un comando de texto y devuelve respuestas para HTML y voz.
    """
    query = query.lower()
    respuesta_html = ""
    respuesta_voz = ""

    if "wikipedia" in query:
        query = query.replace("wikipedia", "").strip()
        try:
            texto_respuesta = wikipedia.summary(query, sentences=1)
            respuesta_html = texto_respuesta
            respuesta_voz = texto_respuesta
        except wikipedia.exceptions.PageError:
            respuesta_html = f"No pude encontrar nada en Wikipedia sobre '{query}'."
            respuesta_voz = respuesta_html
        except wikipedia.exceptions.DisambiguationError as e:
            respuesta_html = f"'{query}' es ambiguo. Podría referirse a: {e.options[:3]}"
            respuesta_voz = respuesta_html
    elif "google" in query:
        query = query.replace("google", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        respuesta_html = f"Buscando '{query}' en Google."
        respuesta_voz = respuesta_html
    elif "youtube" in query:
        song = query.replace("youtube", "").strip()
        # pywhatkit.playonyt(song) # No se puede usar en el servidor
        search_url = f"https://www.youtube.com/results?search_query={song.replace(' ', '+')}"
        respuesta_html = f'No puedo reproducir videos directamente, pero aquí tienes un enlace para buscar "{song}" en YouTube: <a href="{search_url}" target="_blank">Buscar en YouTube</a>'
        respuesta_voz = f'He preparado un enlace de búsqueda en YouTube para {song}.'
    elif "hora" in query or "tiempo" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        respuesta_html = f"La hora es {strTime}"
        respuesta_voz = respuesta_html
    elif "fecha" in query:
        strFecha = datetime.datetime.now().strftime('%d-%m-%Y')
        respuesta_html = f"La fecha de hoy es {strFecha}"
        respuesta_voz = respuesta_html
    elif "escribir" in query:
        respuesta_html = "Lo siento, la función de escribir a mano no está disponible en la versión web desplegada."
        respuesta_voz = respuesta_html
    elif "mensaje" in query:
        respuesta_html = "Lo siento, no puedo enviar mensajes de WhatsApp desde el servidor."
        respuesta_voz = respuesta_html
    elif "chiste" in query:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("select top 1 * from tchistes order by NEWID()")
                chiste = cursor.fetchone()
                if chiste:
                    respuesta_html = chiste[1]
                    respuesta_voz = chiste[1]
                else:
                    respuesta_html = "No encontré ningún chiste en la base de datos."
                    respuesta_voz = respuesta_html
                conn.close()
            except Exception as e:
                respuesta_html = f"Error al consultar la base de datos: {e}"
                respuesta_voz = respuesta_html
        else:
            respuesta_html = "No pude conectarme a la base de datos para contar un chiste."
            respuesta_voz = respuesta_html
            
    elif "lista de alumnos" in query:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("select nombres from tasistencia;")
                alumnos = cursor.fetchall()
                if alumnos:
                    lista_nombres = [alumno[0] for alumno in alumnos]
                    respuesta_html = "<ul>" + "".join(f"<li>{nombre}</li>" for nombre in lista_nombres) + "</ul>"
                    respuesta_voz = "Claro, la lista de alumnos es: " + ", ".join(lista_nombres)
                else:
                    respuesta_html = "No hay alumnos en la lista."
                    respuesta_voz = respuesta_html
                conn.close()
            except Exception as e:
                respuesta_html = f"Error al consultar la base de datos: {e}"
                respuesta_voz = respuesta_html
        else:
            respuesta_html = "No pude conectarme a la base de datos para obtener la lista."
            respuesta_voz = respuesta_html
    elif ("datos" in query and "curso" in query) or "cursos" in query:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Unir tcursos y tprofesores para obtener el nombre del profesor
                sql_query = """
                SELECT c.nombrecurso, p.nombresprofesor
                FROM tcursos c
                JOIN tprofesores p ON c.codprofesor = p.codprofesor;
                """
                cursor.execute(sql_query)
                cursos = cursor.fetchall()
                if cursos:
                    respuesta_html = "<strong>Lista de Cursos y Profesores:</strong><ul>"
                    respuesta_voz = "Claro, los cursos disponibles son: "
                    lista_cursos_voz = []
                    for curso in cursos:
                        respuesta_html += f"<li>{curso.nombrecurso} con el profesor {curso.nombresprofesor}</li>"
                        lista_cursos_voz.append(f"{curso.nombrecurso} con el profesor {curso.nombresprofesor}")
                    respuesta_html += "</ul>"
                    respuesta_voz += ". ".join(lista_cursos_voz)
                else:
                    respuesta_html = "No hay cursos registrados en la base de datos."
                    respuesta_voz = respuesta_html
                conn.close()
            except Exception as e:
                respuesta_html = f"Error al consultar los cursos: {e}"
                respuesta_voz = respuesta_html
        else:
            respuesta_html = "No pude conectarme a la base de datos para obtener los cursos."
            respuesta_voz = respuesta_html
    elif "asistencia" in query:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("select nombres, situacion from tasistencia;")
                alumnos = cursor.fetchall()
                if alumnos:
                    respuesta_html = "<strong>Resultado de la Asistencia:</strong><ul>"
                    respuesta_voz = "Claro, este es el estado de la asistencia: "
                    lista_asistencia_voz = []
                    for alumno in alumnos:
                        respuesta_html += f"<li>{alumno.nombres}: {alumno.situacion}</li>"
                        lista_asistencia_voz.append(f"{alumno.nombres}, {alumno.situacion}")
                    respuesta_html += "</ul>"
                    respuesta_voz += ". ".join(lista_asistencia_voz)
                else:
                    respuesta_html = "No hay alumnos registrados para pasar asistencia."
                    respuesta_voz = respuesta_html
                conn.close()
            except Exception as e:
                respuesta_html = f"Error al consultar la asistencia: {e}"
                respuesta_voz = respuesta_html
        else:
            respuesta_html = "No pude conectarme a la base de datos para pasar la asistencia."
            respuesta_voz = respuesta_html
    elif "objetivos" in query:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT titulo, contenido FROM tobjetivos")
                objetivo = cursor.fetchone()
                if objetivo:
                    respuesta_html = f"<strong>{objetivo.titulo}</strong><br>{objetivo.contenido.replace(chr(10), '<br>')}"
                    respuesta_voz = f"{objetivo.titulo}. {objetivo.contenido}"
                else:
                    respuesta_html = "No encontré objetivos en la base de datos."
                    respuesta_voz = respuesta_html
                conn.close()
            except Exception as e:
                respuesta_html = f"Error al consultar los objetivos: {e}"
                respuesta_voz = respuesta_html
        else:
            respuesta_html = "No pude conectarme a la base de datos para obtener los objetivos."
            respuesta_voz = respuesta_html
    elif "charla" in query:
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT titulo, contenido FROM tcharla")
                charla = cursor.fetchone()
                if charla:
                    respuesta_html = f"<strong>{charla.titulo}</strong><br>{charla.contenido.replace(chr(10), '<br>')}"
                    respuesta_voz = f"Charla de 5 minutos. {charla.titulo}. {charla.contenido}"
                else:
                    respuesta_html = "No encontré la charla en la base de datos."
                    respuesta_voz = respuesta_html
                conn.close()
            except Exception as e:
                respuesta_html = f"Error al consultar la charla: {e}"
                respuesta_voz = respuesta_html
        else:
            respuesta_html = "No pude conectarme a la base de datos para obtener la charla."
            respuesta_voz = respuesta_html
    elif "traduce el texto" in query:
        try:
            # Asumiendo que el archivo está en la raíz del proyecto
            with open("textoeningles.txt", "r", encoding="utf-8") as archivo:
                linea = archivo.read()
                blob = TextBlob(linea)
                texto_traducido = str(blob.translate(from_lang='en', to='es'))
                respuesta_html = f"<strong>Texto Original:</strong><br>{linea}<br><br><strong>Traducción:</strong><br>{texto_traducido}"
                respuesta_voz = f"La traducción es: {texto_traducido}"
        except FileNotFoundError:
            respuesta_html = "No encontré el archivo 'textoeningles.txt' para traducir."
            respuesta_voz = respuesta_html
        except Exception as e:
            respuesta_html = f"Ocurrió un error al traducir: {e}"
            respuesta_voz = respuesta_html
    elif "bienvenido" in query:
        respuesta_html = "Bien gracias, estoy listo para empezar."
        respuesta_voz = respuesta_html
    elif "gracias" in query:
        respuesta_html = "De nada, sigamos."
        respuesta_voz = respuesta_html
    elif "música" in query or "musica" in query:
        # Devolvemos un tipo de respuesta especial para que el frontend sepa que debe reproducir música
        respuesta_html = "Reproduciendo una canción aleatoria..."
        respuesta_voz = "Claro, poniendo algo de música."
        return {'html': respuesta_html, 'voz': respuesta_voz, 'accion': 'reproducir_musica'}
    elif "excel" in query:
        ruta_excel = '/static/excel/comandos.xlsx'
        respuesta_html = f'Claro, puedes descargar el archivo de comandos de Excel aquí: <a href="{ruta_excel}" download>Descargar Excel</a>'
        respuesta_voz = "He preparado el archivo de Excel para que lo descargues."
    elif "pausa" in query:
        respuesta_html = "De acuerdo, entraré en modo de pausa. Di 'activar' para continuar."
        respuesta_voz = "De acuerdo, entraré en modo de pausa. Di activar para continuar."
        return {'html': respuesta_html, 'voz': respuesta_voz, 'accion': 'pausa'}
    elif "activar" in query or "reanudar" in query:
        respuesta_html = "Micrófono reactivado."
        respuesta_voz = "Micrófono reactivado."
        return {'html': respuesta_html, 'voz': respuesta_voz, 'accion': 'activar'}
    elif "reiniciamos" in query:
        respuesta_html = "Ok, empecemos de nuevo."
        respuesta_voz = "Ok, empecemos de nuevo."
        return {'html': respuesta_html, 'voz': respuesta_voz, 'accion': 'reiniciar'}
    else:
        respuesta_html = "No entendí ese comando. Prueba con 'wikipedia', 'google', 'youtube', 'hora', 'fecha', 'escribir' o 'mensaje'."
        respuesta_voz = respuesta_html

    return {'html': respuesta_html, 'voz': respuesta_voz}