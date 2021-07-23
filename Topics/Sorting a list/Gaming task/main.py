# the follwing line reads the list from the input, do not modify it, please
toys = input().split()

# your code below
toys.sort(key=len)
print(toys)
