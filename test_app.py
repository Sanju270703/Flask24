# test_app.py
import json
from app import db, Todo, Employee
import unittest
from unittest.mock import patch, MagicMock
from app import app, db, Todo, publish, run_mqtt_client, on_connect, on_message
from flask import url_for

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Task' in response.data



def test_create_task(client, init_database, mock_mqtt_client):
    
    task_data = {'content': 'Test Task'}
    response = client.post('/', json=task_data)
    assert response.status_code == 302  # Redirect after task creation

    task = Todo.query.first()
    assert task is not None
    assert task.content == 'Test Task'

    mock_mqtt_client.publish.assert_called_once_with('flask/mqtt/create', f'Task Created: {task.id}')



def test_delete_task(client, init_database, mock_mqtt_client):

    task = Todo(content='Task to be deleted')
    db.session.add(task)
    db.session.commit()

    task_id = task.id  # Get the task ID before it's deleted
    response = client.get(f'/delete/{task.id}')
    assert response.status_code == 302  # Redirect after task deletion

    task = Todo.query.get(task_id)
    assert task is None

    mock_mqtt_client.publish.assert_called_once_with('flask/mqtt/delete', f'Task Deleted: {task_id}')



def test_update_task(client, init_database, mock_mqtt_client):

    employee = Employee(name='Test Employee')
    db.session.add(employee)
    db.session.commit()

    task = Todo(content='Task to be updated')
    db.session.add(task)
    db.session.commit()

    updated_data = {'content': 'Updated Task', 'employee_id': employee.id}
    response = client.put(f'/update/{task.id}', json=updated_data)
    assert response.status_code == 302  # Redirect after task update

    task = Todo.query.get(task.id)
    assert task.content == 'Updated Task'
    assert task.employee_id == employee.id

    mock_mqtt_client.publish.assert_called_once_with('flask/mqtt/update', f'Task Updated: {task.id} {employee.id}')



def test_get_employee_tasks(client, init_database, mocker):

    employee = Employee(name='Test Employee')
    db.session.add(employee)
    db.session.commit()

    task = Todo(content='Task for employee', employee_id=employee.id)
    db.session.add(task)
    db.session.commit()

    response = client.get(f'/employeeTodos/{employee.id}/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['employee'] == 'Test Employee'
    assert len(data['tasks']) == 1
    assert data['tasks'][0]['content'] == 'Task for employee'


