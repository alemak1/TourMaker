from sets import Set, ImmutableSet

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



	#Helper Methods
	def reset_request_URL(self):
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
		return tuple(city_state_array)

	def add_origin_to_base_url(self,tour_stop):
		'''
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
		'''
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
		if mode not in self.modes:
			print("That mode is not valid") #change this implementation to raise a ValueError exception
		else:
			self.request_url += "&mode=" + mode.strip()

	def add_sensor_to_base_url(self,hasCensor = False):
		self.request_url += "&sensor="
		if not hasCensor:
			self.request_url += "false"
		else:
			self.request_url +="true"

	#Overloaded Operators
	def get_request_url(self):
		return self.request_url

	def __add__(self, other):
		if(isinstance(other,Tour)):
			return self.locations + other.locations
		elif(isinstance(other,str)):
			return self.locations.append(other)
		else:
			return NotImplemented

	def __gt__(self, other):
		if(isinstance(other, Tour)):
			return self.total_distance > other.total_distance
		elif(isinstance(other, (int,float))):
			return self.total_distance > other
		else:
			return NotImplemented

	def __ge__(self, other):
		if(isinstance(other, Tour)):
			return self.total_distance >= other.total_distance
		elif(isinstance(other, (int,float))):
			return self.total_distance >= other
		else:
			return NotImplemented

	def __eq__(self, other):
		if(len(self.locations) != len(other.locations)):
			return False

		for loc1,loc2 in zip(self.locations, other.locations):
			if loc1 != loc2:
				return False
		return True

	def __ne__(self, other):
		return self != other

	def __lt__(self, other):
		if (isinstance(other, Tour)):
			return self.total_distance < other.total_distance
		elif (isinstance(other, (int, float))):
			return self.total_distance < other
		else:
			return NotImplemented

	def __le__(self, other):
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


	def get_total_distance(self):
		return sum(self.distances)

	def get_distances(self):
		return self.distances


if __name__ == '__main__':


	t1 = Tour("New York, NY", "Lansing, MI", "Chicago, IL", "Houston, TX")
	t2 = Tour("Los Angeles, CA","Seattle, WA","Boise, ID")

	print(t1.get_distances())
	print(t1.get_total_distance())

	print(t2.get_distances())
	print(t2.get_total_distance())


	#print(t1.get_consecutive_stops())