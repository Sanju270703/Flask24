from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from datetime import datetime 
from db import db

from mqtt_client import mqtt_client

# def publish(topic, message):
#     mqtt_client.publish(topic, message)



# from app.employee import employee
# from app.employee.models import Employee

employee = Blueprint('employee', __name__)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # department = db.Column(db.String(100), nullable=False)
    # hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Todo', backref='employee', lazy=True)


    def __repr__(self):
        return '<Employee %r>' % self.id

@employee.route('/employee', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            data=request.json
        # name = request.form['name']
            # employee_id=data['id']
            employee_name=data['name']
        # department = request.form['department']
            new_employee = Employee(name=employee_name)  #department=department

            db.session.add(new_employee)
            db.session.commit()
            # publish('flask/mqtt/employee/create', f'Task Created: {new_employee.id}')
            return {'msg':'success'},200
            # return redirect(url_for('employee.index'))
        except Exception as e:
            print(f'*******{e}')
            return 'There was an issue adding the employee',400
    else:
        # employees = Employee.query.order_by(Employee.hire_date).all()
        # return render_template('employee/index.html', employees=employees)
        employees = Employee.query.all()
        # return render_template('templates/index.html', employees=employees)
        # return render_template('index.html', employees=employees)
        return {'msg':'GET method'}


@employee.route('/employee/delete/<int:id>')
def delete(id):
    employee_to_delete = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee_to_delete)
        db.session.commit()
        return redirect(url_for('/employee'))
        # return {'msg':'success'}, 302
    except Exception:
        return 'There was a problem deleting that employee'

@employee.route('/employee/update/<int:id>', methods=['GET', 'PUT'])
def update(id):
    employee = Employee.query.get_or_404(id)
    if request.method == 'PUT':
        data=request.json
        up_name=data['name']
        employee_id = data.get('employee_id')
        up_employee=Employee(name=up_name)
    
        employee.name=up_name

        # employee.name = request.form['name']
        # employee.department = request.form['department']
        try:
            item = Employee.query.filter_by(id = id).first()
            item.employee_id = employee_id
            db.session.commit()
            print(f'success:{up_employee}')
            return redirect(url_for('/employee'))
        except:
            return 'There was an issue updating the employee'
    # else:
    #     return {'msg':'GET method'}

