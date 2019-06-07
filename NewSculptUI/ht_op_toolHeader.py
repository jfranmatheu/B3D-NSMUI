
import bpy
from bpy import context, types
from bpy.types import (
    Brush,
    FreestyleLineStyle,
    ParticleSettings,
    Texture
)

class NSMUI_OT_toolHeader_brushRemove(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_brush_remove"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Remove Active Brush plus Unlink"
    def execute(self, context):
        brush = bpy.context.tool_settings.sculpt.brush
        bpy.data.brushes.remove(brush, do_unlink=True)
        return {'FINISHED'}

class NSMUI_OT_toolHeader_symmetry_all(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_symmetry_all"
    bl_label = "new_tool_header_tools_for_sculpt_mode"
    bl_description = "Activate/Deactivate Symmetry"

    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.use_symmetry_x == True 
        or bpy.context.scene.tool_settings.sculpt.use_symmetry_y == True
        or bpy.context.scene.tool_settings.sculpt.use_symmetry_z == True):
        
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = False
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = False
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = False
        
        else:
            bpy.context.scene.tool_settings.sculpt.use_symmetry_x = True
            bpy.context.scene.tool_settings.sculpt.use_symmetry_y = True
            bpy.context.scene.tool_settings.sculpt.use_symmetry_z = True
        return {'FINISHED'}

class NSMUI_OT_toolHeader_newTexture(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_new_texture"
    bl_label = "New Texture"
    bl_description = "Create a new texture"
    def execute(self, context):
        #imgTexture = bpy.types.ImageTexture
        imgTexture = bpy.ops.texture.new()
        #bpy.data.brushes[context.brush].texture = bpy.data.textures[]

        return {'FINISHED'}

class NSMUI_OT_toolHeader_multires_subdivide(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_multires_subdivide"
    bl_label = "new_tool_header_tools_for_sculpt_mode"
    bl_description = "New Level of Subdivision for Multires"
    def execute(self, context):
        #bpy.context.object.modifiers["Multires"].name = "Multires"
        #bpy.context.object.modifiers["Multires"].subdivision_type = 'CATMULL_CLARK'
        bpy.ops.object.multires_subdivide(modifier="Multires")
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_1(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_1"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Lvl 1 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 125
        elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
            bpy.context.scene.tool_settings.sculpt.detail_percent = 5
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 1
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_2(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_2"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Lvl 2 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 100
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 10
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 2
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_3(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_3"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Lvl 3 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 80
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 16
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 4
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_4(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_4"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Lvl 4 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 65
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 24
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 6
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_5(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_5"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Lvl 5 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 50
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 32
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 9
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_6(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_6"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Lvl 6 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 35
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 48
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 12
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_any(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_any"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Selected Detail Size for Dynamic Topology"
    value: bpy.props.IntProperty(name="value", default=5)
    def execute(self, value):
        n = self.value
        if(n!=0):
            if bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
                bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = n
            elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
                bpy.context.scene.tool_settings.sculpt.detail_percent = n
            else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
                bpy.context.scene.tool_settings.sculpt.detail_size = n
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_any_l(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_any_l"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Low Value for Dyntopo Detail Size"
    value: bpy.props.IntProperty(name="value", default=5)
    def execute(self, value):
        n = self.value
        bpy.types.Scene.depressL = True
        bpy.types.Scene.depressM = False
        bpy.types.Scene.depressH = False
        NSMUI_OT_toolHeader_dyntopo_any.execute(self, self.value)
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_any_m(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_any_m"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Medium Value for Dyntopo Detail Size"
    value: bpy.props.IntProperty(name="value", default=5)
    def execute(self, value):
        n = self.value
        bpy.types.Scene.depressL = False
        bpy.types.Scene.depressM = True
        bpy.types.Scene.depressH = False
        NSMUI_OT_toolHeader_dyntopo_any.execute(self, self.value)
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_any_h(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_any_h"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "High Value for Dyntopo Detail Size"
    value: bpy.props.IntProperty(name="value", default=5)
    def execute(self, value):
        n = self.value
        bpy.types.Scene.depressL = False
        bpy.types.Scene.depressM = False
        bpy.types.Scene.depressH = True
        NSMUI_OT_toolHeader_dyntopo_any.execute(self, self.value)
        return {'FINISHED'}