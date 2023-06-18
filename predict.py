
import time
"""

2.5*30% + A*30% +B*40%

A >= (3.0 - 2.530% - B40%) / 30%
B >= (3.0 - 2.530% - A30%) / 40%




B = (3.0 - 2.530%) - A30% / 40%

2.8*30% + 2.8*30% + 3.5*40%

"""



def calculate():
    first_calification = 2.2
    result = 0
    A = 0.0
    while True:
        B = (((3.0 - (first_calification * .3)) - A*.3) / .4)
        B = round(B, 1)
        A = round(A, 1)
        R = (first_calification * .3 + A * .3 + B * .4)

        if R == 3.0 and A >= 3.0 and B <= 5.0:
            print(first_calification)
            print(A)
            print(B)
            print()
            break

        #time.sleep(.5)
        A += .1

calculate()