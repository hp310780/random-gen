from itertools import accumulate
from collections import Counter

import pytest

from random_gen import RandomGen


@pytest.fixture(scope="module")
def delta():
    """Represents margin of deviance acceptable
    when comparing 'outputted' and expected probabilities."""
    return 0.1


def test_random_gen_setup():
    """Tests RandomGen correctly assigns class attributes from input."""
    random_nums = (1, 2, 3)
    probabilities = (0.2, 0.3, 0.5)
    r = RandomGen(random_nums, probabilities)

    assert r._random_nums == random_nums
    assert r._n == len(probabilities)
    assert r._cumulative_weights == list(accumulate(probabilities))
    assert r._total_weights == list(accumulate(probabilities))[-1]


def test_random_gen_empty_distribution():
    """Tests that differing lengths of _random_nums and probabilities raises a
    ValueError."""
    random_nums = (1, 2, 3)
    probabilities = ()

    with pytest.raises(ValueError):
        RandomGen(random_nums, probabilities)


def test_random_gen_zero_sum_distribution():
    """Tests that probabilities summing to zero raises a ValueError."""
    random_nums = (1, 2, 3)
    probabilities = (0, 0, 0)

    with pytest.raises(ValueError):
        RandomGen(random_nums, probabilities)


def test_random_gen_duplicate_random_nums():
    """Tests that duplicated random numbers raises a ValueError."""
    random_nums = (1, 2, 2)
    probabilities = (1, 1, 1)

    with pytest.raises(ValueError):
        RandomGen(random_nums, probabilities)


def test_next_num(delta):
    """Tests that RandomGen.next_num() produces numbers along the probability distribution given.
     Note that delta is the margin of deviance accepted."""
    random_nums = (1, 2, 3)
    probabilities = (0.2, 0.3, 0.5)
    r = RandomGen(random_nums, probabilities)
    generated_nums = []
    range_end = 1000

    for _ in range(0, range_end):
        generated_nums.append(r.next_num())

    nums_counter = Counter(generated_nums)

    assert nums_counter.get(1)/range_end == pytest.approx(probabilities[0], delta)
    assert nums_counter.get(2)/range_end == pytest.approx(probabilities[1], delta)
    assert nums_counter.get(3)/range_end == pytest.approx(probabilities[2], delta)


def test_next_num_uniform_distribution(delta):
    """Tests that RandomGen.next_num() distributes a uniform probability equally amongst the
    _random_nums inputted. Note that delta is the margin of deviance accepted."""
    random_nums = (1, 2, 3)
    probabilities = (1, 1, 1)
    r = RandomGen(random_nums, probabilities)

    generated_nums = []
    range_end = 1000

    for _ in range(0, range_end):
        generated_nums.append(r.next_num())

    nums_counter = Counter(generated_nums)

    expected_probability = 1/3
    assert nums_counter.get(1)/range_end == pytest.approx(expected_probability, delta)
    assert nums_counter.get(2)/range_end == pytest.approx(expected_probability, delta)
    assert nums_counter.get(3)/range_end == pytest.approx(expected_probability, delta)

