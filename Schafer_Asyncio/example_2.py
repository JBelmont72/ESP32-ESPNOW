import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = fetch_data(1)  # Could be awaited directly task i is coroutine object
    print(f'task1 coroutine object: {task1}')
    task2 = fetch_data(2)  # Could be awaited directlytask 2 is a coroutine object
    print(f'Task2 coroutine object {task2}')
    result1 = await task1   #   await task1 is 'scheduling' and 'running to completion' task1
    print("Task 1 fully completed")
    result2 = await task2   #   await task1 is 'scheduling' and 'running to completion' task1
    print("Task 2 fully completed")
    return [result1, result2]   #   there is no saving of time. not synchronous 


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.4f} seconds")
