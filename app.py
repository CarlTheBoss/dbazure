from flask import Flask, render_template, request, jsonify
import os
import random
from core.assistant import procesar_comando

app = Flask(__name__)

# --- Rutas de Flask ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/comando', methods=['POST'])
def comando():
    data = request.get_json()
    comando_usuario = data.get('comando')
    if not comando_usuario:
        return jsonify({'respuesta': {'html': 'Por favor, envía un comando.', 'voz': 'Por favor, envía un comando.'}})

    respuesta_asis = procesar_comando(comando_usuario)
    return jsonify({'respuesta': respuesta_asis})

@app.route('/api/musica/aleatoria')
def musica_aleatoria():
    """
    Devuelve el nombre de un archivo de música aleatorio de la carpeta static/music.
    """
    try:
        music_dir = os.path.join(app.static_folder, 'music')
        songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        if not songs:
            return jsonify({'error': 'No se encontraron canciones.'}), 404
        
        random_song = random.choice(songs)
        return jsonify({'cancion': random_song})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)