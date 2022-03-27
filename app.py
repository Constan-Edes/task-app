from logging import exception
from re import search
from turtle import title
from unittest import result
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Tasks
from datetime import datetime
from logging import exception


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db\\tasks.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# ======== Aqui empiezan las rutas ========
# ======== Agrega una tarea ========
@app.route('/')
def home():
    tareas = Tasks.query.all()
    tareas.__str__()
    print(tareas)
    return render_template('index.html', tareas=tareas)



# Agrega una tarea 
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    try:

        if request.method == 'GET':
            return render_template('agregar.html')
        # if request is not GET
        else:
            tarea = request.form.get('tarea')
            ya_completada = request.form.get('completada')
            fecha = datetime.today().strftime('%Y-%m-%d')

            if ya_completada:
                status = 'Completada'
            else:
                status = 'Pendiente'
            
            tarea_nueva = Tasks(tarea, fecha, status)
            db.session.add(tarea_nueva)
            db.session.commit()

            return redirect(url_for('home'))
           
    
    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500
   

# Muestra todas las tareas 
@app.route('/tareas')
def get_tareas():
    try:
        tareas = Tasks.query.all()
        tareas_json = [tarea.serialize()  for tarea in tareas]
        return jsonify(tareas_json), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500
   

# Muestra las tareas completadas
@app.route('/completadas')
def get_completadas():
    try:
        tareas = Tasks.query.all()
        tareas_json = []
        for tarea in tareas:
            if tarea.status == 'Completada':
                tareas_json.append(tarea.serialize())

        return jsonify(tareas_json), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500
   

# Muestra las tareas pendientes
@app.route('/incompletas')
def get_incompletas():
    try:
        tareas = Tasks.query.all()
        tareas_json = []
        for tarea in tareas:
            if tarea.status == 'Pendiente':
                tareas_json.append(tarea.serialize())

        return jsonify(tareas_json), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500
   

# busca las tareas por titulo
@app.route('/busqueda', methods=['GET'])
def busqueda_titulo():
    try:
        search_title = request.args['title']
        resultado = Tasks.query.filter(Tasks.title.like('%' + search_title + '%')).first()
        # task = Tasks.query.filter_by(status=search_title).first()

        if resultado:
            return jsonify(resultado.serialize()), 200
        else:
            return jsonify({'msg': 'La tarea no existe.'}), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error'}), 500
   

# busca las tareas por titulo, fecha y status
@app.route('/busqueda/total' , methods=['GET'])
def busqueda_profunda():
    try:
        fields = {}

        if 'title' in request.args:
            fields['title'] = request.args['title']

        if 'status' in request.args:
            fields['status'] = request.args['status']

        if 'date' in request.args:
            fields['date'] = request.args['date']

        resultado = Tasks.query.filter_by(**fields).first()

        if resultado:
            return jsonify(resultado.serialize()), 200
        else:
            return jsonify({'msg': 'La tarea no existe.'}), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error'}), 500
   

# ======== Aqui terminan las rutas ========

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


