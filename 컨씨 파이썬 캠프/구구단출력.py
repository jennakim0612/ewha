n=int(input("몇 단을 출력할까요? : "))

for x in range(1, 51) :
    print("%d * %d = %d" %(n, x, n*x))