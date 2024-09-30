# CMSC 455 Assignment #2 - Adonias Daniel
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory product storage
memory = []
product_counter = 1

# Get all products or add a new one
@app.route('/products', methods=['GET', 'POST'])
def products():
    global product_counter
    if request.method == 'GET':
        return jsonify(memory)  # Return all products
    
    elif request.method == 'POST':
        new_product = {
            'id': product_counter,
            'name': request.json['name'],
            'price': request.json['price'],
            'quantity': request.json['quantity']
        }
        product_counter += 1
        memory.append(new_product)  # Add new product to memory
        return jsonify(new_product), 201

# Get a product by its ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((product for product in memory if product['id'] == product_id), None)
    if product:
        return jsonify(product)  # Return the product if found
    return jsonify({'ERROR': 'PRODUCT NOT FOUND'}), 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
