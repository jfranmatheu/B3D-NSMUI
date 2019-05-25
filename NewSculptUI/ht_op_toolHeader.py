
import bpy
from bpy import context, types
from bpy.types import (
    Brush,
    FreestyleLineStyle,
    ParticleSettings,
    Texture
)

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

class NSMUI_OT_toolHeader_dyntopo_1(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_1"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "1 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 1
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_2(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_2"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "2 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 2
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_4(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_4"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "4 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 4
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_6(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_6"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "6 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 6
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_8(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_8"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "8 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 8
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_10(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_10"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "10 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 10
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_12(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_12"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "12 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 12
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_16(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_16"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "16 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 16
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_20(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_20"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "20 : Detail Size for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_size = 20
        return {'FINISHED'}