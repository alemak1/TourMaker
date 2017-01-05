
import sys
from tours import *

input_str = ""
number_args = len(sys.argv)

for tour_stop in sys.argv:
    if(tour_stop != sys.argv[0] and tour_stop != sys.argv[number_args-1]):
        input_str += " \"" + tour_stop + "\", "
    elif (tour_stop == sys.argv[number_args-1]):
        input_str += " \"" + tour_stop + "\""



t1 = Tour(input_str)

print(t1)
print(t1.get_total_distance())
print("The total distance for your tour is: {}".format(t1.get_total_distance()))