"""
API de Pokémon

Autor: Luis Álvaro Sanz de Ayala Oliver
Fecha: 13/07/2023

Esta API permite acceder y crear una serie de datos relacionados con los Pokémon.

Endpoints disponibles:
- GET /pokemonapi/<pokemon_id>: Obtiene un Pokémon por su ID.
- POST /pokemonapi: Crea un nuevo Pokémon.

"""
from flask import Flask, jsonify, request
import requests
# Instancia Flask
app = Flask(__name__)


pokemons = [
    {
        "id": 1,
        "name": "bulbasaur",
        "weight": 69,
        "types": ["grass", "poison"]
    }
]

# Función para obtener los 151 primeros Pokémon desde la PokeAPI
def fetch_pokemons():
    url = "https://pokeapi.co/api/v2/pokemon"
    params = {"limit": 151}  # Limitamos la cantidad de resultados a 151
    response = requests.get(url, params=params)
    
    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        data = response.json()
        pokemons = []
        
        # Recorrer los resultados y obtener los datos de cada Pokémon
        for result in data["results"]:
            pokemon_url = result["url"]
            pokemon_response = requests.get(pokemon_url)
            
            # Verificar si la solicitud del Pokémon fue exitosa
            if pokemon_response.status_code == 200:
                pokemon_data = pokemon_response.json()
                
                # Extraer los datos relevantes del Pokémon
                pokemon = {
                    "id": pokemon_data["id"],
                    "name": pokemon_data["name"],
                    "weight": pokemon_data["weight"],
                    "types": [t["type"]["name"] for t in pokemon_data["types"]]
                }
                
                # Agregar el Pokémon a la lista
                pokemons.append(pokemon)
        
        # Devolver la lista de Pokémon obtenidos
        return pokemons
    
    # Devolver None en caso de error en la solicitud
    return None

# Obtener los 151 primeros Pokémon al iniciar la API
pokemons = fetch_pokemons()







# Ruta GET: Obtención de un Pokémon a través de su ID
@app.route('/pokemonapi/<int:pokemon_id>', methods=['GET'])
def get_pokemon(pokemon_id):
    # Iteración de búsqueda por ID
    for pokemon in pokemons:
        if pokemon['id'] == pokemon_id:
            return jsonify(pokemon), 200
    # Mensaje de error 404: Pokemon no encontrado con el ID indicado
    return jsonify({'error 404': f'No se ha encontrado un Pokémon con ID:  {pokemon_id}.'}), 404


# Ruta POST: Creación de un nuevo Pokémon
@app.route('/pokemonapi', methods=['POST'])
def create_pokemon():
    # Obtención de la información del nuevo pokémon enviado
    pokemon = request.json
    # Verificación de ID libre
    for existing_pokemon in pokemons:
        if existing_pokemon['id'] == pokemon['id']:
            # Mensaje de error 400: No se puede satisfacer el requerimiento
            return jsonify({'error 400': 'Ya existe un Pokémon con el mismo ID.'}), 400
    # Agregar el nuevo pokémon a la lista de pokémons
    pokemons.append(pokemon)
    # Creación de recurso (201): Pokémon creado
    return jsonify(pokemon), 201

# Ejecutar la aplicación solo si este archivo es el punto de entrada principal
if __name__ == '__main__':
    app.run()
