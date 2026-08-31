cache = {0: 0, 1: 1}

def fibonacci(n):

    for i in range (2, n + 1):

        if i not in cache:

            cache[i] = cache[i - 1] + cache[i - 2]

    return cache[n]

def is_positive_integer(text):

    try:

        return int(text) > 0

    except:

        pass

    return False
    
if __name__ == "__main__":

    import time

    while True:

        text = input("Please enter a positive integer: ")

        if not is_positive_integer(text):
            continue

        start = time.perf_counter()
        result = fibonacci(int(text))
        end = time.perf_counter()

        print(f"fibonacci({int(text)}) = {result}, calculating this took {end - start:.4e} seconds.")
