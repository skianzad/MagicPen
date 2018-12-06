%clear all;
close all;
timeLog = importdata('timeLog.txt');
xLog = importdata('xLog.txt');
yLog = importdata('yLog.txt');
%A=A(A>300)-360
endpoint=min([length(timeLog),length(xLog),length(yLog)])
for k=1:length(timeLog)
    if timeLog(k)>=180;
        timeLog(k)=timeLog(k)-360;
    end
end
figure;plot(xLog,-yLog, 'o');
xlim([-1 17])
ylim([-18 0])
set(gcf,'Position',[100 0 800 800])

%figure;plot(D(1,1:endpoint),C(1,1:endpoint));
figure;plot(timeLog-timeLog(1),xLog);
hold on
plot(timeLog,yLog);