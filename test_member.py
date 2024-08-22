# test_member.py
import pytest
import json
from app import app, Todo, publish
from db import db  # Adjust this import based on your project structure
from member import Employee  # Adjust this import based on your project structure
from conftest import init_database, mock_mqtt_client  # Import the init_database and mock_mqtt_client fixtures
from unittest.mock import patch
# Ensure your tests are correctly using the fixtures

def test_employee_index(client):
    response = client.get('/employee')
    print(f'response.status_code {response.status_code}')    
    print(f'type response.status_code {type(response.status_code)}')    
    print(f'response.data {response.data}')

    assert response.status_code == 200
    
    assert b'msg' in response.data

# @patch('app.publish', autospec=True)
def test_create_employee(client, mock_mqtt_client):
    # with app.app_context():
    employee_data = {'name': 'Test Employee'}
    response = client.post('/employee', json=employee_data)
    assert response.status_code == 200  # Redirect after employee creation

    employee = Employee.query.first()
    assert employee is not None
    assert employee.name == 'Test Employee'

    #   checkinng the exceptions
    employee_data = {'id':1}
    response = client.post('/employee', json=employee_data)
    assert response.status_code == 400  # Redirect after employee creation

    # mock_mqtt_client.publish.assert_called_once_with('flask/mqtt/employee/create', f'Task Created: {employee.id}')

def test_delete_employee(client, init_database, mock_mqtt_client):
    # with app.app_context():
    employee = Employee(name='Employee to be deleted')
    db.session.add(employee)
    db.session.commit()

    employee_id = employee.id
    with patch('paho.mqtt.client', return_value=mock_mqtt_client):
        response = client.get(f'/employee/delete/{employee.id}')
    assert response.status_code == 200  # Redirect after employee deletion

    employee = Employee.query.get(employee_id)
    assert employee is None

    # mock_mqtt_client.publish.assert_called_once_with('flask/mqtt/employee/delete', f'Task Created: {employee_id}')

def test_update_employee(client, init_database, mock_mqtt_client):
    # with app.app_context():
        employee = Employee(name='Employee')
        db.session.add(employee)
        db.session.commit()

        updated_data = {'id': employee.id, 'name': 'Updated Employee'}
        response = client.put(f'/employee/update/{employee.id}', json=updated_data)
        assert response.status_code == 200  # Redirect after employee update

        employee = Employee.query.get(employee.id)
        assert employee.name == 'Updated Employee'

        # mock_mqtt_client.publish.assert_called_once_with('flask/mqtt/employee/update', f'Task Created: {employee.id}')

