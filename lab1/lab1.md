# CSCI 3212 Lab 1

## Fibonacci numbers

Source: https://en.wikipedia.org/wiki/Fibonacci_sequence  

The Fibonacci sequence is a sequence of numbers where:  
1. The first and second numbers are both ``1``, that is, ``fibonacci(1) = fibonacci(2) = 1``
2. The numbers that follow are the sum of the previous TWO numbers, so  
``fibonacci(3) = fibonacci(2) + fibonacci(1) = 1 + 1 = 2``  
``fibonacci(4) = fibonacci(3) + fibonacci(2) = 2 + 1 = 3``.

```
TODO: Answer the following questions:
fibonacci(5) = 5
fibonacci(6) = 8
fibonacci(7) = 13
fibonacci(8) = 21
fibonacci(9) = 34
```

## Basic implementation

Let's take a look at an implementation:
```python
def fibonacci(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
```
You can also find this in ``algorithms-labs-gw26/lab1/fibonacci.py``, and run it: 
```bash
cd algorithms-labs-gw26/lab1
python fibonacci.py
```
The code version also tells you how much time does it take to complete each calculation.
```
1. Explain what the code above is doing.
    A: The code is a recursive solution. First, it handles the base cases, which are eventually approached by the recursive calls (as n decreases constantly). If the number being considered is not a base case, it recursively adds preceding numbers in the Fibonacci sequence to arrive at the answer.
2. What happens if we remove the "if ... return ..." and only keep the last line?
    A: The code would have no stop case, and would crash from infinite recursion. 
3. What is fibonacci(20)? how much time did it take to calculate that?
    A: fibonacci(20) = 6765, and it took 4.6799e-02 seconds.
4. What is fibonacci(30)? how much time did it take to calculate that?
    A: fibonacci(30) = 832040, and it took 3.1642e-02 seconds.
5. How much time did it take you to calculate fibonacci(40)? (this might take a while...)
    A: fibonacci(40) = 102334155, and it took 2.9681e+00 seconds.
```

## How many function calls?

Modify ``fibonacci_counting.py`` so that it does the same calculation as ``fibonacci.py``, but it also counts how many times the function ``fibonacci(n)`` had to be called. Then answer the following:
```
TODO:
1. How many function calls does fibonacci(1) take?
    A: fibonacci(1) took 1 function call.
2. How many function calls does fibonacci(5) take?
    A: fibonacci(5) took 5 function calls.
3. How many function calls does fibonacci(10) take?
    A: fibonacci(10) took 177 function calls.
4. Why is it so slow? Where does the complexity come from?
    A: The complexity comes from the function call overhead of the recursive implementation coupled with the necessity of recomputing all preceding numbers of the sequence to derive each number. A more elegant solution would cache each derivation to minimize needless recomputation.
5. Is this O(n)? is this O(2^n)? Why?
    A: The Big O of this implementation is O(2^n). Each function call results in 2 more function calls. This leads to exponential growth.
6. Is this Ω(n)? Why?
    A: This Big Omega of this implementation is still Ω(2^n). Even for small values of n, each function call still results in 2 additional function calls, resulting in exponential growth.
```

## Memoization Optimization

Take a look at ``fibonacci_memoization.py``, where memoization is used.
```
TODO:
1. How is this one different from the previous one?
    A: This implementation caches preceding terms in the fibonacci sequence to minimize the number of redundant calls.
2. How much time does it take to calculate fibonacci(30)?
    A: It took 6.1600e-05 seconds.
3. Why is it often faster?
    A: It does not need to recursively recompute fibonacci numbers if the computation has already been done earlier in the algorithm.
4. Also modify this file to count: how many times the function had to be called for fibonacci(30)?
    A: The function had to be called 59 times.
5. Is this O(n)? is this O(2^n)? Why?
    A: This is O(n). Each value in the fibonacci sequence preceding the desired value only has to be computed once with memoization.
6. Is this Ω(n)? is this Ω(2^n)? Why?
    A: This is still Ω(n). Even for small values of n, each preceding value in the fibonacci still needs to be computed once.
```

## Extension: Staircase Problem

Implement ``fibonacci_threeway.py``, where:
1. The first, second, and third numbers are ``1``.
2. The numbers afterwards are the sum of the previous **THREE** numbers, instead of two.
3. Your implementation should be optimized, taking less than 1 second to calculate ``fibonacci_threeway(50)``.

## Optional, challenge problems
1. Instead of recursion, implement ``fibonacci(n)`` using iteration instead.
    
    A: Done in `fibonacci_challenge_1.py`
2. ``fibonacci_memoized.py`` fails if you give it a very large input number such as one million - why? Try fixing it.
    
    A: I recall that you can manually override the maximum recursion depth limit in Python using functionality in the sys library. I searched for the relevant sys documentation and implemented it. However, it is still unable to process the 

3. There is an even faster way to calculate fibonacci numbers, in (almost) O(1) time. Read Wikipedia and try to implement it, or if you like a big challenge, implement it without looking it up.
    
    A: Implemented Binet's Formula in `fibonacci_challenge_2.py`. We derived and proved this formula in Discrete Structures 1.
    https://artofproblemsolving.com/wiki/index.php/Binet%27s_Formula