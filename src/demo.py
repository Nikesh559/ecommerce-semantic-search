import numpy as np
arr = np.array([1, 2, 3, 4, 5])
num_list = [1, 2, 3, 4, 5]
num_arr = {1,2,3,4,5}
print(type(arr))
print(num_list[1])
print(3 in num_list)
y:int = 4
print(y//3)
class Solution:
    def minCost(self, n: int) -> int:
        if n <= 1:
            return 0
        return ((n//2) * ((n+1)//2)) + self.minCost((int)(n//2)) + self.minCost((int)((n + 1)//2))

s = Solution()
print(s.minCost(6))
y = int(5)
print(int(y/2))
st = "Hello, World!"
for i in st:
    print(i)
new_st = st.replace("World", "Python");
print(str.replace(st, "World", "Python"))
print(len(new_st))
if "Python" in st:
    print("Found 'Hello' in the string.")

ages = [1,2,3,4,5]
x =45

for age in ages:
    fstr = f"My age is {age} years. {x}"
    print(fstr)

num_str1 = 1245
str1 = (num_str1)
print(type(str1))

my_list = [1,1,2,4]
print("Type ", type(my_list))
if 1 in my_list:
    print("Found 1 in the list.")

my_list.append(5)
print(my_list)

my_list.insert(0, 0)
print(my_list)
my_list[1]=10
print(my_list)
del my_list[2]
print(my_list)

r_list  = range(1, 10)
print(list(r_list))

for i in range(len(my_list)):
    print(my_list[i])
my_list.sort(reverse=True)
print(my_list)

# SET examples

num_set = {1, 2, 3, 4, 5}
print(num_set)
num_set.add(10)
print(num_set)

for num in num_set:
    print(num)
if 20 in num_set:
    print("Found 10 in the set.")
num_set.discard(20)
print(num_set)
num_set.clear()
print(num_set)


# DICTIONARY examples
my_dict = {"name": "Alice", "age": 30, "city": "New York", "name": "Bob"}
print(my_dict["name"])
print(len(my_dict))  
print(my_dict.keys())
print(my_dict.values())
print(type(my_dict.items()))
my_dict["age"] = 31
print(my_dict)
my_dict.update({"city": "Los Angeles", "country": "USA"})
print(my_dict)
del my_dict["country"]
print(my_dict)
for key, value in my_dict.items():
    print(f"{key}: {value}")
    print(key, value)

if "name" in my_dict:
    print("Found 'name' in the dictionary.")