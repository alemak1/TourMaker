from sets import Set, ImmutableSet
import statistics

#TODO ITEMS:
	#Define error classes and implement error handling and validation in code
		#ValueError should be raised if distance can't be found
	#Create user-interface for generating a tour
	#Optional: Allow for user to query additional tour informatoins/stats from a tour object
		#(i.e.) total time of the tour, etc
	#Include unit tests/doc tests for all the methods and for a comprehensive variety of use cases
	#Additional operator loading for larger variety of different operands (need to do type checking of classes)
	#Additional operator overloading for __isub__ and __iadd__, as well as __int__ (conversion to integers)
	#Finish documentation, including docstrings for all the methods

class Tour:
	'''An instance of this class can be instantiated with an arbitrary number of US cities, and is used
	to fetch information from the web
	'''

	#The base url is a static data member for the Tour class, but an instance member of the Tour object; it is consistent across
	#all instances of the Tour object and is therefore shared in common by all instances of the Tour class
	base_url = "http://maps.googleapis.com/maps/api/distancematrix/json?"

	#The set of all possible modes for traveling between cities is also consistent across different instances of tour
	modes = ImmutableSet(['driving','bicycling','walking'])


	def __init__(self, *args):
		self.locations = []
		self.distances = []
		self.total_distance = 0
		self.request_url = self.base_url
		for loc in args:
			self.locations.append(loc)
		self.calculate_consecutive_distances()
		self.total_distance = self.get_total_distance()


	def get_locations(self):
		'''
		Returns the list of tour locations

		>>> Tour('New York, NY','Buffalo,NY').get_locations()
		['New York, NY', 'Buffalo,NY']

		:return: List of tour stop locations stored in current tour object
		'''
		return self.locations

	#Helper Methods
	def reset_request_URL(self):
		'''Resets the current API-request URL to the base URL

		:return: None
		'''
		self.request_url = self.base_url

	#Helper Methods for Building API Request URL(applicable to a single origin-destination pair)
	def parse_city_state_string(self,city_state_string):
		'''Converts a string containing city name and state name with a comma delimiter into a tuple containing separate
		elements for the city string and state string

		Precondition:	The input string must have comma separator
		Postcondition:	The original string is unmodified

		:param 		A string in the format 'City, State' with a comma delimiter
		:return: 	A tuple with two members, the first being string for the city name, and the second being a string
					for the state name
		'''

		city_state_array = city_state_string.split(',')
		return tuple([city_state_array[0].strip(),city_state_array[1].strip()])

	def add_origin_to_base_url(self,tour_stop):
		'''Adds the name of origin tour-stop to the API request URL
		Precondition: 	The input is in the form of a two-membered tuple
		Postcondition: 	The request_url string instance variable has a query parameter for origin city embedded in the url
		:param 		tour_stop: a tuple containing string elements, one for the city name, the other for the state name
		:return: 	None
		'''
		city_subnames = tour_stop[0].split(' ')
		self.request_url += "origins="
		for subname in city_subnames:
			self.request_url += subname.strip() + '+'
		self.request_url += tour_stop[1].strip()

	def add_destination_to_base_url(self,tour_stop):
		'''Adds the tour-stop destination to the API-request URL
		Precondition: 	The input is in the form of a two-membered tuple, and the request url already has origin query
						parameter embedded in it
		Postcondition: 	The request_url string instance variable has a query parameter for origin and destination cities
		 				embedded in the url
		:param 		tour_stop: a tuple containing string elements, one for the city name, the other for the state name
		:return: 	None
		'''

		city_subnames = tour_stop[0].split(' ')
		self.request_url += "&destinations="
		for subname in city_subnames:
			self.request_url += subname.strip() + '+'
		self.request_url += tour_stop[1].strip()

	def add_mode_to_base_url(self,mode = "driving"):
		'''Adds the traveling mode the API-request URL

		:param 	mode: The possible traveling modes include driving, bicycling, and walking
		:return: None
		'''
		if mode not in self.modes:
			print("That mode is not valid") #change this implementation to raise a ValueError exception
		else:
			self.request_url += "&mode=" + mode.strip()

	def add_sensor_to_base_url(self,hasSensor = False):
		'''Adds the sensor parameter to the query string embedded in the API-request URL

		:param hasSensor: True if sensor=True, False if sensor=False in query URL-query string
		:return:
		'''
		self.request_url += "&sensor="
		if not hasSensor:
			self.request_url += "false"
		else:
			self.request_url +="true"

	#Overloaded Operators
	def get_request_url(self):
		return self.request_url

	def __add__(self, other):
		'''
		Arithmetic addition operator is overloaded so that the locations list in the the two operands can be concatenated.
		The locations list in the right-hand operand are concatenated to the end of the locations list in the left-hand operand


		:param other:
		:return:
		'''
		if(isinstance(other,Tour)):
			return self.locations + other.locations
		elif(isinstance(other,str)):
			return self.locations.append(other)
		else:
			return NotImplemented

	def __gt__(self, other):
		'''Greater than operator is overloaded so that if the total distance of one tour is greater than that of
		another, the result is True and False if otherwise

		>>> t1 = Tour('New York,NY','Los Angeles,CA')
		>>> t2 = Tour('New York,NY','Chicago,IL')
		>>> t1 > t2
		True


		:param other: Another tour object whose total distance is being compared to the current tour object
		:return:
		'''
		if(isinstance(other, Tour)):
			return self.total_distance > other.total_distance
		elif(isinstance(other, (int,float))):
			return self.total_distance > other
		else:
			return NotImplemented

	def __ge__(self, other):
		'''The >= operator is overloaded so that the total distance of one tour object can be compared to that of another

		>>> t1 = Tour("New York, NY","Chicago, IL")
		>>> t2 = Tour("New York, NY","Chicago,IL")
		>>> t3 = Tour("New York, NY","Buffalo, NY")
		>>> t1 >= t2
		True
		>>> t1 >= t3
		True
		>>> t3 >= t1
		False



		:param other:
		:return:
		'''
		if(isinstance(other, Tour)):
			return self.total_distance >= other.total_distance
		elif(isinstance(other, (int,float))):
			return self.total_distance >= other
		else:
			return NotImplemented

	def __eq__(self, other):
		'''The equality operator is overloaded such that two tour objects are equal if and only if their respective
		tour stop locations are the same and in the same order

		>>> t1 = Tour("New York,NY","Chicago, IL","Los Angeles,CA")
		>>> t2 = Tour("New York,NY"," Chicago,IL","Los Angeles,CA")
		>>> t3 = Tour("Los Angeles, CA", "Chicago,IL","New York,NY")
		>>> t5 = Tour("New York,NY","Chicago,IL","Los Angeles,CA","San Francisco,CA")
		>>> t1 == t2
		True
		>>> t1 == t3
		False
		>>> t1 == t5
		False

		:param other:
		:return:
		'''
		if(len(self.locations) != len(other.locations)):
			return False

		city_state_list = []
		other_city_state_list = []

		for loc in self.locations:
			city_state_tuple = self.parse_city_state_string(loc)
			city_state_list.append(city_state_tuple)

		for loc in other.locations:
			city_state_tuple = other.parse_city_state_string(loc)
			other_city_state_list.append(city_state_tuple)

		for loc1,loc2 in zip(city_state_list, other_city_state_list):
			if loc1 != loc2:
				return False
		return True

	def __ne__(self, other):
		return self != other

	def __lt__(self, other):
		'''The arithmetic less than (<) operator is overloaded such that the less than comparison yields True if
		the total distance for one tour object is less than the total distance of another object

		>>> t1 = Tour("New York, NY", "Chicago, IL")
		>>> t2 = Tour("New York, NY", "Boston, MA")
		>>> t2 < t1
		True
		>>> t2 > t1
		False

		:param other:
		:return:
		'''
		if (isinstance(other, Tour)):
			return self.total_distance < other.total_distance
		elif (isinstance(other, (int, float))):
			return self.total_distance < other
		else:
			return NotImplemented

	def __le__(self, other):
		'''The less than or equal (<=) arithmetic operator is overloaded such that a comparison yields True if the
		total distance for one tour object is less than or equal to the tour distance for another tour object

		>>> t1 = Tour("New York, NY","Chicago, IL")
		>>> t2 = Tour("New York,NY", "Chicago,IL")
		>>> t1 <= t2
		True
		>>> t3 = Tour("New York, NY","Los Angeles,LA")
		>>> t1 <= t3
		True

		:param other:
		:return:
		'''
		if (isinstance(other, Tour)):
			return self.total_distance <= other.total_distance
		elif (isinstance(other, (int, float))):
			return self.total_distance <= other
		else:
			return NotImplemented

	#__str__ and __repr__
	def __str__(self):
		output_str = "Tour Stops(in order): \n"
		for index, stop in enumerate(self.locations):
			output_str += str(index) + ": " + stop + "\n"
		return output_str

	def __repr__(self):
		output_string = ""
		for loc in self.locations:
			output_string += "{}; ".format(loc)
		return output_string


	def calculate_single_distance(self):
		from urllib2 import urlopen
		web_obj = urlopen(self.request_url)
		json_string = str(web_obj.read())
		web_obj.close()

		import json
		json_data = json.loads(json_string)
		returned_distance = json_data['rows'][0]['elements'][0]['distance']['value']
		self.distances.append(returned_distance)


	def get_consecutive_stops(self):
		origins = self.locations[0:-1]
		destinations = self.locations[1:]
		return zip(origins,destinations)

	def calculate_consecutive_distances(self, mode = "driving", hasSensor = False):
		consecutive_stops = self.get_consecutive_stops()
		for (origin,destination) in consecutive_stops:
			origin_tuple = self.parse_city_state_string(origin)
			destination_tuple = self.parse_city_state_string(destination)
			self.add_origin_to_base_url(origin_tuple)
			self.add_destination_to_base_url(destination_tuple)
			self.add_mode_to_base_url(mode)
			self.add_sensor_to_base_url(hasSensor)
			self.calculate_single_distance()
			self.reset_request_URL()

	def get_average_distance_between_stops(self):
		'''Calculates the average distance between stops on the tour


		:return: The mean distance among the set of consecutive distances between tour stops
		'''

		return statistics.mean(self.distances)

	def get_total_distance(self):
		return sum(self.distances)

	def get_distances(self):
		return self.distances


if __name__ == '__main__':
	import doctest
	doctest.testmod()


	t1 = Tour("New York, NY", "Lansing, MI", "Chicago, IL", "Houston, TX")
	t2 = Tour("Los Angeles, CA","Seattle, WA","Boise, ID")

	print(t1.get_distances())
	print(t1.get_total_distance())

	print(t2.get_distances())
	print(t2.get_total_distance())


	#print(t1.get_consecutive_stops())