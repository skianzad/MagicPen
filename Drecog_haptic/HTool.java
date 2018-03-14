//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//
import fisica.*;
//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

import org.jbox2d.collision.shapes.CircleDef;
import org.jbox2d.collision.shapes.ShapeDef;
import processing.core.PGraphics;

public class HTool extends FBody {
    protected float m_size;

    protected ShapeDef getShapeDef() {
        CircleDef pd = new CircleDef();
        pd.radius = this.m_size / 2.0F;
        pd.density = this.m_density;
        pd.friction = this.m_friction;
        pd.restitution = this.m_restitution;
        pd.isSensor = this.m_sensor;
        return pd;
    }

    protected ShapeDef getTransformedShapeDef() {
        CircleDef pd = (CircleDef)this.getShapeDef();
        pd.localPosition.set(this.m_position);
        return pd;
    }

    public HTool(float size) {
        this.m_size = size;
        this.setSensor(true);
        this.setAllowSleeping(false);
        //this.m_gravityScale = 0.0F;
        this.setFillColor(10);
        this.setStrokeColor(0);
        this.setDrawable(false);
    }

    public float getSize() {
        return this.m_size;
    }

    public void setSize(float size) {
        this.m_size = size;
        this.recreateInWorld();
    }

    public void draw(PGraphics applet) {
        this.preDraw(applet);
        if (this.m_image != null) {
            this.drawImage(applet);
        } else {
            //applet.ellipse(0.0F, 0.0F, hAPI_Fisica.worldToScreen(this.getSize()), hAPI_Fisica.worldToScreen(this.getSize()));
        }

        this.postDraw(applet);
    }

    public void drawDebug(PGraphics applet) {
        this.preDrawDebug(applet);
        //applet.ellipse(0.0F, 0.0F, hAPI_Fisica.worldToScreen(this.getSize()), hAPI_Fisica.worldToScreen(this.getSize()));
       // applet.line(0.0F, 0.0F, hAPI_Fisica.worldToScreen(this.getSize() / 2.0F), hAPI_Fisica.worldToScreen(0.0F));
        this.postDrawDebug(applet);
    }
}