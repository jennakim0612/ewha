import time

print("집중력 테스트입니다. 정확히 5초를 맞추어보세요.")

for i in range (3,0,-1):
    print("%d초전" %i)
    time.sleep(1)
    
    
st=time.time()
input("시작! 5초가 지났다는 순간 엔터!")
et=time.time()

print("정확한 시간은 %.2f초입니다." %(et-st))