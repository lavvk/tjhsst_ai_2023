import sys

#A
if sys.argv[1] == "A":
    num1 = int(sys.argv[2])
    num2 = int(sys.argv[3])
    num3 = int(sys.argv[4])       
    x = num1+num2+num3
    print(x)

#B
elif sys.argv[1] == "B":
    nums = []
    for arg in sys.argv[2:]:
        nums.append(int(arg))
    print(sum(nums))
    #C
elif sys.argv[1] == "C":
    nums = []
    for arg in sys.argv[2:]:
        nums.append(int(arg))
        
    divisible_by_three = []
    for num in nums:
        if num % 3 == 0:
            divisible_by_three.append(num)
        
    print(divisible_by_three)
#D
elif sys.argv[1] == "D":
    n = int(sys.argv[2])
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[i - 1] + fib_sequence[i - 2])
    print(fib_sequence)
#E
elif sys.argv[1] == "E":
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    values = []
    for k in range(start, end + 1):
        values.append(k**2 - 3*k + 2)
    print(values)
#F
elif sys.argv[1] == "F":
    side1 = float(sys.argv[2])
    side2 = float(sys.argv[3])
    side3 = float(sys.argv[4])
    if side1 + side2 > side3 and side1 + side3 > side2 and side2 + side3 > side1:
        s = (side1 + side2 + side3) / 2
        area = (s * (s - side1) * (s - side2) * (s - side3)) ** 0.5
        print(area)
    else:
        print( "invalid sides")
#G
elif sys.argv[1] == "G":
    x = sys.argv[2].lower()
    vowels = "aeiou"
    
    for vowel in vowels:
        count = x.count(vowel)
        print(vowel + ":", count)

