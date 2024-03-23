import hazelcast

if __name__ == '__main__':

    hz = hazelcast.HazelcastClient()
    map = hz.get_map("test").blocking()
    map.clear()

    key=0
    value = 0

    for i in range(1000):
        key += 1
        value += 1
        map.put(key, value)
        print("Put key {0} and value {1}".format(key, value))