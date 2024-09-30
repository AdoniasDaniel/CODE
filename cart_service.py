import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Link to product service on Render
PRODUCT_SERVICE_URL = 'https://product-service-qwwm.onrender.com'

# In-memory cart storage
memory = {}

# Get cart items for a user
@app.route('/cart/<user_id>', methods=['GET'])
def get_cart(user_id):
    cart_items = memory.get(user_id, [])
    result = []
    for item in cart_items:
        try:
            # Fetch product information from Product Service
            response = requests.get(f"{PRODUCT_SERVICE_URL}/products/{item['product_id']}")
            
            # Check if the request was successful
            if response.status_code != 200:
                return jsonify({"error": f"Failed to retrieve product details for product ID {item['product_id']}"}), response.status_code
            
            # Parse the product details as JSON
            product = response.json()
            
            # Append the product information to the result
            result.append({
                'product_name': product['name'],
                'quantity': item['quantity'],
                'total_price': product['price'] * item['quantity']
            })
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error communicating with Product Service: {str(e)}"}), 500
        except ValueError:
            return jsonify({"error": f"Invalid response from Product Service for product ID {item['product_id']}"}), 500
    return jsonify(result)


# Add product to cart for a user
@app.route('/cart/<user_id>/add/<int:product_id>', methods=['POST'])
def add_to_cart(user_id, product_id):
    cart_items = memory.setdefault(user_id, [])  # Get or create user cart
    for item in cart_items:
        if item['product_id'] == product_id:
            item['quantity'] += 1  # Increment quantity if already in cart
            return jsonify({"message": f"PRODUCT ID#: {product_id} QUANTITY UPDATED IN CART!"}), 201
    # Add new item to cart
    cart_items.append({'product_id': product_id, 'quantity': 1})
    return jsonify({"message": f"PRODUCT ID#: {product_id} WAS SUCCESSFULLY ADDED TO CART!"}), 201

# Remove product from cart for a user
@app.route('/cart/<user_id>/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(user_id, product_id):
    cart_items = memory.get(user_id, [])  # Fetch user cart
    for item in cart_items:
        if item['product_id'] == product_id:
            if item['quantity'] > 1:
                item['quantity'] -= 1  # Decrease quantity if more than one
            else:
                cart_items.remove(item)  # Remove item if quantity is one
            return jsonify({"message": f"PRODUCT ID#: {product_id} QUANTITY UPDATED/REMOVED FROM CART!"}), 200
    return jsonify({"error": "Item not found in cart"}), 404

# Run the cart app
if __name__ == '__main__':
    app.run(port=5001, debug=True)
