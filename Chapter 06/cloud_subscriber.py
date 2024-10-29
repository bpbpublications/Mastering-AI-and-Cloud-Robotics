import paho.mqtt.client as mqtt 
 
# MQTT Configurations 
mqtt_broker_address = 127.0.0.1 
mqtt_broker_port = 1883 
mqtt_topic = "data_topic" 
 
# Callback for Receiving Data 
def on_message(client, userdata, msg): 
    payload = msg.payload 
    print(f"Received Data from Robot: {payload}") 
 
# Initialization Client 
mqtt_client = mqtt.Client() 
mqtt_client.on_message = on_message 
mqtt_client.connect(mqtt_broker_address, mqtt_broker_port) 
 
# Subscribe to the Data Topic 
mqtt_client.subscribe(mqtt_topic) 
 
# Continuously Listen for Messages 
mqtt_client.loop_forever() 