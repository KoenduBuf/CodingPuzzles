

# okay, just let me explain why this is garbage:
# - heavy bs assumption 1; any elevator is good to take
# - heavy bs assumption 2; there is max 1 elevator per floor
# - (V1) look at 't' it means:  t=-1 if ld=="LEFT" else 1
# - (V2) from now on the exit is just another elevator
# - (V3) the exit elivator has more values, because why cut it off
# - (V4) Just removing some variables to make it unreadable
# - (V5) Abusing math garbage to the fullest

####################### V1
# n=int
# w=["WAIT","BLOCK"]
# def o(i):print(w[i])
# l=lambda:[n(x) for x in input().split()]
# _,_,_,F,P,_,_,e=l()
# e=[l() for _ in range(e)]
# while 1:
#  f,p,d=input().split()
#  t=n(d[0],32)/3-8
#  c=n(p)*t
#  d=len([x for x in e if x[0]==n(f) and x[1]*t<c])
#  o(P*t<c) if F==n(f) else o(d)

######################## V2
# n=int
# w=["WAIT","BLOCK"]
# l=lambda:[n(x) for x in input().split()]
# x=l();e=[l() for _ in range(x[7])]+[x[3:5]]
# while 1:
#  f,p,d=input().split()
#  t=n(d[0],32)/3-8
#  c=n(p)*t
#  d=len([x for x in e if x[0]==n(f) and x[1]*t<c])
#  print(w[d])

######################## V3
# n=int
# l=lambda:[n(x) for x in input().split()]
# x=l();e=[l() for _ in range(x[7])]+[x[3:]]
# while 1:
#  f,p,d=input().split()
#  t=n(d[0],32)/3-8
#  d=len([x for x in e if x[0]==n(f) and x[1]*t<n(p)*t])
#  print(["WAIT","BLOCK"][d])

######################## V4
# n=int;l=lambda:[*map(n,input().split())]
# x=l();e=[l() for _ in range(x[7])]+[x[3:]]
# while 1:
#  f,p,d=input().split();t=n(d[0],32)/3-8
#  print(["WAIT","BLOCK"][sum(x[0]==n(f) and x[1]*t<n(p)*t for x in e)])

####################### V5 (199 chars!!!)
n=int;l=lambda:[*map(n,input().split())]
x=l();e=[l() for _ in range(x[7])]+[x[3:]]
while 1:f,p,d=input().split();print(["WAIT","BLOCK"]
[sum((x[0]==n(f))*(n(p)-x[1])*(n(d[0],32)/3-8)>0 for x in e)])
