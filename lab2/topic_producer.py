import time
import hazelcast

client = hazelcast.HazelcastClient()
topic = client.get_topic("events-producer")

for i in range(100):
    topic.publish(i)
    print("Sended {0}".format(i))
    time.sleep(0.5)

client.shutdown()