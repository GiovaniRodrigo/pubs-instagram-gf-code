import numpy as np, wave
sr=44100; dur=33.0; n=int(sr*dur); t=np.arange(n)/sr
out=np.zeros(n)
def note(m): return 440*2**((m-69)/12)
chords=[[57,60,64],[53,57,60],[48,52,55],[55,59,62]]  # Am F C G
bar=2.4
for k in range(int(dur/bar)+1):
    s=int(k*bar*sr); e=min(n,int((k+1)*bar*sr)+sr//4)
    if s>=n: break
    tt=t[s:e]-t[s]; env=np.minimum(1,tt/0.4)*np.exp(-tt*0.35)
    for m in chords[k%4]+[chords[k%4][0]-12]:
        f=note(m); out[s:e]+=0.05*env*(np.sin(2*np.pi*f*tt)+0.4*np.sin(2*np.pi*f*1.003*tt)+0.15*np.sin(4*np.pi*f*tt))
beat=0.6
for k in range(int(dur/beat)):
    T=k*beat
    if T<3.4: continue
    s=int(T*sr); e=min(n,s+int(0.35*sr)); tt=t[s:e]-T
    f=55+90*np.exp(-tt*30); out[s:e]+=0.35*np.sin(2*np.pi*np.cumsum(f)/sr)*np.exp(-tt*9)
    h=int((T+beat/2)*sr); he=min(n,h+int(0.06*sr))
    if h<n: out[h:he]+=0.04*np.random.randn(he-h)*np.exp(-np.arange(he-h)/sr*60)
for T in [3.4,7.6,10.8,17.2,22.2,27.4]:  # whooshes
    s=int((T-0.35)*sr); e=int((T+0.15)*sr); L=e-s
    nz=np.random.randn(L); nz=np.convolve(nz,np.ones(20)/20,'same')
    out[s:e]+=0.25*nz*np.sin(np.linspace(0,np.pi,L))**2
fade=np.ones(n); fl=int(2.5*sr); fade[-fl:]=np.linspace(1,0,fl); out*=fade
out/=np.abs(out).max()*1.25
d=(out*32767).astype(np.int16); st=np.stack([d,d],1)
w=wave.open('music_mei.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(st.tobytes()); w.close()
