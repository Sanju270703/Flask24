import unittest
from unittest.mock import MagicMock, patch, call
import paho.mqtt.client as mqtt

MQTT_TOPICS = ['flask/mqtt/create','flask/mqtt/delete','flask/mqtt/update']

# Assume the MQTT client code is in a file named mqtt_client.py
from mqtt_subscriber import mqtt_client, on_connect, on_message, run_mqtt_client, publish_message

class TestMQTTClient(unittest.TestCase):
    
    @patch('paho.mqtt.client.Client.connect')
    @patch('paho.mqtt.client.Client.loop_forever')
    def test_run_mqtt_client(self, mock_loop_forever, mock_connect):
        # Run the MQTT client function
        run_mqtt_client()
        
        # Check if the connect method was called with the correct arguments
        mock_connect.assert_called_with('127.0.0.1', 1883, 60)
        
        # Check if loop_forever method was called to start the loop
        mock_loop_forever.assert_called_once()

    def test_on_connect(self):
        # Create a mock MQTT client
        client = MagicMock()
        
        # Call the on_connect function
        on_connect(client, None, None, 0)
        
        # # Check if the client subscribed to all topics
        # for topic in MQTT_TOPICS:
        #     client.subscribe.assert_any_call(topic)
        
        # # Check the print statements
        # expected_calls = [unittest.mock.call(f'subscribed to {topic}') for topic in MQTT_TOPICS]
        # with patch('builtins.print') as mock_print:
        #     on_connect(client, None, None, 0)
        #     mock_print.assert_has_calls(expected_calls, any_order=True)

         # Check if the client subscribed to all topics
        expected_calls = [call(topic) for topic in MQTT_TOPICS]
        client.subscribe.assert_has_calls(expected_calls, any_order=True)

    def test_on_message(self):
        # Create a mock message
        msg = MagicMock()
        msg.payload.decode.return_value = 'Test Message'
        msg.topic = 'flask/mqtt/create'
        
        # Patch print to check the output
        with patch('builtins.print') as mock_print:
            on_message(None, None, msg)
            
            # Check if the print statement was called with the correct message
            mock_print.assert_called_with('Message received: Test Message on topic flask/mqtt/create')


    
if __name__ == '__main__':
    unittest.main()
