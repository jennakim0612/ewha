import numpy as np

#-----------------------------
# 1. 데이터 학습시키기!
# 메일 단어 벡터 (0=없음, 1=있음)
# 단어 순서: ["무료", "제안", "클릭", "회의", "프로젝트"]
X = np.array([
    [1,1,1,0,0],  # 스팸
    [1,0,1,0,0],  # 스팸
    [0,0,0,1,1],  # 정상
    [0,0,0,1,0],  # 정상
    [1,1,0,0,0],  # 스팸
    [0,0,1,0,1]   # 정상
])

y = np.array(["스팸","스팸","정상","정상","스팸","정상"])

#-----------------------------
# 2. 사전확률 계산

P_spam = np.sum(y=="스팸") / len(y) #일반적인 스팸확률
P_ham  = np.sum(y=="정상") / len(y) #일반적인 정상확률
#len= 변수 개수의미! 여기서는 6.



#-----------------------------
# 3. 조건부확률 계산 (라플라스 스무딩)
alpha = 1
X_spam = X[y=="스팸"]
X_ham  = X[y=="정상"]

P_x_given_spam = (X_spam.sum(axis=0) + alpha) / (len(X_spam) + 2*alpha)
P_x_given_ham  = (X_ham.sum(axis=0) + alpha) / (len(X_ham) + 2*alpha)

#-----------------------------
# 4. 새로운 데이터로 예측.
# ex: ["무료","클릭"] 있는 메일
x_new = np.array([1,0,1,0,0])

# 사후확률 계산
posterior_spam = P_spam * np.prod(P_x_given_spam**x_new * (1-P_x_given_spam)**(1-x_new))
posterior_ham  = P_ham  * np.prod(P_x_given_ham**x_new * (1-P_x_given_ham)**(1-x_new))

if posterior_spam > posterior_ham:
    print("이 메일은 스팸입니다.")
else:
    print("이 메일은 정상 메일입니다.")