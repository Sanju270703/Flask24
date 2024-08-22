from flask import Flask, render_template, url_for, request , redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql 
import paho.mqtt.client as mqtt
import threading
from flask_migrate import Migrate
from db import db
from member import Employee
# from mqtt_client import init_mqtt
# import mqtt_client
# import mqtt_subscriber 'APP_ACK'  
 
 

app=Flask(__name__) 
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sanjay:password@localhost/taskDB'

 
db.init_app(app)


migrate = Migrate(app, db) 


MQTT_BROKER = '127.0.0.1'
MQTT_PORT = 1883
TOPIC_CREATE = 'flask/mqtt/create'
TOPIC_DELETE = 'flask/mqtt/delete'
TOPIC_UPDATE = 'flask/mqtt/update'
MQTT_TOPICS = ['flask/mqtt/create','flask/mqtt/delete','flask/mqtt/update']


class Todo(db.Model):
    __table_args__ = {'extend_existing': True}  # Allow redefinition
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200), nullable=False)
    completed=db.Column(db.Integer, default=0)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))


    def __repr__(self):
        return '<Task %r>' % self.id
    
# MQTT client
mqtt_client = mqtt.Client()


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe([(TOPIC_CREATE, 0), (TOPIC_DELETE, 0), (TOPIC_UPDATE, 0)])
    for topic in MQTT_TOPICS:
        client.subscribe(topic)
        print(f'subscribed to {topic}')


def on_message(client, userdata, msg):
    log_message = f"\n Message received: {msg.payload.decode()} on topic {msg.topic}"
    print(log_message)
    with open('log_file.txt','a+') as log_file:
        log_file.write(log_message)


mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def publish(topic, message):
    mqtt_client.publish(topic, message)
    

def run_mqtt_client():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

with app.app_context():
    db.create_all()



@app.route('/', methods=['POST','GET'])
def index():
    if request.method=='POST':
        data=request.json
        # task_content=request.form['content']
        task_content=data['content']
        new_task=Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            print(f"Publishing to {TOPIC_CREATE}")
            mqtt_client.publish(TOPIC_CREATE, f'Task Created: {new_task.id}')
            return redirect('/')
          
        except Exception as e:
            print(e)
            
            return 'There was an issue ading your task'
        
    else:
        # mqtt_client.publish('APP_ACK','entered index page')
        tasks=Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)



@app.route('/delete/<int:id>')
def delete(id): 
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        print(f"Publishing to {TOPIC_DELETE}")
        mqtt_client.publish(TOPIC_DELETE, f'Task Deleted: {task_to_delete.id}')
        return redirect('/')
    
    except Exception as e:
        print(f"checking error -->> {e}")
        return 'There was a problem deleting that task'
    


@app.route('/update/<int:id>', methods=['GET', 'PUT'])
def update(id):
    task=Todo.query.get_or_404(id)
    if request.method=='PUT':
        data=request.json
        content = data['content']
        employee_id = data.get('employee_id')
        # task_content=request.form['content']
        task.content = content
        # task=Todo(content=task_content)
        try:
            # db.session.update(task)
            item = Todo.query.filter_by(id = id).first()
            item.employee_id = employee_id
            db.session.commit()
            print(f"Publishing to {TOPIC_UPDATE}")
            mqtt_client.publish(TOPIC_UPDATE, f'Task Updated: {task.id} {employee_id}')
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/employeeTodos/<int:employee_id>/', methods=['GET'])
def get_employee_tasks(employee_id):
    employee = Employee.query.get(employee_id)
    if employee is None:
        return jsonify({'message': 'Employee not found'}), 404
    global Todo
    tasks = Todo.query.filter_by(employee_id=employee_id).all()
    tasks_list = [{'id': task.id, 'content': task.content} for task in tasks]
    
    return jsonify({'employee': employee.name, 'tasks': tasks_list})


from member import employee as main_blueprint
app.register_blueprint(main_blueprint)



if __name__=="__main__":
    mqtt_thread = threading.Thread(target=run_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    app.run(port=3000, debug=True) 