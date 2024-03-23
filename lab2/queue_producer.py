import time
import hazelcast

client = hazelcast.HazelcastClient()
queue = client.get_queue("bq1")

for i in range(100):
    queue.put(i)
    print("Sended {0}".format(i))
    time.sleep(0.1)

client.shutdown()
