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
#     # client.subscribe(MQTT_TOPIC)
#     print(f'subscribed to {MQTT_TOPIC}')


# def on_message(client, userdata, msg):
#     print(f"Message received: {msg.payload.decode()} on topic {msg.topic}")

# mqtt_client.on_connect = on_connect
# mqtt_client.on_message = on_message

# def run_mqtt_client():
#     mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
#     mqtt_client.loop_start()

# def publish_message(topic, message):
#     mqtt_client.publish(topic, message)

# # Start the MQTT client
# run_mqtt_client()

# for i in range(100):
#     message = f'hello from server A {i}'
#     print(f'sending message... : {message}')
#     publish_message(MQTT_TOPIC,message=message)
#     time.sleep(1)



import paho.mqtt.client as mqtt
import time

# MQTT settings
MQTT_BROKER = '127.0.0.1'
MQTT_PORT = 1883
MQTT_TOPIC = 'flask/mqtt'

# Initialize the MQTT client
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

mqtt_client.on_connect = on_connect

def run_mqtt_client():
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()

def publish_message(topic, message):
    mqtt_client.publish(topic, message)

# Start the MQTT client
run_mqtt_client()

for i in range(1):
    message = f'hello from server A {i}'
    print(f'sending message... :{i} : {message}')
    publish_message(MQTT_TOPIC, message)
    time.sleep(1)  # Add a small delay between messages



# client = mqtt.client()

# subscriber={
# 	'insert': insert_table,
# 	'update': update_table,
# 	'delete': delete_record
# }


# def insert_table(client, userdata, mesage):
# 	insert todo (message) values("message")

# def update_table(client, userdata, mesage):
# 	update todo set message="completed mqtt tasks" where id=1
	
# def delete_record(client, userdata, mesage):
# 	delete from todo where message="completed mqtt tasks"


# def on_connect1():
# 	1. subscribe 
# 		for loop on subscriber:
# 			client.subscribe("topic name") # key
# 			client.message_callback_add("topic name", "method1") # key, value 

# def on_disconnect1():
# 	client.reconnect()


# def init_mqtt():
# 	client = mqtt.client("<clinet name>")
# 	MQTT_BROKER = '127.0.0.1'
#     client.on_connect=on_connect_1
#     client.on_disconnecton_disconnect1
#     client.loop_start()