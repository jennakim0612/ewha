a=[]
a.append(input("이름? : "))
a.append(input("와플 또는 크로플? : "))
a.append(input("무슨 맛? : "))
a.append(int(input("몇개? :  ")))

print("="*30)
print(" %s은(는) %s맛 %s을 %d개 먹고싶대요!" %(a[0], a[2], a[1], a[3]))