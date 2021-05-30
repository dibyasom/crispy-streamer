import concurrent.futures
import time


def work(seconds):
    print(f"Sleeping for {seconds} second(s)....")
    time.sleep(seconds)
    return "Done sleeping."


if __name__ == "__main__":

    start = time.perf_counter()

    # t1 = threading.Thread(target=work)
    # t2 = threading.Thread(target=work)

    # threads = []
    # for _ in range(10):
    #     t = threading.Thread(target=work, args=[1.5])
    #     t.start()
    #     threads.append(t)

    # for thread in threads:
    #     thread.join()

    '''Concurrency should be used with context manager.'''
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Schedules function execution, returns a future object
        
        executors = [executor.submit(work, 1+round(i/10, 2))
                     for i in range(10)]

        for job in concurrent.futures.as_completed(executors):
            print(job.result())

    finish = time.perf_counter()
    print(f"Work done in {round(finish-start,2)} second(s)")
