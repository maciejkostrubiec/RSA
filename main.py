import math
import random

Safety = 2 #Insert number to check (lower is more dangerous, but is faster to check if works)

# PART_1 Finding Primes

def isPrime(n):
    i = 2
    while (i*i <= n):
        if (n%i == 0):
            print("divisor: " + str(i))
            return False
        i += 1
    return True

def gcd(a, b):
    if (b):
        return gcd(b, a%b)
    else:
        return a

def findRandomdRelativelyFirst(n, max):
    probablyRelFirst = random.randrange(10,max)
    while (gcd(n, probablyRelFirst) != 1):
        probablyRelFirst = random.randrange(10,max)
    return probablyRelFirst

def quickPow(a, n):
    if (n == 0):
      return 1
    tempPow = quickPow(a, math.floor(n/2))
    tempPow = tempPow*tempPow
    if(n%2 == 1):
        tempPow = tempPow*a
    return tempPow

def preselectPassed(n):
    smallPrimes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,
73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,
179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,
283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,
419,421,431,433,439,443,449,457,461,463,467,479,487,491,499]
    for prime in smallPrimes:
        if (n%prime == 0):
            return False
    return True

def oneSmallFermatTest(n):
    testNumber = findRandomdRelativelyFirst(n, 10**(math.ceil(Safety/10)+2))
    if ((quickPow(testNumber, n-1))%n != 1):
        return False #Not passed - not first
    return True #Passed - probably first

def completeSmallFermatTest(n):
    for i in range(Safety):
        if (oneSmallFermatTest(n) == False):
            return False #Not passed - not first
    return True #Passed - probably first

def oneMiillerRabinTest(d, n):
    a = 2 + random.randrange(1, n-4)
    x = quickPow(a, d) % n
    if (x == 1 or x == n - 1):
        return True #Passed - probably first
    while (d != n - 1):
        x = (x * x) % n
        d *= 2
        if (x == 1):
            return False #Not passed - not first
        if (x == n - 1):
            return True #Passed - probably first
    return False #Not passed - not first

def completeMillerRabinTest(n):
    d = n - 1
    while (d%2 == 0):
        d //= 2
    for i in range(Safety):
        if (oneMiillerRabinTest(d, n) == False):
            return False #Not passed - not first
    return True #Passed - probably first

def findPrime(n):
    numProbablyFirst = False #True if we are sure that we have to look for another value
    while (not numProbablyFirst):
        randomNum = random.randrange(10**n+1,10**(n+1),2)
        if (preselectPassed(randomNum) == True):
            if (completeSmallFermatTest(randomNum) == True):
                if (completeMillerRabinTest(randomNum) == True):
                    numProbablyFirst = True
    return randomNum

# PART_2 RSA

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m

def encode(message):
    p = findPrime(Safety)
    q = findPrime(Safety)
    n = p*q
    euler = (p-1)*(q-1)
    e = findRandomdRelativelyFirst(euler, euler-1)
    d = modinv(e, euler)
    encodedMessage = [(ord(char) ** e) % n for char in message]
    return (encodedMessage, (n, e), (n, d))

def decode(message, n, d):
    decodedMessage = [chr((char ** d) % n) for char in message]
    decodedMessage = ''.join(decodedMessage)
    return decodedMessage

# PART_3 Tests

testList = ["", "Test", "Ala ma kota", "Zażółć Gęślą Jaźń!@#123789"]
testResults = []
for item in testList:
    x = encode(item)
    print(x)
    print(x[0])
    print(x[2][0])
    print(x[2][1])
    y = decode(x[0], x[2][0], x[2][1])
    print(y)
    testResults += [y]

print(testResults)
if (testResults == testList):
    print("All tests passed!")
else:
    print("Ooups, sthg went wrong...")



