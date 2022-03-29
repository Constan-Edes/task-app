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
    # imprime las primeras 60 tareas mas recientes de la base de datos 
    # para acceder al resto se pueden usar las busquedas

    # orden = request.args.get('order', default=0)
    # orden = 0 -> ordena por id descendente (mas reciente)
    # orden = 1 -> ordena por id ascendente (mas antiguo)
    # proximamente se apuntara a ordenar por abecedario y mas de un orden a la vez

    filter = request.args.get('filter', default=None)
    # filter = 1 -> pendientes
    # filter = 2 -> completadas
    # filter = None -> todas

    if filter !=  None:
        tareas = db.session.query(Tasks).filter(Tasks.status == filter).order_by(desc(Tasks.id)).limit(60).all()
    else:
        tareas = db.session.query(Tasks).order_by(desc(Tasks.id)).limit(60).all()

    return render_template('index.html', tareas=tareas, filter=filter)


# Agrega una tarea, no deja agregar una tarea vacia, ni repetida
@app.route('/agregar', methods=['POST'])
def agregar():
    try:
        if request.method == 'POST':
            tarea = request.form.get('tarea')
            tarea = tarea.strip()
            tarea = tarea.capitalize()
            repetida = Tasks.query.filter(Tasks.title == tarea).first() 
            if repetida:
                return 'error'
            
            ya_completada = request.form.get('comp')
            fecha = datetime.today().strftime('%Y-%m-%d')

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
   

# Muestra todas las tareas en formato JSON (sin estilos)
# Falses = Completadas
# Trues = Pendientes
@app.route('/tareas')
def get_tareas():
    try:
        tareas = Tasks.query.all()
        tareas_json = [tarea.serialize()  for tarea in tareas]
        return jsonify(tareas_json), 200

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error.'}), 500


# marca una tarea como completada o pendiente (switch)
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


# elimina una tarea de la base de datos
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


# busca las tareas por titulo 
@app.route('/busqueda', methods=['GET'])
def busqueda_titulo():
    try:
        search_title = request.args['title']
        resultado =  db.session.query(Tasks).filter(Tasks.title.like(f'%{search_title}%'))

        if resultado.count() == 0:
            return render_template('index.html', tareas=[], filter=None)
        else:
            return render_template('index.html', tareas=resultado)

    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error'}), 500


# busca las tareas por titulo o fecha
@app.route('/busqueda/total' , methods=['GET'])
def busqueda_total():
    try:
        search = request.args['search_adv']
        resultado =  db.session.query(Tasks).filter(Tasks.date.like(f'%{search}%') | Tasks.title.like(f'%{search}%'))
       
        if resultado.count() == 0:
            return render_template('index.html', tareas=[], filter=None)
        else:
            return render_template('index.html', tareas=resultado)
        
    except Exception as e:
        exception('[SERVER]: Error -> {}'.format(e))
        return jsonify({'msg': 'Ha ocurrido un error'}), 500
   


# ======== Aqui terminan las rutas ========
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)


