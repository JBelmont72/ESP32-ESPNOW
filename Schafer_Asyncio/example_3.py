'''https://www.youtube.com/watch?v=oAkLSJNr5zY Corey Schafer asynchronous python
/Users/judsonbelmont/Documents/RandomNerd/ESP32-ESPNOW/Schafer_Asyncio/example_3.py
Important points!
this program runs asynchronously. I added my own Count function: need to remember two things.
1. the return for a loop must be outside the loop.
2. even though Count is defined as an async function and uses await asyncio.sleep(.1), it is currently being awaited directly in main(), which means it runs to completion before the program continues. This makes it behave synchronously in the context of your program.

To make Count run concurrently with the other tasks, you should create it as a task using asyncio.create_task() (just like you do with fetch_data). This way, all tasks can run in parallel, and the total runtime will be closer to the longest single task, not the sum of all their durations.
My correction for this was to move the creation of task3 = asyncio.create_task(Count(2)) to before the start awaiting any tasks.
Await all tasks at the end, after they've all been started. 


'''




import asyncio
import time


async def fetch_data(param):
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"

async def Count(param):
    count=0
    for i in range(0,4):
        count +=1
        print(count)
        await asyncio.sleep(.1)
    return count
    


async def main():
    task1 = asyncio.create_task(fetch_data(1))
    print(f'task1 coroutine object: {task1}')
    task2 = asyncio.create_task(fetch_data(2))
    print(f'task2 coroutine object: {task1}')
    task3 =asyncio.create_task(Count(2))
    print(f'count coroutine object: {task3}')
    result1 = await task1
    print("Task 1 fully completed")
    result2 = await task2
    

    
    
    
    result2 =await task2
    
    result3 = await task3
    print("Task 2 fully completed")
    return [result1, result2,result3]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()
print(f"Finished in {t2 - t1:.2f} seconds")
