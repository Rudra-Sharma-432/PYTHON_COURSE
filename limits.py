import sys
print(sys.float_info.dig) # significant decimal digits of precision
print(sys.float_info.max) # largest representable float
print(sys.float_info.min) # smallest representable float


print(f"{0.1:.20f}")
print(f"{0.2:.20f}")
print(f"{0.3:.20f}")
print(f"{0.1 + 0.2:.20f}")



print(0.1 + 0.2 == 0.3) # direct ==
print(round(0.1 + 0.2, 1) == 0.3) # round first
import math
print(math.isclose(0.1 + 0.2, 0.3)) # tolerance-based


print("="*35)
print(f'{math.pi}^4 + {math.pi}^5 ~ {math.e}^6')
print(math.pi**4 + math.pi**5, math.e**6)
print(math.isclose(math.pi**4 + math.pi**5, math.e**6))

print(f'{math.e} ^ {math.pi} - {math.pi} ~ 20')
print(math.e**math.pi - math.pi)
print(math.isclose(math.e**math.pi - math.pi, 20))

print("=" * 35)
