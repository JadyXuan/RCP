import paho.mqtt.client as mqtt
import uuid
import time

class MqttReceiver(object):
    def __init__(self, broker, port, topic, keepallive=60):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.keepallive = keepallive
        
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    
    def listen(self):
        self.client.connect(self.broker, self.port, self.keepallive)
        self.client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {}".format(rc))
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        sensor, event = msg.payload.decode().split("|")
        print("{} : {}".format(sensor, event))

class MqttSender(object):
    def __init__(self, getter):
        self.broker = ""
        self.port = 0
        self.topic = ""
        self.keepallive = 60
        self.client = mqtt.Client()
        self.get = getter
        self.uuid = hash(uuid.getnode())
    
    def set(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def connect(self):
        self.client.connect(self.broker, self.port)
        print("Connect to MQTT Server {}:{}".format(self.broker, self.port))

    def __call__(self, **kwargs):
        msg = "{}|{}".format(self.uuid, self.get(kwargs))
        result = self.client.publish(self.topic, msg)
        if result[0] == 0:
            print("Send {} to topic {}".format(msg, self.topic))
        else:
            print("Failed to send {}, error code {}".format(msg, result[0]))
    


if __name__ == "__main__":
    broker = "192.168.2.105"
    port = 1883
    keepallive = 60
    topic = "/thermal/event_message"
    
    """
    @MqttSender
    def getter():
        return "fall"
    
    getter.set(broker=broker, port=port, keepallive=keepallive, topic=topic)
    getter.connect()
    while True:
        getter()
        time.sleep(1)
    """
    getter = MqttReceiver(broker, port, topic, keepallive)
    getter.listen()

"""
def on_connect(client, userdata, flags, rc):
    print("Connected with result code {}".format(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print("{} : {}".format(msg.topic, msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, keepallive)

client.loop_forever()
"""