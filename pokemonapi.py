from flask import Flask, jsonify, request
import requests
import json

# Instancia Flask
app = Flask(__name__)

# Función para cargar los datos de la PokeAPI en el archivo pokemons.json
def load_pokemons():
    url = "https://pokeapi.co/api/v2/pokemon"
    params = {"limit": 151}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        pokemons = []

        for result in data["results"]:
            pokemon_url = result["url"]
            pokemon_response = requests.get(pokemon_url)

            if pokemon_response.status_code == 200:
                pokemon_data = pokemon_response.json()
                pokemon = {
                    "id": pokemon_data["id"],
                    "name": pokemon_data["name"],
                    "weight": pokemon_data["weight"],
                    "types": [t["type"]["name"] for t in pokemon_data["types"]]
                }
                pokemons.append(pokemon)

        # Guardar los datos de los Pokémon en el archivo pokemons.json
        with open('pokemons.json', 'w') as file:
            json.dump(pokemons, file)

# Cargar los datos de los Pokémon al iniciar la API
load_pokemons()

# Obtener los Pokémon desde el archivo pokemons.json
def fetch_pokemons():
    with open('pokemons.json', 'r') as file:
        pokemons = json.load(file)
    return pokemons

# Obtener los 151 primeros Pokémon al iniciar la API
pokemons = fetch_pokemons()

# Ruta GET: Obtención de un Pokémon a través de su ID
@app.route('/pokemonapi/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    for pokemon in pokemons:
        if pokemon['id'] == pokemon_id:
            return jsonify(pokemon), 200
    return jsonify({'error 404': f'No se ha encontrado un Pokémon con ID: {pokemon_id}.'}), 404

# Ruta POST: Creación de un nuevo Pokémon
@app.route('/pokemonapi', methods=['POST'])
def create_pokemon():
    pokemon = request.json
    for existing_pokemon in pokemons:
        if existing_pokemon['id'] == pokemon['id']:
            return jsonify({'error 400': 'Ya existe un Pokémon con el mismo ID.'}), 400
    pokemons.append(pokemon)
    return jsonify(pokemon), 201

# Ejecutar la aplicación solo si este archivo es el punto de entrada principal
if __name__ == '__main__':
    app.run()
