 #test_mqtt_client.py
from mqtt_client import publish_message

def test_publish_message(mocker):
    mock_mqtt_client = mocker.patch('mqtt_client.mqtt_client')
    publish_message('test/topic', 'test message')
    mock_mqtt_client.publish.assert_called_once_with('test/topic', 'test message')
