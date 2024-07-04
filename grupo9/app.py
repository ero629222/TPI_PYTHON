from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://leo:Leo770077@localhost/crud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Modelo de usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'password': self.password
        }

# Crear la base de datos y la tabla
with app.app_context():
    db.create_all()

# Ruta principal renderiza el html
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint para obtener todos los registros (GET)
@app.route('/api/records', methods=['GET'])
def get_records():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

# Endpoint para crear un nuevo registro (POST)
@app.route('/api/records', methods=['POST'])
def add_record():
    data = request.json
    new_user = User(username=data['username'], name=data['name'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.serialize()), 201

# Endpoint para actualizar un registro (PUT)
#@app.route('/api/records/<int:id>', methods=['PUT'])
#def update_record(id):
#    data = request.json
#    user = User.query.get_or_404(id)
#    user.username = data['username']
#    user.name = data['name']
#    user.password = data['password']
#    db.session.commit()
#    return jsonify(user.serialize())

@app.put('/api/records/<int:id>')
def update_record(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user.username = data['username']
    user.name = data['name']
    user.password = data['password']
    db.session.commit()
    return jsonify(user.serialize())

# Endpoint para eliminar un registro (DELETE)
#@app.route('/api/records/<int:id>', methods=['DELETE'])
#def delete_record(id):
#    user = User.query.get_or_404(id)
#    db.session.delete(user)
#    db.session.commit()
#    return '', 204

@app.delete('/api/records/<int:id>')
def delete_record(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})



if __name__ == '__main__':
    app.run(debug=True)
