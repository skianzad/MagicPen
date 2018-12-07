%clear all;
close all;
A = importdata('Sens.txt');
B = importdata('Time.txt');
C = importdata('X.txt');
D = importdata('Y.txt');
%A=A(A>300)-360
endpoint=min([length(A),length(B),length(C),length(D)])
for k=1:length(A)
    if A(k)>=180;
        A(k)=A(k)-360;
    end
end
figure;plot(B(1,1:endpoint)-B(1),(A(1,1:endpoint)));
hold on ;plot(B(1,1:endpoint)-B(1),C(1,1:endpoint)-C(1));
hold on ;plot(B(1,1:endpoint)-B(1),D(1,1:endpoint)-D(1));
figure;plot(D(1,1:endpoint)-D(1),C(1,1:endpoint)+C(1));

for i=1:endpoint
    A(i)=-35;
    Vsx(i)=(C(i)-C(1))*cos(-A(i)*pi/180)-sin(-A(i)*pi/180)*(D(i)-D(1));
    Vsy(i)=(C(i)-C(1))*sin(-A(i)*pi/180)+cos(-A(i)*pi/180)*(D(i)-D(1));
end
%figure;plot(-Vsx,-Vsy);