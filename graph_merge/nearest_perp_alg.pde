import java.util.*;

/** Returns an array of points that are within a neighborhood of the pen's position
 *  Assume xvals and yvals are in order. And xvals[i] and yvals[i] go together.
 *
 */
 
 float cosine;
 
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
  
  //println(result.size());
  
  return result;
  
}

/**
 * Returns the point from the set points which is the closest to penx, peny
 */

//public PVector nearestPerp(HashSet<PVector> points, float penx, float peny) {
  
//  PVector pen = new PVector(penx, peny);
//  PVector closest = closestPoint(points, pen); //find the point from the set that is the closest
//  PVector secondClosest = secondClosestPoint(points, closest, pen); //find the point from the set that is the second closest
  
//  PVector result = minimize(closest, secondClosest, pen); //find the point between these two points that has the closest distance to 
  
//  return result;
//}

// This is the function that gets the closest perpendicular point. Assumes that the function is legit. //

public PVector closestPerp(String function, PVector pen) {

Expression e = Compile.expression(function, false); // compile the function expression

  
float cur_x = pen.x; // The algorithm starts at pen_x
float gamma = 0.01; // step size multiplier
float precision = 0.00001;
float previous_step_size = 1;
int max_iters = 10000; // maximum number of iterations
int iters = 0; //iteration counter

float df; //local derivative
float prev_x;



while ((previous_step_size > precision) && (iters < max_iters)) {
    df = (dist(pen.x, pen.y, cur_x+precision, e.eval(cur_x+precision).answer().toFloat()) - dist(pen.x, pen.y, cur_x, e.eval(cur_x).answer().toFloat()))/precision; //get the derivative of the distance locally
          
    prev_x = cur_x;
    cur_x -= gamma * df;
    previous_step_size = abs(cur_x - prev_x);
    iters++;
}

//println("The local minimum occurs at", cur_x);

return new PVector(cur_x, e.eval(cur_x).answer().toFloat());
  
}

// Gives repelling force for the haptic guidance. //                                     
public PVector getForce(PVector pen, PVector closestPerp, String curr_fn) { //pen is in graph coordinates, and so is closestPerp

// Constants //
  float k = 1; //constant for the force
  float range = 0.01; // at range units away from the graph, and under, the repulsive force is 0
  float push_const = 5;

  //println("range: ", range);
  float distancek = 30; //distance multiplier
  int power = 1;
  //println("closestPerp: ", closestPerp);
  //println("pen: ", pen);
  float dToWallFromGraph = 10; //how far away the wall is from either side
  float dToWallFromPen = dToWallFromGraph-PVector.dist(pen, closestPerp);
  float cos_threshold = cos(70);

  Expression e = Compile.expression(curr_fn, false); // compile the function expression
  float step = 0.001; //for derivative
  float df = (e.eval(closestPerp.x+step).answer().toFloat() - e.eval(closestPerp.x).answer().toFloat())/step; //derivative at closest perp
  
  //range = abs(df)/40;
  
  PVector tangentVector = new PVector(1, df);
  tangentVector.normalize();
  println("tangentVector: ", tangentVector);
  
  if (penVel_gc.mag() != 0) {
     cosine = abs(PVector.dot(penVel_gc, tangentVector)/penVel_gc.mag());
  }
  println("cosine: ", cosine);
  //println("cos_thres: ", cos_threshold);
  
     if (closestPerp.x > Xfinal) {
       closestPerp.x = pen.x;
     }
  
  if (cosine < cos_threshold && (PVector.dist(pen, closestPerp)) > range) {
 
       
     float magnitude = (float) (Math.pow((PVector.dist(pen, closestPerp))*distancek, power))*k;
  
     PVector dir_normalized = new PVector((closestPerp.x-pen.x)/PVector.dist(pen, closestPerp), (closestPerp.y-pen.y)/PVector.dist(pen, closestPerp));
  
     
  
     float Offset = (float) (Math.pow(range*distancek, power))*k;
  
     PVector force = new PVector((magnitude-Offset)*dir_normalized.x, (magnitude-Offset)*dir_normalized.y);
     println("force (repel): ", force);
     force.add(tangentVector.mult(push_const));
     return force;
  
     
  }
  else { //return new PVector(0, 0);
         PVector push_vector = new PVector(tangentVector.x*push_const, tangentVector.y*push_const);
         if (PVector.dot(penVel_gc, tangentVector) >= 0) { //if the angle is acute
            // don't change the push vector
         }
         else { push_vector.mult(-1); }
         println("force (drive): ", push_vector);
         return push_vector;
  }
  
  
  
}

public PVector getDriveForce(PVector pen, PVector closestPerp, String function) {
  Expression e = Compile.expression(function, false); // compile the function expression
  float step = 0.01; //for derivative computation
  float precision = 100;
  float range = 100;
  int k = 1;
  float lowerBd = 2; // below this magnitude of penVelocity, don't do anything
  
  float df = (e.eval(closestPerp.x+step).answer().toFloat() - e.eval(closestPerp.x).answer().toFloat())/step; //derivative at closest perp
  float penVelocity_slope = penVelocity.y/penVelocity.x;
  
  PVector penTravelDir = new PVector(penVelocity.x/sqrt(penVelocity.x*penVelocity.x+penVelocity.y*penVelocity.y), penVelocity.y/sqrt(penVelocity.x*penVelocity.x+penVelocity.y*penVelocity.y));

  //println("penVelocity: ", penVelocity);
  if (PVector.dist(pen, closestPerp) <= range && abs(df - penVelocity_slope) < precision && penVelocity.mag() > lowerBd) { //if we are within some distance of the graph and the slopes of velocity and df match
  
  //println("match");
  PVector result = new PVector(-penVelocity.x*k, -penVelocity.y*k);
  //println("DriveForce vector: ", result);
  return result;
  
  
    
  }
  else { return new PVector(0, 0); } //no driving force otherwise
  
  
 // return null;
}
