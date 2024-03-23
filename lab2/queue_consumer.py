import time

import hazelcast

client = hazelcast.HazelcastClient()

queue = client.get_queue("bq1").blocking()
while(True):
    msg = queue.take()
    print("Got {0}".format(msg))
    time.sleep(1)
