from flask import Flask, request, jsonify

# HTTP status codes for responses
SUCCESS = 200
CREATED = 201
BAD_REQUEST = 400
NOT_FOUND = 404
INTERNAL_ERROR = 500
NOT_IMPLEMENTED = 501
EXTERNAL_ERROR = 502

# Create a Flask application instance
app = Flask(__name__)

# Mock product data
mock_products = [
    {
        "id": 1,
        "name": "Product 1",
        "vend": "Vendor 1",
        "vend_address": "Address 1",
        "quantity": 100,
        "address": "Warehouse 1",
        "price_unit": 15.99
    },
    {
        "id": 2,
        "name": "Product 2",
        "vend": "Vendor 2",
        "vend_address": "Address 2",
        "quantity": 200,
        "address": "Warehouse 2",
        "price_unit": 25.99
    }
]

# Route to handle GET requests and retrieve all products 
@app.route("/products", methods=["GET"])
def get_product():
    try: 
        if not mock_products:
            return jsonify({"message": "No products found"}), NOT_FOUND
        
        return jsonify({"products": mock_products}), SUCCESS
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Route to handle POST requests and create a new product
@app.route("/products", methods=["POST"])
def post_product():
    try: 
        data = request.get_json()

        if not all(key in data for key in ["name", "vend", "quantity", "price_unit"]):
            return jsonify({"message": "Missing required fields"}), BAD_REQUEST

        new_product = {
            "id": len(mock_products) + 1,
            "name": data['name'],
            "vend": data['vend'],
            "vend_address": data.get('vend_address', None),
            "quantity": data['quantity'],
            "address": data.get('address', None),
            "price_unit": data['price_unit']
        }

        mock_products.append(new_product)

        return jsonify(new_product), CREATED
    
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Route to handle PUT requests and update an existing product
@app.route("/products", methods=["PUT"])
def update_product():
    try:
        product_id = request.args.get("id")

        if not product_id:
            return jsonify({"message": "Product ID is required"}), BAD_REQUEST

        data = request.get_json()

        if not all(key in data for key in ["name", "vend", "quantity", "price_unit"]):
            return jsonify({"message": "Missing required fields"}), BAD_REQUEST
        
        product = next((prod for prod in mock_products if prod["id"] == int(product_id)), None)

        if not product:
            return jsonify({"message": "Product not found"}), NOT_FOUND

        product["name"] = data['name']
        product["vend"] = data['vend']
        product["vend_address"] = data['vend_address']
        product["quantity"] = data['quantity']
        product["price_unit"] = data['price_unit']

        return jsonify(product), SUCCESS
    
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Route to handke DELETE requests and delete a product
@app.route("/products", methods=["DELETE"])
def delete_product():
    try: 
        product_id = int(request.args.get("id"))

        if not product_id:
            return jsonify({"message": "Product ID is required"}), BAD_REQUEST
        
        product = next((prod for prod in mock_products if prod["id"] == product_id), None)
        
        if not product:
            return jsonify({"message": "Product not found"}), NOT_FOUND
        
        mock_products.remove(product)

        return jsonify({"message": "Product deleted successfully"}), SUCCESS
    
    except Exception as e:
        return jsonify({"message": "Internal server error", "error": str(e)}), INTERNAL_ERROR

# Start the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)