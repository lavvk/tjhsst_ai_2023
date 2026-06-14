import sys

# second assignment: (one line of code per question)

s = sys.argv[1]

# 1
print(s[2])

# 2
print(s[4])

# 3
print(len(s))

# 4
print(s[0])

# 5
print(s[-1])

# 6
print(s[-2])

# 7
print(s[2:7])

# 8
print(s[-5:])

# 9
print(s[2:])

# 10
print(s[::2])

# 11
print(s[1::3])

# 12
print(s[::-1])

# 13
print(s.find(' '))

# 14
print(s[:-1])

# 15
print(s[1:])

# 16
print(s.lower())

# 17
print(s.split(' '))

# 18
print(len(s.split(' ')))

# 19
print([c for c in s])

# 20
print(''.join(sorted(s)))

# 21
print(s[:s.find(' ')] if ' ' in s else s)

# 22
print(s == s[::-1])
