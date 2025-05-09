import maya.cmds as mc
import maya.mel as mel
from maya.OpenMaya import MVector

class SpineRigger:
    def __init__(self, spine_joints, controller_size=5, color=(0, 0, 0)):
        self.spine_joints = spine_joints 
        self.controller_size = controller_size
        self.color = color 
        self.controllers = []

    def create_fk_controller(self, jnt_name):
        ctrl_name = f"ac_fk_{jnt_name}"
        ctrl_grp = f"{ctrl_name}_grp"

        # Create controller
        mc.circle(n=ctrl_name, r=self.controller_size, nr=(1, 0, 0))
        mc.group(ctrl_name, n=ctrl_grp)

        #mitch match joint pos
        mc.matchTransform(ctrl_grp, jnt_name)

        #constraints
        mc.orientConstraint(ctrl_name, jnt_name)

        #color control
        r, g, b = self.color
        mc.setAttr(f"{ctrl_name}.overrideEnabled", 1)
        mc.setAttr(f"{ctrl_name}.overrideRGBColors", 1)
        mc.setAttr(f"{ctrl_name}.overrideColorRGB", r, g, b, type="double3")

        return ctrl_name, ctrl_grp

    def rig_fk_spine(self):
        if len(self.spine_joints) < 3:
            mc.error("Spine rig needs at least 3 joints.")

        parent_ctrl = None
        for jnt in self.spine_joints:
            ctrl, grp = self.create_fk_controller(jnt)
            self.controllers.append((ctrl, grp))

            # Parent controllers hierarchically
            if parent_ctrl:
                mc.parent(grp, parent_ctrl)

            parent_ctrl = ctrl

        # Group all controllers
        top_group = "spine_fk_ctrls_grp"
        grp_list = [grp for ctrl, grp in self.controllers]
        if mc.objExists(top_group):
            mc.delete(top_group)
        mc.group(grp_list, n=top_group)

        print("FK Spine rig made!")

    def rig(self):
        self.rig_fk_spine()
