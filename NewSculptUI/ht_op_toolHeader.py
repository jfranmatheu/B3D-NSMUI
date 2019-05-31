
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

class NSMUI_OT_toolHeader_multires_subdivide(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_multires_subdivide"
    bl_label = "new_tool_header_tools_for_sculpt_mode"
    bl_description = "New Level of Subdivision for Multires"
    def execute(self, context):
        #bpy.context.object.modifiers["Multires"].name = "Multires"
        #bpy.context.object.modifiers["Multires"].subdivision_type = 'CATMULL_CLARK'
        bpy.ops.object.multires_subdivide(modifier="Multires")
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_1(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_1"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "1 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 1
        elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
            bpy.context.scene.tool_settings.sculpt.detail_percent = 1
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 1
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_2(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_2"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "2 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 2
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 2
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 2
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_4(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_4"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "4 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 4
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 4
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 4
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_6(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_6"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "6 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 6
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 6
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 6
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_8(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_8"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "8 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 8
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 8
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 8
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_10(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_10"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "10 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 10
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 10
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 10
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_12(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_12"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "12 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 12
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 12
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 12
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_16(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_16"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "16 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 16
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 16
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 16
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_20(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_20"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "20 : Detail Size for Dynamic Topology"
    def execute(self, context):
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 20
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 20
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 20
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_any(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_any"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Selected Detail Size for Dynamic Topology"
    value: bpy.props.FloatProperty(name="value", default=5)
    def execute(self, context):
        #mode = "MID"
        n = self.value
        if(n!=0):
            if bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
                bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = n
            elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
                bpy.context.scene.tool_settings.sculpt.detail_percent = n
            else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
                bpy.context.scene.tool_settings.sculpt.detail_size = n
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_low_detail(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_low_detail"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "LOW Detail Size for Dynamic Topology"
    def execute(self, context):
        from . import dyntopoStage
        dyntopoStage = "LOW"
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_mid_detail(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_mid_detail"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "MID Detail Size for Dynamic Topology"
    def execute(self, context):
        from . import dyntopoStage
        dyntopoStage = "MID"
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_high_detail(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_high_detail"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "HIGH Detail Size for Dynamic Topology"
    def execute(self, context):
        from . import dyntopoStage
        dyntopoStage = "HIGH"
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_relative(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_relative"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Relative Detail for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'RELATIVE'
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_constant(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_constant"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Constant Detail for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_brush(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_brush"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Brush Detail for Dynamic Topology"
    def execute(self, context):
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'BRUSH'
        return {'FINISHED'}