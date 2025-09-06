'''
/Users/judsonbelmont/Downloads/AsyncIO-Schafer/terms.py'''


# import asyncio
# import time


# def sync_function(test_param: str) -> str:
#     print("This is a synchronous function.")

#     time.sleep(0.1)

#     return f"Sync Result: {test_param}"


# # ALSO KNOWN AS A COROUTINE FUNCTION, to run the main function need to start event loop with async.run(), a scheduler, control returns to event loop
# async def async_function(test_param: str) -> str:
#     print("This is an asynchronous coroutine function.")

#     await asyncio.sleep(0.1)

#     return f"Async Result: {test_param}"


# async def main():
#     sync_result = sync_function("Test")
#     print(sync_result)

#     # loop = asyncio.get_running_loop()
#     # future = loop.create_future()  # A promise-like object
#     # print(f"Empty Future: {future}")

#     # future.set_result("Future Result: Test")
#     # future_result = await future
#     # print(future_result)

#     # coroutine_obj = async_function("Test")
#     # print(coroutine_obj)

#     # coroutine_result = await coroutine_obj
#     # print(coroutine_result)

#     # task = asyncio.create_task(async_function("Test"))
#     # print(task)

#     # task_result = await task
#     # print(task_result)


# if __name__ == "__main__":
#     asyncio.run(main())
### copied above and will look at 'awaitables'

# import asyncio
# import time


# def sync_function(test_param: str) -> str:
#     print("This is a synchronous function.")

#     time.sleep(0.1)

#     return f"Sync Result: {test_param}"


# # ALSO KNOWN AS A COROUTINE FUNCTION, to run the main function need to start event loop with async.run(), a scheduler, control returns to event loop
# async def async_function(test_param: str) -> str:
#     print("This is an asynchronous coroutine function.")

#     await asyncio.sleep(0.1)

#     return f"Async Result: {test_param}"


# async def main():
#     # sync_result = sync_function("Test")   ##commented out from first version
#     # print(sync_result)
# ## await keyword. An object has to be 'awaitable' for asynchronous programming
# ## synchronous libraries do not have a way to yield control over to the event loop and sleep is blocking, they cannot stop their execution and be restarted later which is a ust for asynchronous
# ## to use the keyword 'await' must be within an async def function
# ## await means pause the current function and yield control back to the event loop unitl the awaitable is completed.
#     loop = asyncio.get_running_loop()   ## await  keyword implements the method __await__() under the hood 
#     future = loop.create_future()  # A promise-like object
#     print(f"Empty Future: {future}")

#     future.set_result("Future Result: Test")
#     future_result = await future
#     print(future_result)
# '''futures are like apromise of something in the future, we will not use, low-level use only
# futures hold a pending result. can be completed by provididng a result which will complegte the future 


# '''

#     # coroutine_obj = async_function("Test")
#     # print(coroutine_obj)

#     # coroutine_result = await coroutine_obj
#     # print(coroutine_result)

#     # task = asyncio.create_task(async_function("Test"))
#     # print(task)

#     # task_result = await task
#     # print(task_result)


# if __name__ == "__main__":
#     asyncio.run(main())

## copied the code above and will look at coroutines and tasks
# import asyncio
# import time
# # ALSO KNOWN AS A COROUTINE FUNCTION, to run the main function need to start event loop with async.run(), a scheduler, control returns to event loop
# async def async_function(test_param: str) -> str:
#     print("This is an asynchronous coroutine function.")

#     await asyncio.sleep(0.1)

#     return f"Async Result: {test_param}"


# ## await keyword. An object has to be 'awaitable' for asynchronous programming
# ## synchronous libraries do not have a way to yield control over to the event loop and sleep is blocking, they cannot stop their execution and be restarted later which is a ust for asynchronous
# ## to use the keyword 'await' must be within an async def function
# ## await means pause the current function and yield control back to the event loop unitl the awaitable is completed.

# '''futures are like apromise of something in the future, we will not use, low-level use only
# futures hold a pending result. can be completed by provididng a result which will complete in the future 
# Here we will only deal with coroutines and tasks
# COROUTINES are functions defined by the async def keywords, functions that can be paused
# The 'coroutine OBJECT' is the awaitable that gets returned when you call the async def funciton!
 
# important, below when the funciton is awaited, it is scheduled for completion and executed at the same time!
# '''
# async def main():
#     coroutine_obj = async_function("Test")  
#     print(coroutine_obj)        ### output: <coroutine object async_function at 0x103d119c0>
# # to get the coroutine object, we have to 'await' it and that gives us the coroutine result
#     coroutine_result = await coroutine_obj ## only at this point was the command inside the async function run. in this case it  printed as specified by the async_function(): 'This is an asynchronous coroutine function..
#     print(coroutine_result)     ## output:Async Result: Test
# ## the above coroutine runs without setting up the 'task' that follows
#     # task = asyncio.create_task(async_function("Test"))
#     # print(task)
#     # ## output:'  <Task pending name='Task-2' coro=<async_function() running at /Users/judsonbelmont/Documents/RandomNerd/ESP32-ESPNOW/Schafer_Asyncio/terms.py:116>>
#     #             # This is an asynchronous coroutine function.
#     #             # Async Result: Test'
#     # task_result = await task
#     # print(task_result)


# if __name__ == "__main__":
#     asyncio.run(main())
    
## next version is to discuss and explain 'tasks'    
import asyncio
import time

async def async_function(test_param: str) -> str:
    print("This is an asynchronous coroutine function.")

    await asyncio.sleep(0.1)

    return f"Async Result: {test_param}"

async def main():
    # coroutine_obj = async_function("Test")
    # print(coroutine_obj)

    # coroutine_result = await coroutine_obj
    # print(coroutine_result)

    task = asyncio.create_task(async_function("Test"))
    print(task)

    task_result = await task
    print(task_result)
    ## output: <Task pending name='Task-2' coro=<async_function() running at /Users/judsonbelmont/Documents/RandomNerd/ESP32-ESPNOW/Schafer_Asyncio/terms.py:160>>
                # This is an asynchronous coroutine function.
                # Async Result: Test

if __name__ == "__main__":
    asyncio.run(main())
