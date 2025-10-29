double_sum = 1
sum_of_doubles = 1


for i in range(2, 101):
    double_sum += i
    sum_of_doubles += i * i
    
print(double_sum ** 2 - sum_of_doubles)