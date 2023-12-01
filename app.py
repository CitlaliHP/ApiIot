from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///apiIot.db'
db = SQLAlchemy(app)

class Iot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispositivo = db.Column(db.String(80))
    valor = db.Column(db.Integer)

@app.route('/<int:id>', methods=['GET'])
def get_device(id):
    device = Iot.query.get(id)
    if device is None:
        return jsonify({'error': -1}), 404
    return jsonify({'id': device.id, 'dispositivo': device.dispositivo, 'valor': device.valor})

@app.route('/<int:id>/<int:value>', methods=['PATCH'])
def update_device(id, value):
    device = Iot.query.get(id)
    if device is None:
        return jsonify({'error': -1}), 404
    device.valor = value
    db.session.commit()
    return jsonify({'valor': device.valor})

if __name__ == '__main__':
    if not os.path.exists('apiIot.db'):
        db.create_all()
    app.run(debug=True, port=8000)