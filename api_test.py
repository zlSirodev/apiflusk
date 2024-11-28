from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

profesores = [
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "cursos": [
            {
                "id": 1,
                "nombre": "Matemáticas",
                "codigo": "PGY0000",
                "seccion": "013V",
                "alumnos": [
                    {"id": 1, "nombre": "Luis","status":0},
                    {"id": 2, "nombre": "María","status":0},
                    {"id": 3, "nombre": "Pablo","status":0}
                ]
            },
            {
                "id": 2,
                "nombre": "Fisica",
                "codigo": "PGY0000",
                "seccion": "015V",
                "alumnos": [
                    {"id": 1, "nombre": "Luis", "status": 0},
                    {"id": 2, "nombre": "Maria", "status": 0}
                ]
            },
            {
                "id": 3,
                "nombre": "Quimica",
                "codigo": "PGY0000",
                "seccion": "018V",
                "alumnos": [
                    {"id": 1, "nombre": "Luis", "status": 0},
                    {"id": 2, "nombre": "Maria", "status": 0},
                    {"id": 3, "nombre": "Ernesto", "status": 0},
                    {"id": 4, "nombre": "Diana", "status": 0},
                    {"id": 5, "nombre": "Enrique", "status": 0},
                    {"id": 6, "nombre": "Abril", "status": 0}
                ]
            }
        ]
    },
    {
        "id": 3,
        "nombre": "Diego Cares",
        "cursos": [
            {
                "id": 1,
                "nombre": "Programacion de Apps Moviles",
                "codigo": "PGY4121",
                "seccion": "010V",
                "alumnos": [
                    {"id": 1, "nombre": "Juan Pablo","status":1},
                    {"id": 2, "nombre": "Diana","status":1},
                    {"id": 3, "nombre": "Jeremy","status":0}
                ]
            },
            {
                "id": 2,
                "nombre": "Calidad de Software",
                "codigo": "CSY4111",
                "seccion": "009V",
                "alumnos": [
                    {"id": 1, "nombre": "Juan Pablo","status":1},
                    {"id": 2, "nombre": "Diana","status":1},
                    {"id": 3, "nombre": "Jeremy","status":0},
                    {"id": 4, "nombre": "Gianna","status":1}
                ]
            }
        ]
    }
]


usuarios = [
    {
        "id": 1,
        "user": "docente",
        "password": "password1",
        "nombre": "Juan Perez",
        "perfil":  1,
        "correo": "docente@gmail.com"
    },
    {
        "id": 2,
        "user": "alumno",
        "password": "password2",
        "nombre": "Luis Gonzalez",
        "perfil": 2,
        "correo": "alumno@gmail.com"
    },
    {
        "id": 3,
        "user": "docente",
        "password": "password1",
        "nombre": "Diego Cares",
        "perfil":  1,
        "correo": "dcares@gmail.com"
    }
]


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('correo')
    password = request.json.get('password')
    
    usuario = next((u for u in usuarios if u["correo"] == username and u["password"] == password), None)
    
    if usuario:
        return jsonify({
            "id": usuario["id"],
            "nombre": usuario["nombre"],
            "user": usuario["user"],
            "correo": usuario["correo"],
            "tipoPerfil": usuario["perfil"]
        }), 200
    else:
        return jsonify({"message": "Credenciales incorrectas"}), 401


@app.route('/profesores', methods=['GET'])
def obtener_profesores():
    return jsonify(profesores), 200

# Los cursos dados un ID profesor
@app.route('/profesores/<int:profesor_id>/cursos', methods=['GET'])
def obtener_cursos_profesor(profesor_id):
    profesor = next((p for p in profesores if p["id"] == profesor_id), None)
    if not profesor:
        return jsonify({"message": "Profesor no encontrado"}), 404
    return jsonify(profesor["cursos"]), 200

# Endpoint: Los alumnos de un curso dado un ID profesor
@app.route('/profesores/<int:profesor_id>/cursos/<int:curso_id>/alumnos', methods=['GET'])
def obtener_alumnos_curso(profesor_id, curso_id):
    profesor = next((p for p in profesores if p["id"] == profesor_id), None)
    if not profesor:
        return jsonify({"message": "Profesor no encontrado"}), 404
    curso = next((c for c in profesor["cursos"] if c["id"] == curso_id), None)
    if not curso:
        return jsonify({"message": "Curso no encontrado"}), 404
    return jsonify(curso["alumnos"]), 200

#
@app.route('/registrar_asistencia', methods=['POST'])
def registrar_asistencia():
    alumno_id = request.json.get('alumno_id')
    codigo = request.json.get('codigo')
    seccion = request.json.get('seccion')
    fecha = request.json.get('fecha')
    
    # Aquí buscarías el curso y al alumno y actualizarías su estado.
    for profesor in profesores:
        for curso in profesor["cursos"]:
            if curso["codigo"] == codigo and curso["seccion"] == seccion:
                for alumno in curso["alumnos"]:
                    if alumno["id"] == alumno_id:
                        alumno["status"] = 1  # 1 es para presente
                        return jsonify({"message": "Asistencia registrada"}), 200
    
    return jsonify({"message": "No se pudo registrar la asistencia"}), 400


if __name__ == '__main__':
    app.run(debug=True)
