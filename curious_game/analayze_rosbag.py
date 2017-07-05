import rosbag
bag = rosbag.Bag('../data/physical_curiosity_open_day_2_2017-02-03-07-56-54.bag')
all_topics = set()
for topic, msg, t in bag.read_messages():
    all_topics.add(topic)
    # print topic
bag.close()
print(all_topics)