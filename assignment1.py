"""
In this assignment you should interpolate the given function.
"""

import numpy as np
import time
import random
import math

class Assignment1:
    def __init__(self):
        """
        Here goes any one time calculation that need to be made before
        starting to interpolate arbitrary functions.
        """

        pass

    def interpolate(self, f: callable, a: float, b: float, n: int) -> callable:
        """
        Interpolate the function f in the closed range [a,b] using at most n
        points. Your main objective is minimizing the interpolation error.
        Your secondary objective is minimizing the running time.
        The assignment will be tested on variety of different functions with
        large n values.

        Interpolation error will be measured as the average absolute error at
        2*n random points between a and b. See test_with_poly() below.

        Note: It is forbidden to call f more than n times.

        Note: This assignment can be solved trivially with running time O(n^2)
        or it can be solved with running time of O(n) with some preprocessing.
        **Accurate O(n) solutions will receive higher grades.**

        Note: sometimes you can get very accurate solutions with only few points,
        significantly less than n.

        Parameters
        ----------
        f : callable. it is the given function
        a : float
            beginning of the interpolation range.
        b : float
            end of the interpolation range.
        n : int
            maximal number of points to use.

        Returns
        -------
        The interpolating function.
        """
        data_point = []
        points = np.linspace(a, b, n)
        for x in points:
            data_point.append((x, f(x)))

        def g(x):
            for point in range(len(data_point) - 1):
                if data_point[point][0] <= x <= data_point[point + 1][0]:
                    y = np.linspace(data_point[point][1], data_point[point + 1][1], 4)
                    y1 = y[0]
                    y2 = y[1]
                    y3 = y[2]
                    y4 = y[3]
                    t_bezier = (x - data_point[point][0]) / (data_point[point + 1][0] - data_point[point][0])
                    return y4 * t_bezier ** 3 + 3 * y3 * t_bezier ** 2 * (1 - t_bezier) + 3 * y2 * t_bezier * (1 - t_bezier) ** 2 + y1 * (1 - t_bezier) ** 3
        return g

##########################################################################

import unittest
from functionUtils import *
from tqdm import tqdm

class TestAssignment1(unittest.TestCase):

    def test_with_poly(self):
        T = time.time()

        ass1 = Assignment1()
        mean_err = 0

        d = 30
        for i in tqdm(range(100)):
            a = np.random.randn(d)

            f = np.poly1d(a)

            ff = ass1.interpolate(f, -10, 10, 100)

            xs = np.linspace(-10, 9.9, 200)
            y = [f(x) for x in xs]
            yy = [ff(x) for x in xs]
            xs = np.random.random(200)
            err = 0
            for x in xs:
                yy = ff(x)
                y = f(x)
                err += abs(y - yy)

            err = err / 200
            mean_err += err
        mean_err = mean_err / 100

        T = time.time() - T
        print(T)
        print(mean_err)

    def test_with_poly_restrict(self):
        ass1 = Assignment1()
        a = np.random.randn(5)
        f = RESTRICT_INVOCATIONS(10)(np.poly1d(a))
        ff = ass1.interpolate(f, -10, 10, 10)
        xs = np.random.random(20)
        for x in xs:
            yy = ff(x)

if __name__ == "__main__":
    unittest.main()