import os
import io
from flask import Flask, jsonify, send_file, send_from_directory, make_response
from werkzeug.utils import safe_join
from flask_cors import CORS
import ephem
from PIL import Image
from config import ProductionConfig  
from dotenv import load_dotenv

# Get the absolute path to the 'images' directory
IMAGES_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images')


# Load environment variables from .env
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)  # Use ProductionConfig for production
    CORS(app)
    return app

app = create_app()

CORS(app, origins="*") 

observer = ephem.Observer()

astrological_signs = {
    'head': ephem.Sun(),
    'eyes': ephem.Moon(),
    'mouth': ephem.Mercury(),
    'hoodie': ephem.Venus(),
    'hands': ephem.Mars(),
    'legs': ephem.Jupiter(),
    'feet': ephem.Saturn(),
    'ball': ephem.Uranus(),
    'mushroom': ephem.Neptune(),
    'aura': ephem.Pluto(),
}

def calculate_planetary_positions():
    observer.date = ephem.now()
    planets_positions = {}

    for body_part, planet in astrological_signs.items():
        planet.compute(observer)

        if body_part in ['head', 'eyes', 'mouth', 'hoodie']:
            position = float(ephem.Ecliptic(planet).lon) * (180.0 / ephem.pi)
        else:
            position = float(planet.hlong) * (180.0 / ephem.pi)

        position = (position + 360) % 360
        sign = int(position / 30) + 1
        sign_name = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][sign - 1]

        planets_positions[body_part] = {'position': position, 'sign': sign_name}
        print(f"Calculated sign for {body_part}: {sign_name}")

    return planets_positions

def compose_image():
    planets_positions = calculate_planetary_positions()
    background_path = "images/background.png"
    background = Image.open(background_path).convert("RGBA")

    for body_part, data in planets_positions.items():
        sign = data['sign']
        layer_path = os.path.join(IMAGES_DIR, body_part, f"{sign.lower()}.png")
        print(f"Layer path for {body_part}: {layer_path}")

        try:
            layer_image = Image.open(layer_path).convert("RGBA")
            background.paste(layer_image, (0, 0), layer_image)
            print(f"Successfully added layer for {body_part} and {sign}")
        except FileNotFoundError:
            print(f"Image not found for {body_part} and {sign}")
            print(f"Layer path: {layer_path}")

    return background

@app.route('/api/planetary-signs')
def get_planetary_signs():
    planetary_signs = calculate_planetary_positions()
    return jsonify(planetary_signs)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/get-composed-image')
def get_composed_image():
    composed_image = compose_image()
    img_byte_array = io.BytesIO()
    composed_image.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    # Use send_file to send the image inline
    return send_file(img_byte_array, mimetype='image/png', as_attachment=False, download_name='composed_image.png')


if __name__ == '__main__':
    # Use Gunicorn for production deployment
    import multiprocessing
    workers = multiprocessing.cpu_count() * 2 + 1
    bind_address = '0.0.0.0:5000'
    gunicorn_cmd = f'gunicorn -w {workers} -b {bind_address} app:app'
    os.system(gunicorn_cmd)







