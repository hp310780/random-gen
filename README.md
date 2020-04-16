# random-gen #

![Python application](https://github.com/hp310780/random-gen/workflows/Python%20application/badge.svg)

A random number generator that will randomly generate numbers from a given input list and probability distribution.
E.g.
```python
>> from random_gen import RandomGen
>> 
>> r = RandomGen((1,2,3), (0.5,0.1,0.4)) # input number list, probability distribution
>> generated_numbers = [r.next_num() for _ in range(0, 11)] 
>>
>> import collections
>> collections.Counter(generated_numbers) # See distribution of numbers generated
Counter({1: 7, 2: 1, 3: 3})
```
As you can see, the distribution of numbers is roughly in line with the probability distribution passed to RandomGen.
This implementation is taken from cpython random.choices() - https://github.com/python/cpython/blob/master/Lib/random.py#L397
and optimised for known cumulative weights and k.

This works by using the cumulative probabilities of the random number list. Randomly generated probabilities (using `random.random`)
are multiplied by the total sum of the probabilities. This probability is then inserted into the list of cumulative
probabilities using `bisect.bisect` and that insert position used to return the relative random number (from the input `random_nums`). 
As the probability has been proportioned along the probability distribution (because it's multiplied
by the total sum of the probabilities) it is more likely to return numbers that have a larger probability.


## Prerequisites ##
* Python 3.6

## Running ##
```python
>> from random_gen import RandomGen
>> random_nums = (1,2,3)
>> probabilities = (0.5, 0.1, 0.4)
>> r = RandomGen(random_nums, probabilities)
>> r.next_num()
1
```

## Tests ##
* To run the tests: `pytest tests/test_random_gen.py`

## How to make RandomGen more 'pythonic' ##
We could subclass the standard Python `Generator` class and use the dunder methods to provide `next_num` through 
`__next__` or simply provide a generator function called `random_gen` which yields each result when called.  
I would also advise using `random.choices` directly rather than wrapped in a class if the use cases are less than ~10000
inputs (otherwise performance suffers). This would be simpler and more readable.

## Performance ##
| # input numbers provided | # output numbers generated | speed (secs) | function calls | memory consumption for next_num (mb) |
| :---: | :---: | :---: | :---:| :---: |
|100                      | 100                        |    0.005    | 304              |           11                         | 
|1000                     | 1000                       |    0.002    | 3004             |           11                         | 
|10000                    | 10000                      |    0.018    | 30004            |           12.4                       | 
|100000                   | 100000                     |    0.172    | 300004           |           33                         | 
|100000                   | 1000000                    |    1.95     | 3000004          |           199                        | 


## Further Optimisations ##
* Memory consumption needs investigation. Is there an alternative efficient method for bisecting the cumulative probability array 
without using a list?
* Arrays/efficient storage for large sets of numbers if needed.
* Investigate performance of bisect.
