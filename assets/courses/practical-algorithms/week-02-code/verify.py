"""Check solutions, or run with --student after implementing student_week_02.py."""
import importlib
from itertools import product
from fractions import Fraction
import math
import random
import sys

student = '--student' in sys.argv
impl = importlib.import_module('student_week_02' if student else 'solutions')
checks = 0


def check(actual, expected):
    global checks
    assert actual == expected, (actual, expected)
    checks += 1


def unique_baseline(text):
    return max((end - start for start in range(len(text))
                for end in range(start + 1, len(text) + 1)
                if len(set(text[start:end])) == end - start), default=0)


def sum_baseline(target, nums):
    return min((end - start for start in range(len(nums))
                for end in range(start + 1, len(nums) + 1)
                if sum(nums[start:end]) >= target), default=0)


for size in range(7):
    for chars in product('ab ', repeat=size):
        text = ''.join(chars)
        check(impl.longest_unique(text), unique_baseline(text))
check(impl.longest_unique('abba c'), 4)
check(impl.longest_unique('x' * 100000), 1)

for size in range(1, 6):
    for values in product((1, 2, 4), repeat=size):
        nums = list(values)
        for target in range(1, sum(nums) + 2):
            check(impl.min_subarray(target, nums), sum_baseline(target, nums))
        if not student:
            for width in range(1, size + 1):
                check(impl.fixed_window_sums(nums, width),
                      [sum(nums[i:i + width]) for i in range(size - width + 1)])
check(impl.min_subarray(1000000000, [10000] * 100000), 100000)
check(impl.min_subarray(1000000000, [1] * 100000), 0)

rng = random.Random(20261110)
stacks = [impl.MinStack(), impl.MinStack()]
models = [[], []]
for _ in range(3000):
    index = rng.randrange(2)
    stack, model = stacks[index], models[index]
    if not model or rng.random() < 0.55:
        value = rng.choice([-2147483648, -2, 0, 2, 2, 2147483647])
        stack.push(value)
        model.append(value)
    else:
        stack.pop()
        model.pop()
    for stack, model in zip(stacks, models):
        if model:
            check(stack.top(), model[-1])
            check(stack.getMin(), min(model))

for left in range(-8, 9):
    for right in range(-8, 9):
        for op in '+-*/':
            if op == '/' and right == 0:
                continue
            expected = {'+': lambda: left + right, '-': lambda: left - right,
                        '*': lambda: left * right,
                        '/': lambda: math.trunc(Fraction(left, right))}[op]()
            check(impl.rpn([str(left), str(right), op]), expected)


def expression(depth):
    if depth == 0 or rng.random() < 0.3:
        value = rng.randint(-5, 5)
        return [str(value)], value
    left_tokens, left = expression(depth - 1)
    right_tokens, right = expression(depth - 1)
    op = rng.choice('+-*/' if right else '+-*')
    value = {'+': lambda: left + right, '-': lambda: left - right,
             '*': lambda: left * right,
             '/': lambda: math.trunc(Fraction(left, right))}[op]()
    return left_tokens + right_tokens + [op], value


for _ in range(400):
    tokens, expected = expression(3)
    check(impl.rpn(tokens), expected)
check(impl.rpn(['9', '4', '-', '-2', '/']), -2)
check(impl.rpn(['-2']), -2)
print(f'{checks} checks passed ({impl.__name__}).')
