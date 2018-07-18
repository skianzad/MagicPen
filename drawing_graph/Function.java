import org.quark.jasmine.*;

public class Function {
  
    float x; // x-coordinate
    
    public Function(float x) {
      this.x = x;
    }
    
    // Checks if s is a valid expression: if the expression is only in terms of x.
    
    public static boolean valid(String s) {
      System.out.println("valid called");
      if (!s.equals("")) { //if not the empty string
        Expression e = Compile.expression(s, false);
        if (e != null) {
           System.out.println("expression not null");
           try {
             e.eval(5).answer().toFloat_();
           }
           catch (JasmineException ex) {
             
             return false;}
           return true;
        }
        System.out.println("e is null");
        return false;
      }
      else { return false; }
    }
    
    
    /**
     * Requires a check of valid for s before being called. Gets the y coordinate, given the expression and this.x
     * @param s, the mathematical expression in terms of x
     * @return   result of s applied to this.x
     */
     
    public float computeY(String s) {
      
     // String expr = "sqrt(x)";
  //    if (!s.equals("")) {
      Expression e = Compile.expression(s, false);
      //System.out.println(e.eval(x).answer().toFloat());
 //       if (e != null) {
           return e.eval(x).answer().toFloat();
  //      }
   //     else return 0.0f;
    //  }
      
      //if (s.equals("x^3")) {
      //  return x*x*x;
      //}
      //else return 0.0f;
      
    }
  
}
