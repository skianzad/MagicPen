import org.quark.jasmine.*;

public class Function {
  
    float x; // x-coordinate
    
    public Function(float x) {
      this.x = x;
    }
    
    public float computeY(String s) {
      
     // String expr = "sqrt(x)";
      Expression e = Compile.expression(s, false);
      //System.out.println(e.eval(x).answer().toFloat());
      return e.eval(x).answer().toFloat();
      
      //if (s.equals("x^3")) {
      //  return x*x*x;
      //}
    //  else return 0.0f;
      
    }
  
}
