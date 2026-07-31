a=[]
print('='*30)
a.append(input("이름은? "))
a.append(input("소속학교는? "))
a.append(int(input("행복도는? ")))

print("소속학교: %s, 이름: %s, 행복도: %d%%" %(a[1], a[0], a[2]))