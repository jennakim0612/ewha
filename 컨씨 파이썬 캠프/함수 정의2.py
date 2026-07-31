def get_info() :
    name=input("name: ")
    age=int(input("나이"))
    return name, age

a,b=get_info()
print(a,b)