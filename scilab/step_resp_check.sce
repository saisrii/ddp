A=diag(ones(10,1)*-22,0)+diag(ones(9,1)*11,1)+diag(ones(9,1)*11,-1)
A(10,10)=-11
B=zeros(10,1)
B(1,1)=1
C=zeros(1,10)
C(1,10)=1
D=zeros(1)
sys=syslin('c',A,B,C,D)
t=0:0.01:4;
u=ones(1:length(t));
[y,x]=csim(u,t,sys);
plot2d(t,y)