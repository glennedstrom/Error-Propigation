import math
import warnings

#error propagation class
class err():
    """
    Error Propagation Calculating type

    err(number, ±error)

    Overloaded math functions to auto-calculate error:
    * / + - **

    """
    used_funct = []

    def __init__(self, val, err):
        self.val = val
        self.err = err

    # operation overloading

    def __add__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(o, 0)
        return err(self.val + o.val, math.sqrt(self.err**2 + o.err**2))

    def __sub__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(o, 0)
        return err(self.val - o.val, math.sqrt(self.err**2 + o.err**2))

    def __mul__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(o, 0)
        ans = self.val * o.val
        answer = math.sqrt((self.err/self.val)**2 + (o.err/o.val)**2)*ans
        return err(ans, answer)

    def __truediv__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(o, 0)
        ans = self.val / o.val
        answer = math.sqrt((self.err/self.val)**2 + (o.err/o.val)**2)*ans
        return err(ans, answer)

    def __pow__(self, o):
        if type(o) != err: #exponents need to be exact
            o = err(o, 0)
        elif o.err != 0:# x**n; where n needs to have no error
            warnings.warn("WARNING: your exponent needs to be exact; ignoring error...")
        ans = self.val ** o.val
        derivative = o.val*self.val**(o.val-1)
        answer = abs(derivative)*self.err
        return err(ans, answer)

    #output formatting
    def __str__(self):
        return str(self.val) + " ± " + str(self.err)


if __name__ == "__main__":
    test = err(15, .5)
    test2 = err(20, .5)

    d=err(120, 3)
    t=err(20.0, 1.2)
    print("Velocity:", d/t)

    w=err(4.52, 0.02)
    x=err(2.0, 0.02)
    y=err(3.0, .6)
    print("product and power", w*x+y**2)
