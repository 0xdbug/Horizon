from astroquery.jplhorizons import Horizons
import json
import os

os.makedirs('output', exist_ok=True)

def get_planet_dance(planet_id, name, period=1, scale=255):
    step = '12h' if period <= 12 else f'{int(period/12)}d'
    epochs = {
        'start': '2024-01-01',
        'stop': f'{2024 + period}-01-01',
        'step': step
    }
    earth = Horizons(id='399', location='@0', epochs=epochs).vectors()
    planet = Horizons(id=planet_id, location='@0', epochs=epochs).vectors()
    relative_x = planet['x'] - earth['x']
    relative_y = planet['y'] - earth['y']
    max_value = max(max(abs(relative_x)), max(abs(relative_y)))
    scaled_x = (relative_x / max_value) * scale
    scaled_y = (relative_y / max_value) * scale
    coordinates = [
        {"x": float(x), "y": float(y)}
        for x, y in zip(scaled_x, scaled_y)
    ]
    filename = os.path.join('output', f'{name.lower()}_dance.json')
    with open(filename, 'w') as f:
        json.dump(coordinates, f, indent=2)
    return coordinates

planets = {
    '10': ('Sun', 1),
    '301': ('Moon', 1),
    '199': ('Mercury', 8),
    '299': ('Venus', 8),
    '499': ('Mars', 15),
    '599': ('Jupiter', 12),
    '699': ('Saturn', 30),
    '799': ('Uranus', 84),
    '899': ('Neptune', 165),
}

for planet_id, (name, period) in planets.items():
    coords = get_planet_dance(planet_id, name, period=period)
