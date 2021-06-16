def reverse(num):
    rnum = 0
    while(num!=0):
        r=num%10
        rnum = rnum*10+r
        num//=10
    return rnum

ans = reverse(123)
print(ans)
ans = reverse(-1)
print(ans)