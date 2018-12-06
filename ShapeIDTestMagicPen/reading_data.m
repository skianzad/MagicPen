clear all;
close all;
timeLog = importdata('timeLog.txt'); %import the data
xLog = importdata('xLog.txt');
yLog = importdata('yLog.txt');

endpoint=min([length(timeLog),length(xLog),length(yLog)]) %not sure what this does
for k=1:length(timeLog)
    if timeLog(k)>=180;
        timeLog(k)=timeLog(k)-360;
    end
end

% replace with an image of your choice
img = imread('bump.jpg');

figure;
plot(xLog.*40,yLog.*40, 'o');
%xlim([-1 17.5])
%ylim([-19 0])

hold on
imshow(img);
alpha(0.3);

% set(gcf,'Position',[100 0 900 800])

%figure;plot(D(1,1:endpoint),C(1,1:endpoint));
% figure;plot(timeLog-timeLog(1),xLog);
% hold on
% plot(timeLog,yLog);