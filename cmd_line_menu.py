
import sys
from tours import *

input_str = ""
for tour_stop in sys.argv:
    input_str += tour_stop


t1 = Tour(input_str)

print("The total distance for your tour is: {}".format(t1.get_total_distance()))