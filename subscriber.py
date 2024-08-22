# import paho.mqtt.client as mqtt
# import time 
# # MQTT settings
# # MQTT_BROKER = 'broker.hivemq.com'
# MQTT_BROKER = '127.0.0.1'
# MQTT_PORT = 1883
# MQTT_TOPIC = 'flask/mqtt'

# # Initialize the MQTT client
# mqtt_client = mqtt.Client()

# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     client.subscribe(MQTT_TOPIC)
#     print(f'subscribed to {MQTT_TOPIC}')


# def on_message(client, userdata, msg):
#     print(f"Message received: {msg.payload.decode()} on topic {msg.topic}")

# mqtt_client.on_connect = on_connect
# mqtt_client.on_message = on_message

# def run_mqtt_client():
#     mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
#     mqtt_client.loop_start()
#     mqtt_client.loop_forever()

# def publish_message(topic, message):
#     mqtt_client.publish(topic, message)

# # Start the MQTT client
# run_mqtt_client()

# # for i in range(100):
# #     message = 'hello from server A'
# #     print(f'sending message... :{i} : {message}')
# #     publish_message(MQTT_TOPIC,message=message)
# #     time.sleep(1)

import paho.mqtt.client as mqtt

# MQTT settings
MQTT_BROKER = '127.0.0.1'
MQTT_PORT = 1883
# MQTT_TOPIC = 'flask/mqtt'
MQTT_TOPICS = ['flask/mqtt/create','flask/mqtt/delete','flask/mqtt/update']


# Initialize the MQTT client
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in MQTT_TOPICS:
        client.subscribe(topic)
        print(f'subscribed to {topic}')

def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()} on topic {msg.topic}")

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def run_mqtt_client():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_forever()

# Start the MQTT client
run_mqtt_client()