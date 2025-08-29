from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)


USER_INFO = {
    "user_id": "asim_sahoo_22072004",
    "email": "asim2018off@gmail.com",
    "roll_number": "22BCE10267"
}

def categorize_data(data_array):

    odd_numbers = []
    even_numbers = []
    alphabets = []
    special_characters = []

    for item in data_array:
        if isinstance(item, str):
            # Check if it's a number
            if item.isdigit():
                num = int(item)
                if num % 2 == 0:
                    even_numbers.append(item)
                else:
                    odd_numbers.append(item)
            # Check if it's alphabetic
            elif item.isalpha():
                alphabets.append(item.upper())
            # If it's not a number or alphabet, it's a special character
            elif not item.isalnum():
                special_characters.append(item)

    return odd_numbers, even_numbers, alphabets, special_characters

def calculate_sum(data_array):

    total = 0
    for item in data_array:
        if isinstance(item, str) and item.isdigit():
            total += int(item)
    return str(total)

def create_concat_string(data_array):
    # Extract all alphabetic characters
    alphabets = []
    for item in data_array:
        if isinstance(item, str):
            for char in item:
                if char.isalpha():
                    alphabets.append(char.lower())

    # Reverse the order
    alphabets.reverse()

    # Apply alternating caps (starting with uppercase for first char)
    result = ""
    for i, char in enumerate(alphabets):
        if i % 2 == 0:
            result += char.upper()
        else:
            result += char.lower()

    return result

@app.route('/bfhl', methods=['POST'])
def process_data():

    try:
        # Get JSON data from request
        json_data = request.get_json()

        if not json_data or 'data' not in json_data:
            return jsonify({
                "is_success": False,
                "error": "Invalid input: 'data' field is required"
            }), 400

        data_array = json_data['data']

        if not isinstance(data_array, list):
            return jsonify({
                "is_success": False,
                "error": "Invalid input: 'data' must be an array"
            }), 400

        # Process the data
        odd_numbers, even_numbers, alphabets, special_characters = categorize_data(data_array)
        sum_result = calculate_sum(data_array)
        concat_string = create_concat_string(data_array)

        # Prepare response
        response = {
            "is_success": True,
            "user_id": USER_INFO["user_id"],
            "email": USER_INFO["email"],
            "roll_number": USER_INFO["roll_number"],
            "odd_numbers": odd_numbers,
            "even_numbers": even_numbers,
            "alphabets": alphabets,
            "special_characters": special_characters,
            "sum": sum_result,
            "concat_string": concat_string
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "is_success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({
        "operation_code": 1
    }), 200

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "message": "BFHL API is running",
        "status": "healthy"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
