from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS extension
import ephem
from PIL import Image
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set the observer's date to the current date
observer = ephem.Observer()

# Astrological sign for each body part
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

# Function to calculate planetary positions and astrological signs using whole sign houses
def calculate_planetary_positions():
    observer.date = ephem.now()
    planets_positions = {}

    for body_part, planet in astrological_signs.items():
        planet.compute(observer)

        if body_part in ['head', 'eyes', 'mouth', 'hoodie']:
            # Use ecliptic longitude for Sun, Mercury, Venus
            position = float(ephem.Ecliptic(planet).lon) * (180.0 / ephem.pi)
        else:
            # Use heliocentric longitude for other planets
            position = float(planet.hlong) * (180.0 / ephem.pi)

        # Ensure the position is within [0, 360)
        position = (position + 360) % 360
        # Convert position to degrees
        sign = int(position / 30) + 1  # Each zodiac sign is 30 degrees
        sign_name = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'][sign - 1]

        planets_positions[body_part] = {'position': position, 'sign': sign_name}
        print(f"Calculated sign for {body_part}: {sign_name}")

    return planets_positions

@app.route('/generate-image')


# Function to compose the image based on planetary positions
def compose_image():
    planets_positions = calculate_planetary_positions()

    # Load the background image
    background_path = "images/background.png"
    background = Image.open(background_path).convert("RGBA")

    # Paste the layers onto the background
    for body_part, data in planets_positions.items():
        sign = data['sign']

        # Construct the image layer path based on the current planet and astrological sign
        layer_path = f"images/{body_part}/{sign}.png"

        # Load the corresponding image layer
        try:
            layer_image = Image.open(layer_path).convert("RGBA")
            # Composite the layer onto the background
            background.paste(layer_image, (0, 0), layer_image)
        except FileNotFoundError:
            print(f"Image not found for {body_part} and {sign}")
            print(f"Layer path: {layer_path}")

    # Save the composed image
    output_path = "output/generated_images/output_image.png"
    background.save(output_path)
    print("Image composed successfully.")

# Function to continuously update the image and send planetary sign names to HTML
def continuously_update_image(interval_seconds):
    while True:
        observer.date = ephem.now()
        print(f"Updating image at {observer.date}")
        compose_image()
        time.sleep(interval_seconds)

# Call the function with a 4-hour interval
continuously_update_image(4 * 60 * 60)
















































