__author__ = 'Chris'

import numpy.random as npr

class Arrival(object):
    def __init__(self, passenger):
        self.passenger = passenger
        self.next_event = passenger.arrival



    def set_next_event(self,passenger):
        self.next_event = passenger.arrival
    def set_next_passenger(self,passenger):
        self.passenger = passenger


class CheckIn(object):

    def __init__(self,number, is_first_class):
        self.is_free = True
        self.passenger = None
        self.number = number
        self.is_first_class = is_first_class
        self.next_event = None

    def generate_print_time(self):
        return npr.exponential(scale=(float(1)/2),size=1)

    def generate_check_time(self,num_of_bags):
        bag_time = 0

        if num_of_bags == 0:
            return 0
        else:
            for bag in xrange(1,num_of_bags):
                bag_time += npr.exponential(scale=1,size=1)
            return bag_time
        
    def generate_delay(self):
        s = float(1/3)
        return npr.exponential(scale=(float(1)/3),size=1)

    def generate_total_time(self, bag_number):
        return self.generate_print_time() + self.generate_check_time(bag_number) + self.generate_delay()

    def dock_passenger(self,customer):
        self.customer = customer
        self.is_free = False

    def release_passenger(self):
        self.customer = None
        self.is_free = True
    def set_next_event(self, time):
        self.next_event = time

class Security(object):
    def __init__(self, is_first_class):
        self.is_free = True
        self.passenger = None
        self.is_first_class = is_first_class
        self.next_event = None

    def generate_screen_time(self):
        return npr.exponential(scale=(1/3),size=1)

    def dock_passenger(self,customer):
        self.customer = customer
        self.is_free = False

    def release_passenger(self):
        self.customer = None
        self.is_free = True

class Gate(object):
    pass
    #need refund mechanism

class CommuterFlight(object):
    def __init__(self):
        self.next_event = 30

class InternationalFlight(object):
    def __init__(self):
        self.next_event = 0
