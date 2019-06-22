
import bpy
from bpy import context, types
from bpy.types import (
    Brush,
    Texture
)

def toggle_off_curves():
    scn = bpy.types.Scene
    scn.depress_Smooth = True
    scn.depress_Round = True
    scn.depress_Root = True
    scn.depress_Sharp = True
    scn.depress_Line = True
    scn.depress_Max = True

def toggle_off_dyntopo_levels():
    scn = bpy.types.Scene
    scn.depress_dyntopo_lvl_1 = True
    scn.depress_dyntopo_lvl_2 = True
    scn.depress_dyntopo_lvl_3 = True
    scn.depress_dyntopo_lvl_4 = True
    scn.depress_dyntopo_lvl_5 = True
    scn.depress_dyntopo_lvl_6 = True

class NSMUI_OT_toolHeader_brush_curve(bpy.types.Operator):
    bl_idname = "nsmui.ot_curve_shape"
    bl_label = ""
    bl_description = "Change Curve Preset."
    shape: bpy.props.StringProperty(name="shape", default='SMOOTH')
    def execute(self, shape):
        scn = bpy.types.Scene
        toggle_off_curves()
        if self.shape == 'SMOOTH':
            scn.depress_Smooth = False
        elif self.shape == 'ROUND':
            scn.depress_Round = False
        elif self.shape == 'ROOT':
            scn.depress_Root = False
        elif self.shape == 'SHARP':
            scn.depress_Sharp = False
        elif self.shape == 'LINE':
            scn.depress_Line = False
        elif self.shape == 'MAX':
            scn.depress_Max = False

        bpy.ops.brush.curve_preset(shape=self.shape)
        return {'FINISHED'}

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
    bl_description = "Level 6 of detail, the greater one. The more level the more detail !"
    def execute(self, context):
        toggle_off_dyntopo_levels()
        if bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT':
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 125
        elif bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH':
            bpy.context.scene.tool_settings.sculpt.detail_percent = 5
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 1
        bpy.types.Scene.depress_dyntopo_lvl_6 = False
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_2(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_2"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Level 5 of detail. The more level the more detail !"
    def execute(self, context):
        toggle_off_dyntopo_levels()
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 100
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 10
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 2
        bpy.types.Scene.depress_dyntopo_lvl_5 = False
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_3(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_3"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Level 4 of detail. The more level the more detail !"
    def execute(self, context):
        toggle_off_dyntopo_levels()
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 80
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 16
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 4
        bpy.types.Scene.depress_dyntopo_lvl_4 = False
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_4(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_4"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Level 3 of detail. The more level the more detail !"
    def execute(self, context):
        toggle_off_dyntopo_levels()
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 65
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 24
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 6
        bpy.types.Scene.depress_dyntopo_lvl_3 = False
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_5(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_5"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Level 2 of detail. The more level the more detail !"
    def execute(self, context):
        toggle_off_dyntopo_levels()
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 50
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 32
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 9
        bpy.types.Scene.depress_dyntopo_lvl_2 = False
        return {'FINISHED'}

class NSMUI_OT_toolHeader_dyntopo_lvl_6(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_dyntopo_lvl_6"
    bl_label = "New Sculpt-Mode UI"
    bl_description = "Level 1 of detail, the lower one. The more level the more detail !"
    def execute(self, context):
        toggle_off_dyntopo_levels()
        if(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'CONSTANT'):
            bpy.context.scene.tool_settings.sculpt.constant_detail_resolution = 35
        elif(bpy.context.scene.tool_settings.sculpt.detail_type_method == 'BRUSH'):
            bpy.context.scene.tool_settings.sculpt.detail_percent = 48
        else: # bpy.context.scene.tool_settings.sculpt.detail_type_method = 'MANUAL' // 'RELATIVE'
            bpy.context.scene.tool_settings.sculpt.detail_size = 12
        bpy.types.Scene.depress_dyntopo_lvl_1 = False
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


def foo():
    print (time.ctime())

class NSMUI_OT_toolHeader_brush_custom_icon(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_brush_custom_icon"
    bl_label = "Create Custom Icon"
    bl_description = "Create a Custom Icon for the Actual Brush based on the Viewport"
    def execute(self, context):
        scene = context.scene
        brush = bpy.context.tool_settings.sculpt.brush # Get active brush
        brush.use_custom_icon = True # Mark to use custom icon
        # active = context.active_object

        # BACKUP DATA
        overlays_state = context.space_data.overlay.show_overlays
        gizmo_state = context.space_data.show_gizmo
        resX = scene.render.resolution_x
        resY = scene.render.resolution_y
        displayMode = scene.render.display_mode
        oldpath = scene.render.filepath
        lens = context.space_data.lens
        film = scene.render.film_transparent

        # PRIMEROS PREPARATIVOS :)
        scene.render.display_mode = 'NONE'
        context.space_data.overlay.show_overlays = False
        context.space_data.show_gizmo = False
        scene.render.resolution_x = 256
        scene.render.resolution_y = 256
        context.space_data.lens = 80
        scene.render.film_transparent = True

        # RANDOM GENERATION / NOW IS NOT NECESARY
        # import random
        # n = random.randint(0,23) # GENERATE RANDOM NUMBER
        # filename = brush.name + "_icon_" + str(n) + ".png" # GENERATE FILENAME WITH RANDOM NUMBER

        import os
        temp_dir = bpy.app.tempdir # TEMPORAL FOLDER OF THE ACTUAL BLENDER PROJECT
        script_file = os.path.realpath(__file__)
        addon_dir = os.path.dirname(script_file) # ADDON'S DIRECTORY
        icons_folder = "/icons/"
        icons_dir = addon_dir + "/Sculpt_Brushes" + icons_folder
        
        filename = brush.name + "_icon.png"
        filepath = icons_dir + filename
        # print(filepath)

        # RENDER SETTINGS
        scene.render.image_settings.file_format = 'PNG'
        scene.render.filepath = filepath
        bpy.ops.render.opengl(write_still=True) # RENDER + SAVE (In filepath as PNG)

        render_image = bpy.data.images["Render Result"] # GET RENDERED IMAGE
        render_image.name = filename # CHANGE RENDERED IMAGE' NAME TO GENERATE FILENAME
        bpy.ops.image.pack() # PACK IMAGE TO .BLEND FILE

        # ASIGN ICON (RENDER) TO BRUSH
        bpy.data.brushes[brush.name].icon_filepath = filepath

        # RESTORE DATA
        scene.render.resolution_x = resX
        scene.render.resolution_y = resY
        context.space_data.overlay.show_overlays = overlays_state
        context.space_data.show_gizmo = gizmo_state
        scene.render.display_mode = displayMode
        scene.render.filepath = oldpath
        context.space_data.lens = lens
        scene.render.film_transparent = film

        try:
            bpy.data.images.remove(bpy.data.images[filename + ".001"])
        except:
            pass
        #print(brush.__dir__())
        #for prop in brush.__dir__():
        #    print("{'0'" + str(prop) + "'0':" +"'0'" + str(prop) + "'0'},")

        # PREPARE NEW RENDER IMAGE SLOT FOR ANOTHER ICON
        bpy.ops.image.new(name="Render Result")

        return {'FINISHED'}


def printAttr(brush):
    for attr in dir(brush):
        if hasattr( brush, attr ):
            print( "{'0'%s'0': '0'%s'0'}," % (attr, getattr(brush, attr)))
            # print( "obj.%s = %s" % (attr, getattr(brush, attr)))
    return {'FINISHED'}


class NSMUI_OT_toolHeader_UI_preset_default(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_ui_preset_default"
    bl_label = "Default UI Preset"
    bl_description = "Change Tool Header UI to default state. Reset."
    def execute(self, context):
        wm = context.window_manager
        wm.toggle_brush_menu = True
        wm.toggle_UI_elements = True
        wm.toggle_prefs = True
        wm.toggle_brush_customIcon = False
        wm.toggle_stages = True
        wm.toggle_brush_settings = True
        wm.toggle_brushAdd = True
        wm.toggle_brushRemove = False
        wm.toggle_brushReset = True
        wm.toggle_stroke_settings = True
        wm.toggle_stroke_method = False
        wm.toggle_falloff = True
        wm.toggle_falloff_curvePresets = False
        wm.toggle_sliders = True
        wm.toggle_slider_brushSize = True
        wm.toggle_slider_brushStrength = True
        wm.toggle_slider_brushSmooth = True
        wm.toggle_slider_spacing = False
        wm.toggle_dyntopo = True
        wm.toggle_mask = False
        wm.toggle_symmetry = True
        wm.toggle_texture_new = True
        wm.toggle_texture_open = True

        return {'FINISHED'}

class NSMUI_OT_toolHeader_UI_preset_recommendation(bpy.types.Operator):
    bl_idname = "nsmui.ht_toolheader_ui_preset_recommendation"
    bl_label = "Recommended UI Preset"
    bl_description = "Use recommended preset to change Tool Header UI."
    def execute(self, context):
        if bpy.context.window.workspace == bpy.data.workspaces["Sculpting"]:
            bpy.ops.screen.header_toggle_menus()
        wm = context.window_manager
        wm.toggle_brush_menu = True
        wm.toggle_UI_elements = True
        wm.toggle_prefs = True
        wm.toggle_brush_customIcon = True
        wm.toggle_stages = True
        wm.toggle_brush_settings = False
        wm.toggle_brushAdd = True
        wm.toggle_brushRemove = False
        wm.toggle_brushReset = False
        wm.toggle_stroke_settings = False
        wm.toggle_stroke_method = True
        wm.toggle_falloff = False
        wm.toggle_falloff_curvePresets = True
        wm.toggle_sliders = True
        wm.toggle_slider_brushSize = False
        wm.toggle_slider_brushStrength = False
        wm.toggle_slider_brushSmooth = False
        wm.toggle_slider_spacing = False
        wm.toggle_dyntopo = True
        wm.toggle_mask = False
        wm.toggle_symmetry = True
        wm.toggle_texture_new = True
        wm.toggle_texture_open = True

        return {'FINISHED'}