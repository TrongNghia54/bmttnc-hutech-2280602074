from flask import Flask, request, jsonify

from cipher.caesar import CaesarCipher
from cipher.vigenere.vigenere_cipher import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.transposition import TranspositionCipher # Thêm dòng này

app = Flask(__name__)

# CAESAR CIPHER ALGORITHM
caesar_cipher = CaesarCipher()

@app.route("/api/caesar/encrypt", methods=["POST"])
def caesar_encrypt():
    data = request.json
    plain_text = data.get('plain_text')
    key = data.get('key')

    if plain_text is None or key is None:
        return jsonify({"error": "Missing plain_text or key"}), 400
    try:
        key = int(key)
    except ValueError:
        return jsonify({"error": "Key must be an integer"}), 400

    encrypted_text = caesar_cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_message': encrypted_text})

@app.route("/api/caesar/decrypt", methods=["POST"])
def caesar_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text')
    key = data.get('key')

    if cipher_text is None or key is None:
        return jsonify({"error": "Missing cipher_text or key"}), 400
    try:
        key = int(key)
    except ValueError:
        return jsonify({"error": "Key must be an integer"}), 400

    decrypted_text = caesar_cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_message': decrypted_text})

# VIGENERE CIPHER ALGORITHM
vigenere_cipher = VigenereCipher()

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.json
    plain_text = data.get('plain_text')
    key = data.get('key')

    if plain_text is None or key is None:
        return jsonify({"error": "Missing plain_text or key"}), 400

    encrypted_text = vigenere_cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.json
    cipher_text = data.get('cipher_text')
    key = data.get('key')

    if cipher_text is None or key is None:
        return jsonify({"error": "Missing cipher_text or key"}), 400

    decrypted_text = vigenere_cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# RAIL FENCE CIPHER ALGORITHM
rail_fence_cipher = RailFenceCipher(3)

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt_api(): # Đổi tên hàm để tránh trùng lặp nếu có
    data = request.json
    plain_text = data.get('plain_text')

    if plain_text is None:
        return jsonify({"error": "Missing plain_text"}), 400

    encrypted_text = rail_fence_cipher.rail_fence_encrypt(plain_text)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt_api(): # Đổi tên hàm để tránh trùng lặp nếu có
    data = request.json
    cipher_text = data.get('cipher_text')

    if cipher_text is None:
        return jsonify({"error": "Missing cipher_text"}), 400

    decrypted_text = rail_fence_cipher.rail_fence_decrypt(cipher_text)
    return jsonify({'decrypted_text': decrypted_text})


# PLAYFAIR CIPHER ALGORITHM
playfair_cipher = PlayFairCipher()

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix_api():
    data = request.json
    key = data.get('key')

    if key is None:
        return jsonify({"error": "Missing key"}), 400

    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    return jsonify({'playfair_matrix': playfair_matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt_api():
    data = request.json
    plain_text = data.get('plain_text')
    key = data.get('key')

    if plain_text is None or key is None:
        return jsonify({"error": "Missing plain_text or key"}), 400

    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt_api():
    data = request.json
    cipher_text = data.get('cipher_text')
    key = data.get('key')

    if cipher_text is None or key is None:
        return jsonify({"error": "Missing cipher_text or key"}), 400
    
    if len(cipher_text) % 2 != 0:
        return jsonify({"error": "Cipher text length must be even for Playfair decryption. Please provide a valid encrypted text."}), 400

    playfair_matrix = playfair_cipher.create_playfair_matrix(key)
    decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
    return jsonify({'decrypted_text': decrypted_text})

# TRANSPOSITION CIPHER ALGORITHM
transposition_cipher = TranspositionCipher() # Thêm dòng này

@app.route('/api/transposition/encrypt', methods=['POST']) # Thêm route này
def transposition_encrypt(): # Thêm hàm này
    data = request.json #
    plain_text = data.get('plain_text') #
    key = data.get('key') #

    if plain_text is None or key is None:
        return jsonify({"error": "Missing plain_text or key"}), 400
    try:
        key = int(key)
    except ValueError:
        return jsonify({"error": "Key must be an integer"}), 400

    encrypted_text = transposition_cipher.encrypt(plain_text, key) #
    return jsonify({'encrypted_text': encrypted_text}) #

@app.route('/api/transposition/decrypt', methods=['POST']) # Thêm route này
def transposition_decrypt(): # Thêm hàm này
    data = request.json #
    cipher_text = data.get('cipher_text') #
    key = data.get('key') #

    if cipher_text is None or key is None:
        return jsonify({"error": "Missing cipher_text or key"}), 400
    try:
        key = int(key)
    except ValueError:
        return jsonify({"error": "Key must be an integer"}), 400
        
    decrypted_text = transposition_cipher.decrypt(cipher_text, key) #
    return jsonify({'decrypted_text': decrypted_text}) #


# Main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)