__author__ = 'Chris'
from collections import deque
import numpy.random as npr
import operator

class Commuter(object):

   def __init__(self,arrival):
       self.arrival = arrival
       self.bags = npr.geometric(p=.8,size=1)
       self.total_time = 0 #adjust when leave station system_time - station time
       #need to adjust for arrival time
       self.checkin_time = 0
       self.security_time = 0
       self.gate_time = 0 #total_system_time - system time when leave security

       self.is_first_class = False



class International(object):

    def __init__(self, arrival, is_first_class):
        self.arrival = arrival
        self.is_first_class = is_first_class
        self.bags = npr.geometric(p=.6,size=1)
        self.total_time = 0
        self.flight_time = None


class Passengers(object):

    def create_commuter(self):
        arrival_time = npr.poisson(lam=(40))
        return Commuter(arrival_time)

    def create_international(self, is_first_class):
        arrival_time = int(abs(npr.normal(loc=75, scale=50)))
        #is_first_class = is_first_class
        return International(arrival_time, is_first_class)

    def commuter_arrivals(self,num_of_passengers):
        commuter_passengers = []
        for commuter in xrange(0,num_of_passengers):
            commuter_passengers.append(self.create_international())
        return commuter_passengers

    def international_arrivals(self,num_of_passengers):
        international_passengers = []
        for passenger in xrange(0,num_of_passengers):
            international_passengers.append(self.create_international())
        return international_passengers


    def commuter_queue(self, commuter_list):
        return deque(commuter_list.sort(key=operator.attrgetter("arrival"), reversed=False))
    def international_queue(self, commuter_list):
        return deque(commuter_list.sort(key=operator.attrgetter("arrival"), reversed=False))
