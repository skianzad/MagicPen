import java.util.*;

/** Returns an array of points that are within a neighborhood of the pen's position
 *  Assume xvals and yvals are in order. And xvals[i] and yvals[i] go together.
 *
 */
public HashSet<PVector> relevantPoints(float[] xvals, float[] yvals, float pen_x, float pen_y) {
  
  HashSet<PVector> result = new HashSet();
  
  PVector pen = new PVector(pen_x, pen_y);
  
  int steps_to_pen = floor(pen_x/xSpace); // number of steps (from 0) of length xSpace to get to just before pen_x
  int steps_to_0 = floor(xvals[0]/xSpace); //number of steps from 0 to get to the xval[0]
  
  int index_low = steps_to_pen - steps_to_0; //index of x-coord that is immediately before and after pen position
  int index_high = index_low + 1; 
  
  PVector before = new PVector(xvals[index_low], yvals[index_low]); //the point that comes before pen_x
  PVector after = new PVector(xvals[index_high], yvals[index_high]); //the point that comes after pen_x
  
  float radius = max(PVector.dist(pen, before), PVector.dist(pen, after)); //the radius of search
  
  int radius_in_steps = ceil(radius/xSpace); //the radius in steps
  
  for (int i = min(1, steps_to_pen - radius_in_steps); i < steps_to_pen + radius_in_steps; i++) { //looping through indices that fall within the radius;
      PVector temp1 = new PVector(xvals[i], yvals[i]); 
      PVector temp2 = new PVector(xvals[i-1], yvals[i-1]); // add each point, and its neighbors. Since this is a set, duplicates will not occur
      PVector temp3 = new PVector(xvals[i+1], yvals[i+1]);
      result.add(temp1);
      result.add(temp2);
      result.add(temp3);
  }
  
  println(result.size());
  
  return result;
  
}

/**
 * Returns the point from the set points which is the closest to penx, peny
 */

public PVector nearestPerp(HashSet<PVector> points, float penx, float peny) {
  
  PVector pen = new PVector(penx, peny);
  PVector closest = closestPoint(points, pen); //find the point from the set that is the closest
  PVector secondClosest = secondClosestPoint(points, closest, pen); //find the point from the set that is the second closest
  
  PVector result = minimize(closest, secondClosest, pen); //find the point between these two points that has the closest distance to 
  
  return result;
}

public PVector closestPoint(HashSet<PVector> points, PVector pen) {
  PVector temp;
  float dist;
  
  for (PVector v : points) {
   // if (dist(v, pen)) < dist) {
      
   // }
  }
  return null;
  
}

public PVector secondClosestPoint(HashSet<PVector> points, PVector closest, PVector pen) {
  
  return null;
}

public PVector minimize(PVector closest, PVector secondClosest, PVector pen) {
  
  return null;
}
