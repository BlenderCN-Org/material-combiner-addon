import bpy
from bpy.props import *
from ... utils . objects import get_obs
from ... utils . materials import get_materials


class RefreshObData(bpy.types.Operator):
    bl_idname = 'smc.refresh_ob_data'
    bl_label = 'Combine List Items'
    bl_description = 'Refresh Items'

    def execute(self, context):
        scn = context.scene
        ob_list = get_obs(scn.objects)
        scn.smc_ob_data.clear()
        for ob_id, ob in enumerate(ob_list):
            mat_list = get_materials(ob)
            item = scn.smc_ob_data.add()
            item.ob = ob
            item.ob_id = ob_id
            item.type = 0
            for mat in mat_list:
                item = scn.smc_ob_data.add()
                item.ob = ob
                item.ob_id = ob_id
                item.mat = mat
                item.type = 1
            item = scn.smc_ob_data.add()
            item.type = 2
        return {'FINISHED'}


class CombineItemMat(bpy.types.Operator):
    bl_idname = 'smc.combine_switch'
    bl_label = 'Add Item'
    bl_description = 'Select / Deselect'

    list_id = IntProperty(default=0)

    def execute(self, context):
        scn = context.scene
        items = scn.smc_ob_data
        item = items[self.list_id]
        if item.type:
            ob_item = next((ob for ob in items if (ob.ob_id == item.ob_id) and not ob.type), None)
            if ob_item:
                if item.used:
                    item.used = False
                else:
                    ob_item.used = True
                    item.used = True
        else:
            ob_item_list = [mat for mat in items if (mat.ob_id == item.ob_id) and mat.type]
            if ob_item_list:
                if item.used:
                    for ob_item in ob_item_list:
                        ob_item.used = False
                    item.used = False
                else:
                    for ob_item in ob_item_list:
                        ob_item.used = True
                    item.used = True
        return {'FINISHED'}


class CombineMenuType(bpy.types.Operator):
    bl_idname = 'smc.combine_menu_type'
    bl_label = 'Combine Menu State'
    bl_description = 'Menu Window'

    def execute(self, context):
        scn = context.scene
        if scn.smc_combine_state:
            bpy.ops.smc.refresh_ob_data()
            scn.smc_combine_state = False
        else:
            scn.smc_combine_state = True
        return {'FINISHED'}