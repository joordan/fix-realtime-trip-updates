### to add
### delta from scheduled
### if it is an arrival update arrival time instead 



from google.transit import gtfs_realtime_pb2
import urllib
import os

filename = raw_input("Enter realtime/url/file.pb: ")

stopchange = []
emptytrip = []
entitynum = -1
stopcount = 0

feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.urlopen(filename)
feed.ParseFromString(response.read())
print feed.header.timestamp
for entity in feed.entity:
    entitynum += 1
    if not entity.trip_update.stop_time_update:
	emptytrip.append(entity.id)
	del feed.entity[entitynum]
	#del feed.entity[:]
	#feed.ClearField('entity')
	continue

    for stop_time_update in entity.trip_update.stop_time_update:
	stopcount = stopcount + 1
	#trip check
	if id != entity.id:
		previousTime = 0
		previousDelay = None
		sequence_flag = 0

	#arrival check
	if stop_time_update.arrival.time:#if its an arrival
		if (sequence_flag == stop_time_update.stop_sequence - 1) :	#check if the current update is the next in sequence 
			if not previousDelay: #time < last time now check if last has a delay
				stop_time_update.arrival.time = previousTime #if not delay copy the last time
				stopchange.append("\t" + str(entity.id) + "\t" + str(stop_time_update.stop_sequence) + "\t\t" + str(stop_time_update.stop_id) + "\t\tarrival")
			else:
				stop_time_update.arrival.time += -(stop_time_update.arrival.delay) + previousDelay	#adjust time to have prev delay
				stop_time_update.arrival.delay = previousDelay
				stopchange.append("\t" + str(entity.id) + "\t" + str(stop_time_update.stop_sequence) + "\t\t" + str(stop_time_update.stop_id) + "\t\tarrival")

	#departure check
	elif stop_time_update.departure.time < previousTime:
		if not previousDelay: #time < last time now check if last has a delay
			stop_time_update.departure.time = previousTime #if not delay copy the last time
			stopchange.append("\t" + str(entity.id) + "\t" + str(stop_time_update.stop_sequence) + "\t\t" + str(stop_time_update.stop_id) + "\t\tdeparture")
			sequence_flag = stop_time_update.stop_sequence
		else:	# else there is a delay and adjust
			stop_time_update.departure.time += -(stop_time_update.departure.delay) + previousDelay
			stop_time_update.departure.delay = previousDelay
			sequence_flag = stop_time_update.stop_sequence
			stopchange.append("\t" + str(entity.id) + "\t" + str(stop_time_update.stop_sequence) + "\t\t" + str(stop_time_update.stop_id) + "\t\tdeparture")

	#store previous values
	id = entity.id
	if stop_time_update.departure.time:
		previousDelay = stop_time_update.departure.delay
		previousTime = stop_time_update.departure.time
	else:
		previousDelay = stop_time_update.arrival.delay
		previousTime = stop_time_update.arrival.time

    print entity

fname= "tripid2.pb"
file = open(fname,"w")
file.write(feed.SerializeToString())
file.close()
print "timestamp:",feed.header.timestamp,"\n"
print "trips updated"
print entitynum +1,"trips"
print stopcount,"stops\n"

if emptytrip:
        count = 1
	print "Empty trips:", len(emptytrip)
	for id in emptytrip:
		print str(count)+".",id	
                count += 1
	print "\n"

if stopchange:
        count = 1
        print "Time changes:", len(stopchange)
        print "\ttrip\tsequence\tstop\t\ttype"
        for x in stopchange:
                print str(count)+".",x
                count += 1

if not emptytrip and not stopchange:
	print "feed OK! no changes needed"

