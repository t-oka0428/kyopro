#https://github.com/t-oka0428/kyopro/blob/main/trie_and_ahocorasick.py

import collections

#X:文字列集合(数字に直してね),n:文字集合のサイズ
#G,parent,acceptの順にreturn
#G[i][s]は頂点iから文字sを読むとどこに行くか(なければ-1)
def trie(X,n):
  x = len(X)
  G = [[-1 for _ in range(n)]]
  parent = [-1]
  accept = [False]
  for S in X:
    now = 0
    for s in S:
      if G[now][s] == -1:
        G[now][s] = len(G)
        G.append([-1 for _ in range(n)])
        parent.append(now)
        accept.append(False)
      now = G[now][s]
    accept[now] = True
  return G,parent,accept

#trie木をaho_corasick遷移グラフに改造
def aho_corasick(G,parent,n):
  N = len(parent)
  failure = [-1 for _ in range(N)]
  failure[0] = 0
  q = collections.deque()
  for c in range(n):
    v = G[0][c]
    if v == -1:
      G[0][c] = 0
    else:
      failure[v] = 0
      q.append(v)
  while q:
    now = q.popleft()
    for c in range(n):
      v = G[now][c]
      if v == -1:
        G[now][c] = G[failure[now]][c]
      else:
        failure[v] = G[failure[now]][c]
        q.append(v)

  return G,failure
