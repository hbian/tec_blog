# Set default value to a dictionary

from collections import defaultdict
a = {} 
a = defaultdict(lambda:0,a)

a["anything"] # => 0