import math
pi=math.pi
def PointsInCircum(r,n,phi):
    return [(math.cos(2*pi/n*x+phi)*r,math.sin(2*pi/n*x+phi)*r) for x in range(0,n+1)]
# math.atan2(point-center)
point= [10,10]
center= [1,1]
print(center[1])
distance=[(point[0]-center[0]),(point[1]-center[1])]
phi=math.atan2(distance[1],distance[1])
print(180*phi/pi)
r=math.sqrt(distance[0]*distance[0]+distance[1]*distance[1])
points=PointsInCircum(r,100,phi)
print(len(points))
for x in points:
    print(round(x[0]+center[0],3),round(x[1]/1.00+center[1],3))
# print(math.cos(60))/