__author__ = 'seaadmin'
from Passenger import *
from Stations import *
import numpy.random as npr


num_passengers = 1000

#for each international flight
#need to add flight time offset to arrival time


flight_money = 0
flight_cost = 0

hours = 10

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


checkin_agent_cost = 25*(len(coach_checkin_list) + len(first_class_checkin_list)) * hours

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



#Queue Lists
first_class_checkin_queue_list = []
coach_checkin_queue_list = []

first_class_security_queue_list = []
coach_security_queue_list = []

coach_gate_list = []
first_class_gate_list = []
commuter_gate_list = []







#Generate Passengers
passenger_gen = Passengers()
for k in xrange(0,hours):
    for i in xrange(0, 40):
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



first_class_boarding_passenger = None
coach_boarding_passenger = None






next_arrival = Arrival(all_passengers.popleft())
#event list
event_list = [next_arrival,coach_checkin_1,coach_checkin_2,coach_checkin_3,first_class_checkin_1,coach_security_1,
              coach_security_2,first_class_security_1,CommuterFlight(),InternationalFlight()]

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
            #print "*****************This is X", x
            return x



    #print "****************Smallest Item ", event_list[smallest_index]

    #return event_list[smallest_index]


refunds_num = 0
refunds_cost = 0

system_time = 0

event = event_list[0]

system_time += event.next_event

i = 0
#print len(all_passengers)



while(system_time < (hours*60)):



    if isinstance(event, Arrival):

        passenger = event.passenger

        #print passenger.arrival

        if isinstance(passenger, Commuter):
            flight_money += 200
        elif isinstance(passenger, International):
            if passenger.is_first_class:
                flight_money += 1000
            else:
                flight_money += 500


        if passenger.is_first_class:
             if len(first_class_checkin_queue) == 0:
                #find free check-in
                first_class_checkin_list.sort(key=lambda x: x.is_free, reverse=True)
                free_station = first_class_checkin_list[0]

                if free_station.is_free:
                    free_station.dock_passenger(passenger)
                    free_station.set_next_event(float(free_station.generate_total_time(passenger.bags) + system_time))
                    #print "Next 1" ,free_station.next_event
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
                    #print "Next 2" ,free_station.next_event
                else:
                    coach_checkin_queue.append(passenger)
            else:
                coach_checkin_queue.append(passenger)

            #generate time
            #set next event to sys time + generate time
            #get next arrival
        #event.passenger = all_passengers.popleft()
        #system_time = event.passenger.arrival
        if len(all_passengers) > 0:
            next_passenger = all_passengers.popleft()
        else:
            next_passenger = None

        event.set_next_event(next_passenger)
        event.set_next_passenger(next_passenger)



        #system_time = event.passenger.arrival


        #print "Passenger: %i" % i
        """print "Arrival time: %f" % passenger.arrival
        print "Coach Queue Length: %i" % len(coach_checkin_queue)
        print "First Class Queue Length: %i" % len(first_class_checkin_queue)
        print "First Class Station: ", first_class_checkin_1.is_free
        print "Coach Station 1: ", coach_checkin_1.is_free
        print "Coach Station 2: ", coach_checkin_2.is_free
        print "Coach Station 3: ", coach_checkin_3.is_free"""



    elif isinstance(event, CheckIn):


        checked_passenger = event.passenger

        if event.is_first_class:
            if len(first_class_security_queue) == 0 and first_class_security_1.is_free:
                first_class_security_1.dock_passenger(checked_passenger)
                first_class_security_1.set_next_event(float(system_time + first_class_security_1.generate_screen_time()))
            else:
                first_class_security_queue.append(checked_passenger)

            #event.release_passenger()

        else: #coach
            coach_security_list.sort(key=lambda x: x.is_free, reverse=True)
            free_coach_security = coach_security_list[0]
            if len(coach_security_queue) == 0 and free_coach_security.is_free:
                free_coach_security.dock_passenger(passenger)
                free_coach_security.set_next_event(float(free_coach_security.generate_screen_time() + system_time))
            else:
                coach_security_queue.append(checked_passenger)
            pass



        event.release_passenger()
        event.set_next_event(None)

        #dock new passenger

        if event.is_first_class:
            if len(first_class_checkin_queue) > 0:
                next_first_class_passenger = first_class_checkin_queue.popleft()
                event.dock_passenger(next_first_class_passenger)
                event.set_next_event(float(system_time + event.generate_total_time(next_first_class_passenger.bags)))

        else:
            coach_checkin_list.sort(key=lambda x: x.is_free, reverse=True)
            free_coach_checkin = coach_checkin_list[0]

            if free_coach_checkin.is_free and len(coach_checkin_queue)>0:
                next_coach_passenger = coach_checkin_queue.popleft()
                free_coach_checkin.dock_passenger(next_coach_passenger)
                event.set_next_event(float(system_time + event.generate_total_time(next_coach_passenger.bags)))



        #print "FC Security Queue: %i" % len(first_class_security_queue)
        #print "Coach Security Queue: %i" % len(coach_security_queue)
        #print "Checkin"
        #event.set_next_event(None)
        #print "Yabba"
        #break
        #print "Done break"
    elif isinstance(event, Security):
        #print "Security"
        event.set_next_event(None)

        secured_passenger = event.passenger

        #move to gate
        if event.is_first_class:
            first_class_gate.append(secured_passenger)


        else:
            if isinstance(secured_passenger, International):
                coach_gate.append(secured_passenger)

            else:
                commuter_gate.append(secured_passenger)



        event.release_passenger()
        #take next passenger

        if event.is_first_class:
            if len(first_class_security_queue) > 0:
                next_security_first_class_passenger = first_class_security_queue.popleft()
                event.dock_passenger(next_first_class_passenger)
                event.set_next_event(float(event.generate_screen_time() + system_time))
        else:
            if len(coach_security_queue) > 0:
                next_security_coach_passenger = coach_security_queue.popleft()
                event.dock_passenger(next_security_coach_passenger)
                event.set_next_event(float(event.generate_screen_time() + system_time))




    elif isinstance(event, Flight):

        #print "Flight"
        #event.set_next_event()


        if isinstance(event, CommuterFlight):
            for i in xrange(0,50):
                if len(commuter_gate) > 0:
                    if len(commuter_gate) != 0:
                        commuter_gate.popleft()

            flight_cost += 1000
            event.set_next_event()

        elif isinstance(event, InternationalFlight):

            if first_class_boarding_passenger is None:
                first_class_boarding_passenger = first_class_gate.popleft()

            for k in xrange(0,50):

                if len(first_class_gate) > 0:
                    if first_class_boarding_passenger.flight_time < event.next_event:


                        if (event.next_event - first_class_boarding_passenger.arrival) >= 90:
                            refunds_num += 1
                            refunds_cost += 1000


                        first_class_boarding_passenger = first_class_gate.popleft()
                    elif first_class_boarding_passenger.flight_time > event.next_event:
                        break
                    else:
                        first_class_boarding_passenger = first_class_gate.popleft()


            #coach
            if coach_boarding_passenger is None:
                coach_boarding_passenger = coach_gate.popleft()

            for k in xrange(0,50):
                if len(coach_gate) > 0:
                    if coach_boarding_passenger.flight_time < event.next_event:
                        if (event.next_event - first_class_boarding_passenger.arrival) >= 90:
                            refunds_num += 1
                            refunds_cost += 500
                        coach_boarding_passenger = coach_gate.popleft()
                    elif coach_boarding_passenger.flight_time > event.next_event:
                        break
                    else:
                        coach_boarding_passenger = coach_gate.popleft()


            flight_cost += 10000


            event.set_next_event()



    print system_time
    first_class_checkin_queue_list.append((system_time,len(first_class_checkin_queue)))
    coach_checkin_queue_list.append((system_time,len(coach_checkin_queue)))

    first_class_security_queue_list.append((system_time,len(first_class_security_queue)))
    coach_security_queue_list.append((system_time,len(coach_security_queue)))

    coach_gate_list.append((system_time,len(coach_gate)))
    first_class_gate_list.append((system_time,len(first_class_gate)))
    commuter_gate_list.append((system_time,len(commuter_gate)))


    event = next_event()

    system_time = event.next_event

    #print event
    #print event.next_event
    #print event.passenger
    #system_time = event.next_event
    #system_time = event.next_event

    #print "System Time: %f" % system_time
    i+= 1



"""print "Money earned from tickets: %i" % flight_money
print "Money spent on flights: %i" % flight_cost
print "Money spent on check-in agents: %i" % checkin_agent_cost
print "Number of refunds: %i" % refunds_num
print "Refunds Cost: %i" % refunds_cost
print "Coach Checkin Queue: %i" % len(coach_checkin_queue)
print "First Class Checkin Queue: %i" % len(first_class_checkin_queue)

print "Coach Security Queue: %i" % len(coach_security_queue)
print "First Class Security Queue: %i" % len(first_class_security_queue)

print "Commuter Gate: %i" % len(commuter_gate)
print "Coach Gate: %i" % len(coach_gate)
print "First Class Gate: %i" % len(first_class_gate)"""

"""print first_class_checkin_queue_list
print coach_checkin_queue_list

print first_class_security_queue_list
print coach_security_queue_list

print coach_gate_list
print first_class_gate_list
print commuter_gate_list"""