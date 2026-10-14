#https://github.com/t-oka0428/kyopro/blob/main/geometry.py

from functools import cmp_to_key
import collections
import random
import math

#float配列Pの中身を空白区切りでe表記を避けて表示
def pf(P):
  N = len(P)
  for i in range(N):
    if i == 0:
      print(f"{P[i]:f}",end = "")
    else:
      print(f" {P[i]:f}",end = "")
  print()

def abs2(p):
  x,y = p
  return x*x + y*y

def scalar(r,p):
  return (r*p[0],r*p[1])

def dot_product(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  return x1*x2 + y1*y2

def cross_product(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  return x1*y2 - x2*y1

def vec(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  return (x2-x1,y2-y1)

def plus(P):
  x,y = 0,0
  for i in P:
    x += i[0]
    y += i[1]
  return (x,y)

def dist2(p1,p2):
  return abs2(vec(p1,p2))

#pからp1p2への垂線の足
def projection(p1,p2,p):
  x1,y1 = p1
  x2,y2 = p2
  x,y = p
  t = dot_product(vec(p1,p),vec(p1,p2)) / dist2(p1,p2)
  px,py = x1 + t*vec(p1,p2)[0], y1 + t*vec(p1,p2)[1]
  return (px,py)

#p1p2におけるpの対称点
def reflection(p1,p2,p):
  x1,y1 = p1
  x2,y2 = p2
  x,y = p
  d = projection(p1,p2,p)
  px,py = plus([d, vec(p, d)])
  return (px,py)

#偏角比較 p1 < p2 なら -1, p1 == p2 なら 0, p1 > p2 なら 1
#p1,p2 != (0,0)
def declination(p1,p2):
  x1,y1 = p1[:2]
  x2,y2 = p2[:2]
  a1 = y1 > 0 or (y1 == 0 and x1 > 0)
  a2 = y2 > 0 or (y2 == 0 and x2 > 0)
  if a1 == a2:
    c = cross_product(p1[:2],p2[:2])
    if c > 0:
      return -1
    elif c == 0:
      return 0
    else:
      return 1
  else:
    if a1:
      return -1
    else:
      return 1

#偏角ソート
#点群Pを反時計回りに並べ替えて返す
def declination_sorted(P):
  P.sort(key = cmp_to_key(declination))
  return P

#線分p0p1と線分p2p3が交差するか
#端点を含む
def intersect(p0,p1,p2,p3):
  v1,v2 = vec(p0,p1),vec(p2,p3)
  if cross_product(v1,v2) == 0:
    if cross_product(v1, vec(p0, p2)) == 0:
      if p0 > p1:
        p0,p1 = p1,p0
      if p2 > p3:
        p2,p3 = p3,p2
      if p0 > p2:
        p0,p1,p2,p3 = p2,p3,p0,p1
      if dist2(p0,p1) >= dist2(p0,p2):
        return True
      else:
        return False
    else:
      return False
  else:
    v1,v2 = vec(p0,p1),vec(p2,p3)
    a1 = cross_product(v1, vec(p0, p2)) * cross_product(v1, vec(p0, p3))
    a2 = cross_product(v2, vec(p2, p0)) * cross_product(v2, vec(p2, p1))
    return a1 <= 0 and a2 <= 0

#直線p0p1と直線p2p3の交点
def cross_point(p0,p1,p2,p3):
  v1,v2 = vec(p0,p1),vec(p2,p3)
  x0,y0 = p0
  x2,y2 = p2
  vx1,vy1 = v1
  vx2,vy2 = v2
  t1 = (- vy2*(x2-x0) + vx2*(y2-y0)) / (- vx1*vy2 + vx2*vy1)
  t2 = (- vy1*(x2-x0) + vx1*(y2-y0)) / (- vx1*vy2 + vx2*vy1)
  px = x0 + vx1*t1
  py = y0 + vy1*t1
  return (px,py)

#線分p1p2と点pの距離の二乗
def distance_of_point_and_segment(p1,p2,p):
  if dot_product(vec(p1, p), vec(p1, p2)) < 0:
    return dist2(p1, p)
  if dot_product(vec(p2, p), vec(p2, p1)) < 0:
    return dist2(p2, p)
  else:
    d = projection(p1,p2,p)
    return dist2(d, p)

#線分p0p1と線分p2p3の距離の二乗
def distance_of_segments(p0,p1,p2,p3):
  if intersect(p0,p1,p2,p3):
    return 0
  m0 = distance_of_point_and_segment(p0,p1,p2)
  m1 = distance_of_point_and_segment(p0,p1,p3)
  m2 = distance_of_point_and_segment(p2,p3,p0)
  m3 = distance_of_point_and_segment(p2,p3,p1)
  return min(m0,m1,m2,m3)

#半時計回りに並んだ点列Pがなす多角形の面積
#凸でなくても良い
def area(P):
  N = len(P)
  c = 0
  for i in range(1,N-1):
    v1,v2 = vec(P[0],P[i]),vec(P[0],P[i+1])
    c += cross_product(v1,v2)
  c /= 2
  return c

#半時計回りに並んだ点列Pがなす多角形が凸かどうか
#line：内角180度を許容するか否か
def is_convex(P,line):
  N = len(P)
  for i in range(N):
    v1,v2 = vec(P[i],P[(i+1)%N]),vec(P[i],P[(i+2)%N])
    if line and cross_product(v1,v2) < 0:
      return False
    if not line and cross_product(v1,v2) <= 0:
      return False
  return True

#半時計回りに並んだ点列Pがなす多角形のどこに点pがあるか O(len(P))で
#凸でなくても良い
#外部なら0, 境界なら1, 内部なら2
#INFは適宜変更
def conteined_in_convex(P,p):
  for i in range(N):
    v1,v2 = vec(P[i],P[(i+1)%N]),vec(P[i],p)
    if cross_product(v1,v2) == 0 and dot_product(v1,v2) >= 0 and abs2(v1) >= abs2(v2):
      return 1
  INF = 10**18
  p0 = (INF,p[1])
  c = 0
  for i in range(N):
    if intersect(P[i],P[(i+1)%N],p,p0):
      if (p[1] > P[i][1]) != (p[1] > P[(i+1)%N][1]):
        c += 1
  if c % 2 == 0:
    return 0
  else:
    return 2

#凸包構築
#line：内角180度を許容するか否か
def convex(P,line):
  N = len(P)
  P.sort()
  q1 = collections.deque()
  for i in range(N):
    while len(q1) >= 2:
      v1,v2 = vec(q1[-2],q1[-1]),vec(q1[-2],P[i])
      if line and cross_product(v1,v2) < 0:
        q1.pop()
      elif not line and cross_product(v1,v2) <= 0:
        q1.pop()
      else:
        break
    q1.append(P[i])
  q2 = collections.deque()
  for i in range(N-1,-1,-1):
    while len(q2) >= 2:
      v1,v2 = vec(q2[-2],q2[-1]),vec(q2[-2],P[i])
      if line and cross_product(v1,v2) < 0:
        q2.pop()
      elif not line and cross_product(v1,v2) <= 0:
        q2.pop()
      else:
        break
    q2.append(P[i])
  Q = []
  while len(q1) > 1:
    Q.append(q1.popleft())
  while len(q2) > 1:
    Q.append(q2.popleft())
  return Q

#closest_pair用の再帰関数
#点群P[l:r]の答えと,内部の点をy座標で昇順に並べたindex配列
#INFは適宜変更
def closest_pair_sub(P,l,r):
  INF = 4*10**18
  if r-l <= 1:
    return INF,[l]
  mid = (l+r)//2

  dl,y_sorted_point_l = closest_pair_sub(P,l,mid)
  dr,y_sorted_point_r = closest_pair_sub(P,mid,r)
  q1 = collections.deque(y_sorted_point_l)
  q2 = collections.deque(y_sorted_point_r)
  y_sorted_point = []
  while q1 or q2:
    if q1 and q2:
      if P[q1[0]][1] <= P[q2[0]][1]:
        y_sorted_point.append(q1.popleft())
      else:
        y_sorted_point.append(q2.popleft())
    elif q1:
      y_sorted_point.append(q1.popleft())
    else:
      y_sorted_point.append(q2.popleft())

  q = collections.deque()
  mid_x = P[mid][0]
  d = min(dl,dr)
  d0 = d
  for i in y_sorted_point:
    if abs(P[i][0] - mid_x)**2 < d0:
      while q and abs(P[i][1] - P[q[0]][1])**2 >= d0:
        q.popleft()
      for k in q:
        d = min(d, dist2(P[k], P[i]))
      q.append(i)

  return d,y_sorted_point



#点群P内の最近点対の二乗
#Pはx座標で昇順
def closest_pair(P):
  P.sort()
  d,y_sorted_point = closest_pair_sub(P,0,len(P))
  return d

#3点以下の点群の最小包含円
#半径は二乗された値
#3点なら外接円
#0点の場合原点を中心とした半径0の円とする
def circumcenter(P):
  if len(P) == 0:
    ox,oy,r2 = 0,0,0
  elif len(P) == 1:
    ox,oy,r2 = P[0][0],P[0][1],0
  elif len(P) == 2:
    p1,p2 = P
    ax,ay = p1
    bx,by = p2
    ox = (ax+bx) / 2
    oy = (ay+by) / 2
    r2 = dist2(p1, (ox,oy))
  else:
    p1,p2,p3 = P
    v2,v3 = vec(p1,p2), vec(p1,p3)
    if cross_product(v2,v3) == 0:
      if dot_product(v2,v3) < 0:
        p4,p5 = p2,p3
      elif abs2(v2) <= abs2(v3):
        p4,p5 = p1,p3
      else:
        p4,p5 = p1,p2
      ox,oy,r2 = circumcenter([p4,p5])
    else:
      ax,ay = p1
      bx,by = p2
      cx,cy = p3
      sa,sb,sc = abs2(p1), abs2(p2), abs2(p3)
      D = 2*(ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
      ox = (sa*(by-cy) + sb*(cy-ay) + sc*(ay-by)) / D
      oy = (sa*(cx-bx) + sb*(ax-cx) + sc*(bx-ax)) / D
      r2 = dist2(p1, (ox,oy))
  return ox,oy,r2

#点群Pの最小包含円の中心と半径の二乗
#参照順を乱択しており,僅かな確率でTLEする
#期待計算量はO(N)
def minimum_enclosing_circle(P):
  eps = 1e-9
  random.shuffle(P)
  N = len(P)
  if N == 0:
    return 0,0,0
  cx,cy = P[0]
  r2 = 0
  R = [(0,0),(0,0),(0,0)]
  for i in range(1,N):
    p = P[i]
    if dist2(p, (cx, cy)) > r2 + eps:
      R[0] = p
      cx,cy,r2 = circumcenter(R[:1])
      for j in range(i):
        q = P[j]
        if dist2(q, (cx, cy)) > r2 + eps:
          R[1] = q
          cx,cy,r2 = circumcenter(R[:2])
          for k in range(j):
            r = P[k]
            if dist2(r, (cx, cy)) > r2 + eps:
              R[2] = r
              cx,cy,r2 = circumcenter(R)
  return cx,cy,r2

#2円の共通接線の個数
def common_tangent_number(p1,p2):
  x1,y1,r1 = p1
  x2,y2,r2 = p2
  Ra,D,Rb = (r1-r2)**2, dist2((x1, y1), (x2, y2)), (r1+r2)**2
  if Rb < D:
    return 4
  elif D == Rb:
    return 3
  elif Ra < D < Rb:
    return 2
  elif Ra == D:
    return 1
  else:
    return 0

#三点p1p2p3の内心の中心と半径
def incircle(p1,p2,p3):
  a,b,c = dist2(p2,p3), dist2(p3,p1), dist2(p1,p2)
  a,b,c = math.sqrt(a), math.sqrt(b), math.sqrt(c)
  S = abs(area([p1,p2,p3]))
  r = (2*S)/(a+b+c)
  A,B,C = scalar(a/(a+b+c),p1), scalar(b/(a+b+c),p2), scalar(c/(a+b+c),p3)
  cx,cy = plus([A,B,C])
  return cx,cy,r

#円cと直線p1p2の交点
#unique：重複を排除するか否か
def cross_point_cl(p1,p2,c,unique = True):
  cx,cy,r = c
  cp = (cx,cy)
  d = projection(p1,p2,cp)
  a0 = r*r - dist2(cp,d)
  a = math.sqrt(max(0,a0))
  vp = vec(p1,p2)
  v = scalar(a/math.sqrt(abs2(vp)),vp)
  cp1 = plus([d,v])
  cp2 = plus([d,scalar(-1,v)])
  P = sorted([cp1, cp2])
  eps = 1e-12
  if unique and dist2(P[0],P[1]) < eps:
    return [P[0]]
  return P

#円c1と円c2の交点
#unique：重複を排除するか否か
def cross_point_cc(c1,c2,unique = True):
  cx1,cy1,r1 = c1
  cx2,cy2,r2 = c2
  cp1,cp2 = (cx1,cy1),(cx2,cy2)
  D = dist2(cp1,cp2)
  t = (r1*r1 - r2*r2 + D) / (2*D)
  v = vec(cp1,cp2)
  u = (-v[1],v[0])
  p1 = plus([cp1,scalar(t,v)])
  p2 = plus([p1,u])
  return cross_point_cl(p1,p2,c1,unique)

#点pを通る円cの接線の接点
#unique：重複を排除するか否か
def tangent(p,c,unique = True):
  cp = c[:2]
  v = scalar(0.5,(vec(p,cp)))
  cx0,cy0 = plus([p,v])
  r0 = math.sqrt(abs2(v))
  c0 = (cx0,cy0,r0)
  return cross_point_cc(c,c0,unique)

#円c1と円c2の共通接線のc1における接点
#unique：重複を排除するか否か
def common_tangent(c1,c2,unique = True):
  cp1,cp2 = c1[:2],c2[:2]
  r1,r2 = c1[-1],c2[-1]
  v = vec(cp1,cp2)
  u = (-v[1],v[0])
  N = common_tangent_number(c1,c2)
  if N >= 1:
    if r1 != r2:
      p1 = plus([cp1, scalar(r1/(r1-r2), v)])
      P1 = tangent(p1,c1,unique)
    else:
      pa = plus([cp1, scalar(r1/math.sqrt(abs2(u)), u)])
      pb = plus([cp1, scalar(-r1/math.sqrt(abs2(u)), u)])
      P1 = [pa,pb]
  else:
    P1 = []
  if N >= 3:
    p2 = plus([cp1, scalar(r1/(r1+r2), v)])
    P2 = tangent(p2,c1,unique)
  else:
    P2 = []
  return sorted(P1+P2)

#ベクトルp1,p2がなす角(ラジアン)
def theta(p1,p2):
  c =  dot_product(p1,p2) / (math.sqrt(abs2(p1)) * math.sqrt(abs2(p2)))
  c = max(-1,min(1,c))
  the = math.acos(c)
  return the

#三角形Op1p2とOを中心とする半径rの円の共通部分の面積
#符号付き
def common_area_ct(p1,p2,r):
  area = 0
  P = cross_point_cl(p1,p2,(0,0,r))
  Q1 = [(p1[0],p1[1],0),(p2[0],p2[1],0)]
  Q2 = [(i[0],i[1],1) for i in P]
  Q = sorted(Q1+Q2, key = lambda p: dot_product(vec(p1, p2), p[:2]))
  q = len(Q)
  t = 0
  for i in range(q-1):
    q1,q2 = (Q[i][0],Q[i][1]),(Q[i+1][0],Q[i+1][1])
    a,b = Q[i][2],Q[i+1][2]

    if a == 0:
      t += 1
    if t != 1:
      continue

    if a == b == 0:
      if abs2(q1) > r*r:
        c = r*r*theta(q1,q2)/2
      else:
        c = cross_product(q1,q2)/2
    elif a == b == 1:
      c = cross_product(q1,q2)/2
    elif a == 0 and b == 1:
      if abs2(q1) > r*r:
        c = r*r*theta(q1,q2)/2
      else:
        c = cross_product(q1,q2)/2
    else:
      if abs2(q2) > r*r:
        c = r*r*theta(q1,q2)/2
      else:
        c = cross_product(q1,q2)/2
    area += abs(c)

  if cross_product(p1,p2) >= 0:
    return area
  else:
    return -area

#半時計回りに並んだ点列Pがなす多角形と円の共通部分の面積
#凸でなくても良い
def common_area_cp(c,P):
  cp = c[:2]
  r = c[-1]
  N = len(P)
  area = 0
  for i in range(N):
    area += common_area_ct(vec(cp, P[i]), vec(cp, P[(i+1)%N]), r)
  return area

#円c1,c2の共通部分の面積
def common_area_cc(c1,c2):
  N = common_tangent_number(c1,c2)
  cp1,cp2 = c1[:2],c2[:2]
  r1,r2 = c1[-1],c2[-1]
  if N >= 3:
    return 0
  elif N <= 1:
    r = min(r1,r2)
    return r*r*math.pi
  area = 0
  p3,p4 = cross_point_cc(c1,c2,unique = False)
  v12 = vec(cp1,cp2)
  v13,v14,v23,v24 = vec(cp1,p3),vec(cp1,p4),vec(cp2,p3),vec(cp2,p4)
  if cross_product(v12,v13) >= 0:
    p3,p4 = p4,p3
    v13,v14,v23,v24 = v14,v13,v24,v23

  theta1 = math.atan2(cross_product(v13,v14),dot_product(v13,v14))
  if theta1 < 0:
    theta1 += 2*math.pi
  area += r1*r1*theta1/2
  area += cross_product(v14,v13)/2

  theta2 = math.atan2(cross_product(v24,v23),dot_product(v24,v23))
  if theta2 < 0:
    theta2 += 2*math.pi
  area += r2*r2*theta2/2
  area += cross_product(v23,v24)/2

  return area
