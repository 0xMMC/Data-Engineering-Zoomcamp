import pandas as pd
import sys

# do something

print(sys.argv)

# sys.argv[0] is the name of the file
# sys.argv[1] is whatever argument we pass after
# sys.argv[2] is whatever we pass afterwards etc

day = sys.argv[1]

print(f'Job finished successfully on day = {day}!')

