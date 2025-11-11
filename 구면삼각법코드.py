import math

# 지구 반지름
R = 6371

# 도시별 위도/경도 (도)
seoul = (37.5665, 126.9780)
london = (51.5074, -0.1278)
cape_town = (-33.9249, 18.4241)

# 라디안 변환
def to_rad(deg):
    return math.radians(deg)

def spherical_angle(lat1, lon1, lat2, lon2):
    # 중심각(호의 각도) 구하는 구면 코사인 법칙 (특수형)
    phi1 = to_rad(lat1)
    phi2 = to_rad(lat2)
    delta_lambda = to_rad(lon2 - lon1)
    cos_c = math.sin(phi1)*math.sin(phi2) + math.cos(phi1)*math.cos(phi2)*math.cos(delta_lambda)
    cos_c = min(1, max(-1, cos_c))  # 수치 안정성
    return math.acos(cos_c)  # 라디안 반환

# 중심각 a = ∠BOC = 런던–케이프타운
a = spherical_angle(london[0], london[1], cape_town[0], cape_town[1])
# 중심각 b = ∠AOC = 서울–케이프타운
b = spherical_angle(seoul[0], seoul[1], cape_town[0], cape_town[1])

# 각 C = 케이프타운 각도 ≈ 위도 기준 추정 또는 내적 기반 계산도 가능
# 여기선 간단화 위해 내적 기반으로 계산해보기
def angle_at_C(A, B, C):
    # A, B, C: (lat, lon)
    def to_xyz(lat, lon):
        lat, lon = map(to_rad, (lat, lon))
        return [
            math.cos(lat) * math.cos(lon),
            math.cos(lat) * math.sin(lon),
            math.sin(lat)
        ]
    a = to_xyz(*A)
    b = to_xyz(*B)
    c = to_xyz(*C)

    def dot(u, v):
        return sum(ui*vi for ui, vi in zip(u, v))
    
    ca = [ai - ci for ai, ci in zip(a, c)]
    cb = [bi - ci for bi, ci in zip(b, c)]
    
    dot_product = dot(ca, cb)
    norm_ca = math.sqrt(dot(ca, ca))
    norm_cb = math.sqrt(dot(cb, cb))
    
    cos_angle = dot_product / (norm_ca * norm_cb)
    cos_angle = min(1, max(-1, cos_angle))
    return math.acos(cos_angle)

C_angle = angle_at_C(seoul, london, cape_town)

# 구면 코사인 법칙: cos c = cos a cos b + sin a sin b cos C
cos_c = math.cos(a) * math.cos(b) + math.sin(a) * math.sin(b) * math.cos(C_angle)
cos_c = min(1, max(-1, cos_c))
c = math.acos(cos_c)

# 거리
distance = R * c

print(f"서울–런던 구면 거리 (변 c): {distance:.2f} km")
print(f"중심각 c (라디안): {c:.4f}, (도): {math.degrees(c):.2f}°")
