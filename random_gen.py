import random
import bisect
from itertools import accumulate


class RandomGen(object):
    """
    Takes random numbers and a probability distribution. When self.next_num() is called,
    it will generate random numbers from those inputted along this probability
    distribution. Random numbers and probability list must be of the
    same length.
    """
    def __init__(self, random_nums, probabilities):
        """
        Args:
          random_nums (Tuple[int]): Tuple of random numbers.
          probabilities (Tuple[int]): Tuple of probabilities.
        """
        if len(probabilities) != len(random_nums):
            raise ValueError('The number of probabilities does not match the number of random numbers.')

        if len(set(random_nums)) != len(random_nums):
            raise ValueError('Duplicates numbers found in random numbers.')

        self._random_nums = random_nums
        self._random = random.random
        self._n = len(self._random_nums)
        # turns list of probabilities into cumulative sum
        self._cumulative_weights = list(accumulate(probabilities))
        self._total_weights = self._cumulative_weights[-1]

        if self._total_weights <= 0.0:
            raise ValueError('Total of probabilities must be greater than zero.')

    def next_num(self):
        """When this method is called multiple times over a long period,
        it should return the numbers roughly with the initialised probabilities.

        This implementation is taken from cpython random.choices() -
        https://github.com/python/cpython/blob/master/Lib/random.py#L397
        And optimised for known cumulative weights and k.

        Returns:
            Int. One of the self._random_nums.
        """
        return self._random_nums[bisect.bisect(self._cumulative_weights, self._random() * self._total_weights)]
