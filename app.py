from asyncio import tasks
from logging import exception
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, Tasks
from datetime import datetime
from sqlalchemy import desc


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db\\tasks.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


# ======== Aqui empiezan las rutas ========
# ======== Agrega una tarea ========
@app.route('/')
def home():
    tareas =  db.session.query(Tasks).order_by(desc(Tasks.id)).all()
    return render_template('index.html', tareas=tareas )



# Agrega una tarea 
@app.route('/agregar', methods=['POST'])
def agregar():
    try:

        if request.method == 'POST':
            tarea = request.form.get('tarea')
            ya_completada = request.form.get('comp')
            fecha = datetime.today().strftime('%Y-%m-%d')
            print(ya_completada  )

            if ya_completada == 'on':
                status = 0
            else:
                status = 1  
            
            # 1 = pendiente, 0 = completada
            tarea_nueva = Tasks(tarea, fecha, status=status)
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


@app.route('/done/<int:id>')
def done(id):
    try:
        tarea = Tasks.query.get(int(id))

        if tarea.status == 1:
            tarea.status = 0
        else:
            tarea.status = 1
        
        db.session.commit()
        return redirect(url_for('home'))

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500




@app.route('/delete/<int:id>')
def borrar_tarea(id):
    try:
        tarea = Tasks.query.get(int(id))
        db.session.delete(tarea)
        db.session.commit()
        return redirect(url_for('home'))

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500



# Muestra las tareas False = completadas
@app.route('/completadas')
def get_completadas():
    try:
        tareas = Tasks.query.all()
        tareas_json = []
        for tarea in tareas:
            if tarea.status == 0:
                tareas_json.append(tarea.serialize())

        return jsonify(tareas_json), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500
   

# Muestra las tareas Trues = Pendientes
@app.route('/incompletas')
def get_incompletas():
    try:
        tareas = Tasks.query.all()
        tareas_json = []
        for tarea in tareas:
            if tarea.status == 1:
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

        if resultado:
            return jsonify(resultado.serialize()), 200
        else:
            return jsonify({'msg': 'La tarea no existe.'}), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error'}), 500
   

# busca las tareas por titulo, fecha y status
@app.route('/busqueda/total' , methods=['GET'])
def busqueda_total():
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


