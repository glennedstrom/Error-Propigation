import math
from math import pi # in case you want to reference pi while calculating
import warnings
import re

#error propagation class
class err():
    """
    Error Propagation Calculating type

    err(number, ±error)

    Overloaded math functions to auto-calculate error:
    * / + - **

    *sigfigs don't work yet; they are commented out
    """
    vars = {} # convert user's letters to dictionary indexing syntax and replace the values in the formula with str.replace()

    def __init__(self, val, err, sig=-1):

        if sig == -1: #significant figures
            self.sig = self.sigfigs(val)
        else:
            self.sig = sig

        # warn if the input wasn't a string originally
        self.str = str(val)
        self.val = float(val)   # number
        self.err = float(err)   # plus/minus error

    def sigfigs(self, val): #do this before the number is a float, otherwise the number may have a different amount of sig figs than intended
        if '.' in val:
            return len(val.lstrip('0.').replace('.', ''))
        else:
            return len(val.strip('0'))

    # operation overloading

    def __add__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(str(o), 0)

        ans = self.val + o.val

        #sig figs (numbers after decimal) # -1 to remove decimal point
        sig = str(ans).index('.') + (min(len(str(self.val % 1)), len(str(o.val % 1))) - 1)

        print("sqrt(", self.err, "^2 + ", o.err, "^2)")
        return err(str(ans), math.sqrt(self.err**2 + o.err**2), sig)
    __radd__ = __add__

    def __sub__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(str(o), 0)

        ans = self.val - o.val

        #sig figs (numbers after decimal) # -1 to remove decimal point
        sig = str(ans).index('.') + (min(len(str(self.val % 1)), len(str(o.val % 1))) - 1)

        print("sqrt(", self.err, "^2 + ", o.err, "^2)")
        return err(str(ans), math.sqrt(self.err**2 + o.err**2), sig)

    def __rsub__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(str(o), 0)

        ans = o.val - self.val

        print("sqrt(", self.err, "^2 + ", o.err, "^2)")
        return err(str(ans), math.sqrt(self.err**2 + o.err**2), -1)

    def __mul__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(str(o), 0)

        ans = self.val * o.val

        error = math.sqrt((self.err/self.val)**2 + (o.err/o.val)**2)*ans
        print("sqrt((",self.err,"/",self.val,")^2 + (",o.err,"/",o.val,")^2)*",ans,"=",error)
        sig = self.sigfigs(str(ans))
        return err(str(ans), error, sig)
    __rmul__ = __mul__

    def __truediv__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(str(o), 0)
        ans = self.val / o.val
        error = math.sqrt((self.err/self.val)**2 + (o.err/o.val)**2)*ans
        print("sqrt((",self.err,"/",self.val,")^2 + (",o.err,"/",o.val,")^2)*",ans,"=",error)
        sig = self.sigfigs(str(ans))
        return err(str(ans), error, sig)

    def __rtruediv__(self, o):
        if type(o) != err:
            warnings.warn("WARNING: types do not match, autoconverting with o.err=0")
            o = err(str(o), 0)
        ans =  o.val / self.val
        error = math.sqrt((self.err/self.val)**2 + (o.err/o.val)**2)*ans
        print("sqrt((",self.err,"/",self.val,")^2 + (",o.err,"/",o.val,")^2)*",ans,"=",error)
        return err(str(ans), error)

    def __pow__(self, o):
        if type(o) != err: #exponents need to be exact
            o = err(str(o), 0)
        elif o.err != 0:# x**n; where n needs to have no error
            warnings.warn("WARNING: your exponent needs to be exact; ignoring error...")
        ans = self.val ** o.val
        derivative = o.val*self.val**(o.val-1)
        print("derivative = ", o.val, "*", self.val,"^(",o.val-1,") =",derivative)
        error = abs(derivative)*self.err
        print("|", derivative,"|*", self.err, "=", error)
        return err(str(ans), error)

    def __rpow__(self, o):
        if type(o) != err: #exponents need to be exact
            o = err(str(o), 0)
        elif self.err != 0:# x**n; where n needs to have no error
            warnings.warn("WARNING: your exponent needs to be exact; ignoring error...")

        ans =  o.val ** self.val
        derivative = self.val*o.val**(self.val-1)
        print("derivative = ", self.val, "*", o.val,"^(",self.val-1,") =", derivative)
        error = abs(derivative)*o.err
        print("|", derivative,"|*", o.err, "=", error)
        return err(str(ans), error)
    #output formatting
    def __str__(self):

        #decimals = len(str(self.val)) - self.sig-1#-1 for decimal point maybe
        #print(decimals)
        return str(self.val) + " ± " + str(self.err) + " ( % " + str(round(self.err/self.val*100,4)) + " )"


def main():
    while True:
        try:# for bad user input
            var = input("Enter a variable; none to continue: ")
            if var == '':
                break

            val = input(var + " = ")
            e = input(var + " = " + val + " ± ")

            err.vars[var] = err(val, e)

        except Exception as e:
            print(e)
    print("\nType your equations below, ctrl-c to exit\n")
    converted = ''
    while True:
        try:
            eq = input()
            if eq == '':#loop back to variable definition
                break

            converted = eq
            pattern = re.compile(r'(' + '|'.join(sorted(err.vars.keys(),key=len, reverse=True)) + r')') #match the keys in the order of their length longest to shortest to avoid repeats
            converted = pattern.sub(r'err.vars["\1"]', eq)
            [print(i, "=", err.vars[i]) for i in set(pattern.findall(eq))]
            print()

            print(eq + ' = ' + str(eval(converted))) # don't use eval unless you are the only user 
            print("\n")

        except Exception as e:
            print(str(e) + ": " + str(converted))
    main()#recursive call so you can go back and change variables


if __name__ == "__main__":
    main()
