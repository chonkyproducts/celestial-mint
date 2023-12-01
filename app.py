import os 
from flask import Flask, jsonify, send_file, render_template
from werkzeug.utils import safe_join
from flask_cors import CORS
import ephem
from PIL import Image
import io
import time

app = Flask(__name__)
app.template_folder = os.path.abspath('templates')
CORS(app)

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
        layer_path = f"images/{body_part}/{sign}.png"

        try:
            layer_image = Image.open(layer_path).convert("RGBA")
            background.paste(layer_image, (0, 0), layer_image)
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
    return render_template('index.html')

@app.route('/get-composed-image')
def get_composed_image():
    composed_image = compose_image()

    # Specify the download name for the attachment
    download_name = 'composed_image.png'

    # Use safe_join to ensure the filename is safe
    download_path = safe_join(app.root_path, 'downloads', download_name)

    # Save the image to the specified path
    composed_image.save(download_path, format='PNG')

    # Send the file with the specified download name
    return send_file(download_path, mimetype='image/png', as_attachment=True, download_name=download_name)

if __name__ == '__main__':
    app.run(debug=True)


