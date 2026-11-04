"""Motor de color: sRGB<->OKLCh, WCAG 2.2, APCA (0.1.9) y generacion por contraste
   (el algoritmo de Adobe Leonardo: dado un objetivo de contraste, resolver el color)."""
import numpy as np

M1 = np.array([[0.8189330101,0.3618667424,-0.1288597137],
               [0.0329845436,0.9293118715, 0.0361456387],
               [0.0482003018,0.2643662691, 0.6338517070]])
M2 = np.array([[0.2104542553, 0.7936177850,-0.0040720468],
               [1.9779984951,-2.4285922050, 0.4505937099],
               [0.0259040371, 0.7827717662,-0.8086757660]])
XYZ_RGB = np.array([[ 3.2409699419,-1.5373831776,-0.4986107603],
                    [-0.9692436363, 1.8759675015, 0.0415550574],
                    [ 0.0556300797,-0.2039769589, 1.0569715142]])
RGB_XYZ = np.linalg.inv(XYZ_RGB)

def lin(c): return np.where(c<=0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
def gam(c): return np.where(c<=0.0031308, c*12.92, 1.055*np.abs(c)**(1/2.4)-0.055)

def srgb_to_oklab(rgb):
    x = RGB_XYZ @ lin(np.asarray(rgb,float))
    l = np.cbrt(M1 @ x)
    return M2 @ l
def oklab_to_srgb(lab):
    l = np.linalg.inv(M2) @ np.asarray(lab,float)
    x = np.linalg.inv(M1) @ (l**3)
    return gam(XYZ_RGB @ x)
def oklch_to_rgb(L,C,H):
    h=np.radians(H)
    return oklab_to_srgb([L, C*np.cos(h), C*np.sin(h)])
def in_gamut(rgb, eps=1e-4): return bool(np.all(rgb>-eps) and np.all(rgb<1+eps))

def clip_chroma(L,C,H):
    """reduce C hasta que entre en sRGB (gamut mapping por busqueda binaria)"""
    lo,hi=0.0,C
    if in_gamut(oklch_to_rgb(L,C,H)): return C
    for _ in range(40):
        mid=(lo+hi)/2
        if in_gamut(oklch_to_rgb(L,mid,H)): lo=mid
        else: hi=mid
    return lo

def hexof(rgb):
    v=np.clip(np.asarray(rgb),0,1)
    return '#%02X%02X%02X'%tuple(np.round(v*255).astype(int))
def unhex(h):
    h=h.lstrip('#'); return np.array([int(h[i:i+2],16)/255 for i in (0,2,4)])

def rel_lum(rgb):
    r,g,b = lin(np.asarray(rgb,float))
    return 0.2126*r+0.7152*g+0.0722*b
def wcag(a,b):
    la,lb = rel_lum(a), rel_lum(b)
    hi,lo = max(la,lb), min(la,lb)
    return (hi+0.05)/(lo+0.05)

def _apca_y(rgb):
    r,g,b = np.clip(np.asarray(rgb,float),0,1)
    Y = 0.2126729*r**2.4 + 0.7151522*g**2.4 + 0.0721750*b**2.4
    return Y + (0.022-Y)**1.414 if Y < 0.022 else Y
def apca(text,bg):
    Yt,Yb=_apca_y(text),_apca_y(bg)
    if Yb>Yt:
        S=(Yb**0.56 - Yt**0.57)*1.14
        return 0.0 if S<0.1 else (S-0.027)*100
    S=(Yb**0.65 - Yt**0.62)*1.14
    return 0.0 if S>-0.1 else (S+0.027)*100

def solve_contrast(target, bg, H, Cmax, lighter=True):
    """Leonardo: mueve L en OKLCh hasta alcanzar el contraste WCAG objetivo."""
    lo,hi = (0.0,1.0)
    best=None
    for _ in range(60):
        L=(lo+hi)/2
        C=clip_chroma(L,Cmax,H)
        rgb=np.clip(oklch_to_rgb(L,C,H),0,1)
        c=wcag(rgb,bg)
        best=(L,C,rgb,c)
        if (c<target) == lighter: lo=L
        else: hi=L
    return best
