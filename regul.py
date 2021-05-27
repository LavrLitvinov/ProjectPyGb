import re
t1 = "w.googl.com"
t2 = "ww.googl.com"

t3 = "www.googl.com"

i = re.search("/(http[s]?:\/\/)?(www\.)?(?i)[a-z]{1}[a-z|0-9|\-]*(?-i)\.{1}[a-z]{1,4}", "www.googl.com") 
print(i)