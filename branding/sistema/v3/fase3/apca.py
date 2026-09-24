def Y(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    y=0.2126729*r**2.4+0.7151522*g**2.4+0.0721750*b**2.4
    return y+(0.022-y)**1.414 if y<0.022 else y
def lc(txt,bg):
    yt,yb=Y(txt),Y(bg)
    if abs(yb-yt)<0.0005: return 0.0
    if yb>yt:
        s=(yb**0.56-yt**0.57)*1.14; o=0 if s<0.1 else s-0.027
    else:
        s=(yb**0.65-yt**0.62)*1.14; o=0 if s>-0.1 else s+0.027
    return round(o*100,1)
def wcag(a,b):
    def L(h):
        h=h.lstrip('#'); c=[int(h[i:i+2],16)/255 for i in (0,2,4)]
        c=[x/12.92 if x<=0.04045 else ((x+0.055)/1.055)**2.4 for x in c]
        return 0.2126*c[0]+0.7152*c[1]+0.0722*c[2]
    l1,l2=sorted([L(a),L(b)],reverse=True); return round((l1+0.05)/(l2+0.05),2)
if __name__=='__main__':
    for t in ['#EFFCF7','#BECBC6','#86A799','#00EAA5','#517064']: print(t, lc(t,'#011F16'), wcag(t,'#011F16'))
