//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by Fernflower decompiler)
//

import java.util.ArrayList;
import org.jbox2d.common.Vec2;
import processing.core.PApplet;

public class HVirtualCoupling {
    protected float m_size = 0.5F;
    protected HTool h_tool;
    protected FBox h_avatar;
    protected Vec2 vc_force = new Vec2(0.0F, 0.0F);
    protected Vec2 tool_position = new Vec2(0.0F, 0.0F);
    protected Vec2 tool_velocity = new Vec2(0.0F, 0.0F);
    protected Vec2 avatar_position = new Vec2(0.0F, 0.0F);
    protected Vec2 avatar_velocity = new Vec2(0.0F, 0.0F);
    protected ArrayList<FContact> avatarContact;
    protected float vc_stiffness = 250000.0F;
    protected float vc_damping = 700.0F;
    protected float vc_free_mass = 0.00525F;
    protected float vc_contact_mass = 1.10F;

    public HVirtualCoupling(float size) {
        this.h_tool = new HTool(size);
        this.h_avatar = new FBox(size-size/2,size);
        this.h_avatar.setAngularDamping(10.0F);
        this.h_avatar.setGrabbable(false);
        this.h_avatar.setRotatable(false);
        this.avatarContact = new ArrayList();
    }

    public float getSize() {
        return this.m_size;
    }

    public void setSize(float size) {
        this.m_size = size;
        this.h_tool.recreateInWorld();
        this.h_avatar.recreateInWorld();
    }

    public void setPosition(float x, float y) {
        this.h_avatar.setPosition(x, y);
    }

    public void init(FWorld world, float x, float y) {
        this.setAvatarPosition(x, y);
        this.setAvatarVelocity(0.0F, 0.0F);
        this.setToolPosition(x, y);
        world.add(this.h_avatar);
        world.add(this.h_tool);
    }

    public void setToolPosition(float x, float y) {
        this.h_tool.setPosition(x, y);
        this.tool_position = new Vec2(x, y);
        this.h_tool.setVelocity(0.0F, 0.0F);
    }

    public void setToolVelocity(float x, float y) {
        this.tool_velocity = new Vec2(x, y);
        this.h_tool.setVelocity(0.0F, 0.0F);
    }

    public void setAvatarPosition(float x, float y) {
        this.h_avatar.setPosition(x, y);
        this.avatar_position = new Vec2(x, y);
    }

    public void setAvatarVelocity(float vx, float vy) {
        this.avatar_velocity = new Vec2(vx, vy);
        this.h_avatar.setVelocity(vx, vy);
    }

    public float getToolPositionX() {
        return this.h_tool.getX();
    }

    public float getToolPositionY() {
        return this.h_tool.getY();
    }

    public float getToolVelocityX() {
        return this.tool_velocity.x;
    }

    public float getToolVelocityY() {
        return this.tool_velocity.y;
    }

    public float getAvatarPositionX() {
        return this.h_avatar.getX();
    }

    public float getAvatarPositionY() {
        return this.h_avatar.getY();
    }

    public float getAvatarVelocityX() {
        return this.h_avatar.getVelocityX();
    }

    public float getAvatarVelocityY() {
        return this.h_avatar.getVelocityY();
    }

    public void updateCouplingForce() {
        this.updateCouplingForce(this.vc_free_mass, this.vc_stiffness, this.vc_damping, this.vc_contact_mass);
    }

    public void updateCouplingForce(float mass, float stiffness, float damping) {
        this.updateCouplingForce(mass, stiffness, damping, this.vc_contact_mass);
    }

    public void updateCouplingForce(float free_mass, float stiffness, float damping, float contact_mass) {
        this.avatarContact = this.h_tool.getContacts();
        damping /= 20.0F;
        stiffness /= 20.0F;
        float density;
        if ((this.avatarContact.size() != 1 || ((FContact)this.avatarContact.get(0)).getBody2() != this.h_avatar && ((FContact)this.avatarContact.get(0)).getBody1() != this.h_avatar) && this.avatarContact.size() != 0) {
            density = contact_mass * 4.0F / (3.14F * this.m_size * this.m_size);
            this.h_avatar.setDensity(density);
            this.h_tool.setDensity(0.25F);
        } else {
            density = free_mass * 4.0F / (3.14F * this.m_size * this.m_size);
            this.h_avatar.setDensity(density);
            this.h_tool.setDensity(density);
        }

        this.setToolVelocity(0.0F, 0.0F);
        this.vc_force.set(stiffness * (this.getAvatarPositionX() - this.getToolPositionX()) + damping * (this.getAvatarVelocityX() - this.getToolVelocityX()), stiffness * (this.getAvatarPositionY() - this.getToolPositionY()) + damping * (this.getAvatarVelocityY() - this.getToolVelocityY()));
        this.h_avatar.addForce(-this.vc_force.x, -this.vc_force.y);
    }

    public float getVCforceX() {
        return this.vc_force.x;
    }

    public float getVCforceY() {
        return this.vc_force.y;
    }

    public float getVirtualCouplingForceX() {
        return this.vc_force.x;
    }

    public float getVirtualCouplingForceY() {
        return this.vc_force.y;
    }

    public void setVirtualCouplingStiffness(float stiffness) {
        this.vc_stiffness = stiffness;
    }

    public void setVirtualCouplingDamping(float damping) {
        this.vc_damping = damping;
    }

    public float getVirtualCouplingStiffness() {
        return this.vc_stiffness;
    }

    public float getVirtualCouplingDamping() {
        return this.vc_damping;
    }

    void drawContactVectors(PApplet applet) {
        ArrayList<FContact> c_draw = this.h_avatar.getContacts();

        for(int i = 0; i < c_draw.size(); ++i) {
            if (((FContact)c_draw.get(i)).getBody1() != this.h_tool && ((FContact)c_draw.get(i)).getBody2() != this.h_tool) {
                applet.pushMatrix();
                applet.translate(hAPI_Fisica.worldToScreen(((FContact)c_draw.get(i)).getX()), hAPI_Fisica.worldToScreen(((FContact)c_draw.get(i)).getY()));
                applet.line(0.0F, 0.0F, hAPI_Fisica.worldToScreen(((FContact)c_draw.get(i)).getNormalX()), hAPI_Fisica.worldToScreen(((FContact)c_draw.get(i)).getNormalY()));
                applet.translate(hAPI_Fisica.worldToScreen(((FContact)c_draw.get(i)).getNormalX()), hAPI_Fisica.worldToScreen(((FContact)c_draw.get(i)).getNormalY()));
                applet.rotate((float)Math.atan2((double)((FContact)c_draw.get(i)).getNormalY(), (double)((FContact)c_draw.get(i)).getNormalX()));
                applet.pushMatrix();
                applet.rotate(0.3F);
                applet.line(0.0F, 0.0F, -10.0F, 0.0F);
                applet.popMatrix();
                applet.pushMatrix();
                applet.rotate(-0.3F);
                applet.line(0.0F, 0.0F, -10.0F, 0.0F);
                applet.popMatrix();
                applet.popMatrix();
            }
        }

    }
}