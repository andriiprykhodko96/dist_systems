import hazelcast
def onMessage(messageReceived):
    print("Consumed {0}".format(messageReceived.message))

client = hazelcast.HazelcastClient()
topic = client.get_topic("events-producer")
topic.add_listener(onMessage)

input("Start\n")
