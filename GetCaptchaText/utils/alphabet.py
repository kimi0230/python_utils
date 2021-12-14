import string

d = {**dict.fromkeys(string.ascii_uppercase, 0), **
     dict.fromkeys(string.ascii_lowercase, 0)}

a = [i for i in d.keys()]
a.sort()
for i in a:
    print(i)
