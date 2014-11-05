__author__ = 'seaadmin'
from Passenger import *
from Stations import *
import numpy.random as npr


num_passengers = 1000

#for each international flight
#need to add flight time offset to arrival time

all_passengers = deque()
all_passengers_list = []

coach_checkin_1 = CheckIn(1,False)
coach_checkin_2 = CheckIn(2,False)
coach_checkin_3 = CheckIn(3,False)
first_class_checkin_1 = CheckIn(4,True)


#Create check-in
coach_checkin_list = [coach_checkin_1,coach_checkin_2,coach_checkin_3]
first_class_checkin_list = [first_class_checkin_1]

coach_checkin_queue = deque()
first_class_checkin_queue = deque()




#Create Security
coach_security_1 = Security(False)
coach_security_2 = Security(False)
first_class_security_1 = Security(True)
coach_security_list = [coach_security_1,coach_security_2]
first_class_security_list = [first_class_security_1]





#queues
coach_security_queue = deque()
first_class_security_queue = deque()

#Gates
first_class_gate = deque()
coach_gate = deque()
commuter_gate = deque()



#Generate Passengers
passenger_gen = Passengers()
for i in xrange(0, 1000):
    passenger = passenger_gen.create_commuter()
    #print "Arrival Time: %f" % passenger.arrival
    all_passengers_list.append(passenger)


num_of_first_class_passengers = int(npr.binomial(50, 0.8, 1))
num_of_coach_passengers = int(npr.binomial(100, 0.85, 1))

for i in xrange(0,num_of_first_class_passengers):
    passenger = passenger_gen.create_international(True)
    #print "First Class: %i" % passenger.arrival
    all_passengers_list.append(passenger)

for i in xrange(0,num_of_coach_passengers):
    passenger = passenger_gen.create_international(False)
    #print "Coach: %i" % passenger.arrival
    all_passengers_list.append(passenger)


all_passengers_list.sort(key=lambda x: x.arrival)

all_passengers = deque(all_passengers_list)

"""for x in all_passengers_list:
    print x.arrival"""

#Arrivals


next_arrival = Arrival(all_passengers.popleft())
#event list
event_list = [next_arrival,coach_checkin_1,coach_checkin_2,coach_checkin_3,first_class_checkin_1,coach_security_1,coach_security_2,first_class_security_1]

def next_event():
    """y = sorted(event_list,key=lambda x:(x.next_event is None, x))
    print "*****************Arrival Time: ",y[0].next_event
    print "*****************Arrival Time: ",y[1].next_event
    print float(y[0].next_event) > y[1].next_event
    return y[0]"""
    #combined_events = []
    #for event in event_list:
        #combined_events.append(event.next_event)

    #smallest_index = combined_events.index(min(combined_events))

    event_list.sort(key=lambda x: x.next_event)

    for x in event_list:
        if x.next_event is not None:
            print "*****************This is X", x
            return x



    #print "****************Smallest Item ", event_list[smallest_index]

    #return event_list[smallest_index]




system_time = 0

event = event_list[0]

system_time += event.next_event

i = 0
print len(all_passengers)

while(len(all_passengers) != 0):



    if isinstance(event, Arrival):

        passenger = event.passenger

        print passenger.arrival


        if passenger.is_first_class:
             if len(first_class_checkin_queue) == 0:
                #find free check-in
                first_class_checkin_list.sort(key=lambda x: x.is_free, reverse=True)
                free_station = first_class_checkin_list[0]

                if free_station.is_free:
                    free_station.dock_passenger(passenger)
                    free_station.set_next_event(float(free_station.generate_total_time(passenger.bags) + system_time))
                    print "Next 1" ,free_station.next_event
                else:
                    first_class_checkin_queue.append(passenger)
             else:
                 first_class_checkin_queue.append(passenger)

        else:

            #check queue length
            if len(coach_checkin_queue) == 0:
                #find free check-in
                coach_checkin_list.sort(key=lambda x: x.is_free, reverse=True)
                free_station = coach_checkin_list[0]
                if free_station.is_free:
                    free_station.dock_passenger(passenger)
                    free_station.set_next_event(float(free_station.generate_total_time(passenger.bags) + system_time))
                    print "Next 2" ,free_station.next_event
                else:
                    coach_checkin_queue.append(passenger)
            else:
                coach_checkin_queue.append(passenger)

            #generate time
            #set next event to sys time + generate time
            #get next arrival
        #event.passenger = all_passengers.popleft()
        #system_time = event.passenger.arrival

        next_passenger = all_passengers.popleft()

        event.set_next_event(next_passenger)
        event.set_next_passenger(next_passenger)



        #system_time = event.passenger.arrival


        print "Passenger: %i" % i
        print "Arrival time: %i" % passenger.arrival
        print "Coach Queue Length: %i" % len(coach_checkin_queue)
        print "First Class Queue Length: %i" % len(first_class_checkin_queue)
        print "First Class Station: ", first_class_checkin_1.is_free
        print "Coach Station 1: ", coach_checkin_1.is_free
        print "Coach Station 2: ", coach_checkin_2.is_free
        print "Coach Station 3: ", coach_checkin_3.is_free



    elif isinstance(event, CheckIn):
        print "Checkin"
        event.set_next_event(1)
        print "Yabba"
        break
        print "Done break"
    elif isinstance(event, Security):
        pass
    elif isinstance(event, CommuterFlight):
        pass
    elif isinstance(event, InternationalFlight):
        pass

    event = next_event()

    system_time = event.next_event

    #print event
    #print event.next_event
    #print event.passenger
    #system_time = event.next_event
    #system_time = event.next_event

    print "System Time: %i" % system_time
    i+= 1