import time


def fetch_data(param):
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


def main():
    result1 = fetch_data(1)
    print("Fetch 1 fully completed")
    result2 = fetch_data(2)
    print("Fetch 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()
t3=time.time_ns()
# main()## this runs the program but does not return the result1,result2
results = main()
print(results)
t4 =time.time_ns()
t2 = time.perf_counter()
print(f'finishedL {t4-t3}')
print(f"Finished in {t2 - t1:.3f} seconds")
