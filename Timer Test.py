import time

start_time = time.time()
print(start_time)

# The thing to time. Using sleep as an example
time.sleep(1)

end_time = time.time()
elapsed_time = end_time - start_time

print(elapsed_time)