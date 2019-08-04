# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "NewSculptUI",
    "author" : "JFranMatheu",
    "description" : "New UI and Tools for Sculpt Mode! :D",
    "blender" : (2, 80, 0),
    "version" : (0, 5, 4),
    "location" : "View3D > Tool Header /// View3D > 'N' Panel: Brushes / Sculpt)",
    "warning" : "This version is still in development. ;)",
    "category" : "Generic"
}
support = True
#import gpu
#import bgl
#from gpu_extras.batch import batch_for_shader
from gpu_extras.presets import draw_texture_2d#, draw_circle_2d
#import functools
# IMPORTS # NECESITA LIMPIEZA!!!
import sys
import os
import platform
import bpy 
import traceback
from bpy.types import Operator, AddonPreferences, Header, Panel, Brush, UIList, Menu, Texture, Scene, WindowManager, UILayout
from bl_ui.utils import PresetPanel
import bpy.utils.previews
from os.path import dirname, join, abspath, basename
from bpy import context, types, ops
from bl_ui.properties_paint_common import (
        UnifiedPaintPanel,
        brush_texture_settings,
        brush_texpaint_common,
        brush_mask_texture_settings,
        brush_basic_sculpt_settings
        )
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, FloatVectorProperty, BoolVectorProperty
from bpy.utils import register_class, unregister_class
from bl_ui.space_view3d import VIEW3D_HT_tool_header

platform = platform.system()

# ----------------------------------------------------------------- #
#   ADDON PREFERENCES                                     #
# ----------------------------------------------------------------- #

class NSMUI_AddonPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = "NewSculptUI"
    '''
    filepath: StringProperty(
        name="Example File Path",
        subtype='FILE_PATH',
    )
    '''

    if platform == "Windows":
        IM_filepath = "/Remesher/Windows/Instant Meshes.exe"
        Q_filepath = "/Remesher/Windows/quadriflow_clang.exe" # thanks to javitang
    elif platform == "Linux":
        IM_filepath = "/Remesher/Linux/Instant Meshes"
        Q_filepath = ""
    elif platform == "Darwin":
        IM_filepath = "/Remesher/MacOS/Instant Meshes.app"
        Q_filepath = ""

    quadriflow_filepath : bpy.props.StringProperty(
        name="Quadriflow Executable",
        subtype='FILE_PATH',
        default=os.path.dirname(__file__) + Q_filepath
    )
    instantMeshes_filepath: bpy.props.StringProperty(
        name="Instant Meshes Executable",
        subtype='FILE_PATH',
        default=os.path.dirname(__file__) + IM_filepath,
    )
    '''
    meshlab_filepath: bpy.props.StringProperty(
        name="Meshlab Server Executable",
        subtype='FILE_PATH',
        default="C:\Program Files\VCG\MeshLab\meshlabserver.exe",
    )
    '''
    #########################################################
    #   UPDATE VALUES FROM PREFERENCES TO DYNTOPO STAGES    #
    #########################################################
    # Relative
    def update_relativeLow(self, context):
        dyntopoStages[0].relative_Values = self.relative_Low
    def update_relativeMid(self, context):
        dyntopoStages[1].relative_Values = self.relative_Mid
    def update_relativeHigh(self, context):
        dyntopoStages[2].relative_Values = self.relative_High
    # Constant
    def update_constantLow(self, context):
        dyntopoStages[0].constant_Values = self.constant_Low
    def update_constantMid(self, context):
        dyntopoStages[1].constant_Values = self.constant_Mid
    def update_constantHigh(self, context):
        dyntopoStages[2].constant_Values = self.constant_High
    # Brush
    def update_brushLow(self, context):
        dyntopoStages[0].brush_Values = self.brush_Low
    def update_brushMid(self, context):
        dyntopoStages[1].brush_Values = self.brush_Mid
    def update_brushHigh(self, context):
        dyntopoStages[2].brush_Values = self.brush_High

    # USE CUSTOM DYNTOPO VALUES
    dyntopo_UseCustomValues: BoolProperty(
        name="Custom Values",
        description="Use Custom Values for Dyntopo's new system by levels and stages",
        default=False,
    )
    # RELATIVE VALUES
    relative_Low : FloatVectorProperty(
        name="Relative Low Value", description="",
        subtype='NONE', default=[14, 12, 10], soft_min=10, soft_max=20,
        size=3, step=1, precision=0 ,update=update_relativeLow
    )
    relative_Mid : FloatVectorProperty(
        name="Relative Mid Value", description="",
        subtype='NONE', default=[8, 6, 4], soft_min=4, soft_max=10,
        size=3, step=1, precision=0 ,update=update_relativeMid
    )
    relative_High : FloatVectorProperty(
        name="Relative High Value", description="",
        subtype='NONE', default=[3, 2, 1], soft_min=0.1, soft_max=4,
        size=3, precision=1 ,update=update_relativeHigh
    )
    # CONSTANT VALUES
    constant_Low : FloatVectorProperty(
        name="Constant Low Value", description="",
        subtype='NONE', default=[20, 30, 40], soft_min=0.1, soft_max=50,
        size=3, precision=1 ,update=update_constantLow
    )
    constant_Mid : FloatVectorProperty(
        name="Constant Mid Value", description="",
        subtype='NONE', default=[55, 65, 75], soft_min=50, soft_max=95,
        size=3, step=1, precision=0 ,update=update_constantMid
    )
    constant_High : FloatVectorProperty(
        name="Constant High Value", description="",
        subtype='NONE', default=[95, 110, 125], soft_min=95, soft_max=200,
        size=3, step=1, precision=0 ,update=update_constantHigh
    )
    # BRUSH VALUES
    brush_Low : FloatVectorProperty(
        name="Brush Low Value", description="",
        subtype='NONE', default=[65, 55, 45], soft_min=50, soft_max=100,
        size=3, step=1, precision=0 ,update=update_brushLow
    )
    brush_Mid : FloatVectorProperty(
        name="Brush Mid Value", description="",
        subtype='NONE', default=[35, 27, 20], soft_min=20, soft_max=50,
        size=3, step=1, precision=0 ,update=update_brushMid
    )
    brush_High : FloatVectorProperty(
        name="Brush High Value", description="",
        subtype='NONE', default=[15, 10, 5], soft_min=0.1, soft_max=20,
        size=3, precision=1 ,update=update_brushHigh
    )
    # copy and paste if you want more slots, also you should add them to the layout over pt_ui_panel.py, 
    # just search for the existing slots and copy paste the code and change the name/number of the slot
    custom_UI_Slot_1 : BoolVectorProperty(name="Slot 1", description="Slot number 1 for custom UI presets", subtype='NONE', size=26)
    create_custom_UI_Slot_1 : BoolProperty(name="Create Slot 1", description="Create Slot number 1 for custom UI presets", default=False)
    custom_UI_Slot_2 : BoolVectorProperty(name="Slot 2", description="Slot number 2 for custom UI presets", subtype='NONE', size=26)
    create_custom_UI_Slot_2 : BoolProperty(name="Create Slot 2", description="Create Slot number 2 for custom UI presets", default=False)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        _row = col.row(align=True)
        _row.label(text="Specify the path to 'Instant Meshes' executable")
        prop = _row.operator("wm.url_open", text="Download program", icon='SORT_ASC')
        prop.url = "https://github.com/wjakob/instant-meshes"
        col.prop(self, "instantMeshes_filepath", text="")

        box = layout.box()
        col = box.column(align=True)
        _row = col.row(align=True)
        _row.label(text="Specify the path to 'Quadriflow' executable")
        prop = _row.operator("wm.url_open", text="Download Sources and Compile", icon='SORT_ASC')
        prop.url = "https://github.com/hjwdzh/QuadriFlow"
        if platform == "Linux":
            prop = _row.operator("wm.url_open", text="LINUX GUIDE TO COMPILE", icon='INFO')
            prop.url = "https://blender.community/c/hoy/gjcbbc/"
        col.prop(self, "quadriflow_filepath", text="")

        layout = self.layout
        layout.prop(self, "dyntopo_UseCustomValues", text="Use Custom Values for Dyntopo")
        box = layout.box()
        box.label(text="DYNTOPO: PER STAGES")
        box.active = self.dyntopo_UseCustomValues

        col = box.column(align=True)
        row = col.row(align=True)
        row.separator(factor=6)
        row.label(text="SKETCH")
        row.label(text="DETAIL")
        row.label(text="POLISH")

        _col = col.split().column(align=True)
        #col.label(text="Relative Values")
        _row = _col.row(align=False)
        _row.prop(self, "relative_Low", text="Relative")
        _row.prop(self, "relative_Mid", text="")
        _row.prop(self, "relative_High", text="")

        _col = col.split().column(align=True)
        #_col.label(text="Constant Values")
        _row = _col.row(align=False)
        _row.prop(self, "constant_Low", text="Constant")
        _row.prop(self, "constant_Mid", text="")
        _row.prop(self, "constant_High", text="")

        _col = col.split().column(align=True)
        #_col.label(text="Brush")
        _row = _col.row(align=False)
        _row.prop(self, "brush_Low", text="Brush")
        _row.prop(self, "brush_Mid", text="")
        _row.prop(self, "brush_High", text="")

        layout.separator()
        box = layout.box()
        col = box.column(align=True)
        col.label(text="CUSTOM UI PRESETS : ")
        row = col.row(align=True)
        row.prop(self, "create_custom_UI_Slot_1", text="Slot 1")
        #row = col.row(align=True)
        #row.prop(self, "custom_UI_Slot_1", text="UI Toggles")
        row = col.row(align=True)
        row.prop(self, "create_custom_UI_Slot_2", text="Slot 2")

        layout.separator()
        box = layout.box()
        col = box.column()
        row = col.row(align=True)
        row.operator("nsmui.check_updates", text="Check for Updates")
        row.operator("nsmui.update", text="Update")

        #layout.label(text="PER LEVELS (BY DEFAULT MODE) : ")

register_class(NSMUI_AddonPreferences)

# ----------------------------------------------------------------- #
#   DYNTOPO SETUP                                                   #
# ----------------------------------------------------------------- #
# Values for Detail Size depending of the METHOD used
# LEFT (LOW) - CENTER (MID) - RIGHT (HIGH)  
# RELATIVE & MANUAL --> a menor valor, mayor detalle. Valor en px.
relative_Low = [14,12,10]
relative_Mid = [8,6,4]
relative_High = [3,2,1]
# CONSTANT --> a mayor valor, mayor detalle. Valor fixed. (Aquí los valores están invertidos)
constant_Low = [20, 30, 40]
constant_Mid = [55, 65, 75]
constant_High = [95, 110, 125]
# BRUSH --> a menor, mayor detalle. Valor en % de detalle.
brush_Low = [65, 55, 45]
brush_Mid = [35, 27, 20]
brush_High = [15, 10, 5]
# LEVEL OF DETAIL GROUPS FOR EACH STAGE # DE MOMENTO AHÍ SE QUEDA AUNQUE SE PODRÍA USAR (para array 3 dimensiones)
# sketch_Values = [relative_Low, constant_Low, brush_Low]
# detail_Values = [relative_Mid, constant_Mid, brush_Mid]
# polish_Values = [relative_High, constant_High, brush_High]
# STRUCT CLASS
class DyntopoStage:

    # BRUSH VALUES
    relative_Values : FloatVectorProperty(
        subtype='NONE', default=[0, 0, 0],
        size=3,
    )
    constant_Values : FloatVectorProperty(
        subtype='NONE', default=[0, 0, 0],
        size=3,
    )
    brush_Values : FloatVectorProperty(
        subtype='NONE', default=[0, 0, 0],
        size=3,
    )
    
    def __init__(self, stage_Name, relative_Values = [], constant_Values =[], brush_Values = []):
        self.stage_Name = stage_Name
        self.relative_Values = relative_Values
        self.constant_Values = constant_Values
        self.brush_Values = brush_Values

    def __repr__(self):
        return "DyntopoStage[%s, %i[], %i[], %i[]]" % (self.stage_Name, self.relative_Values, self.constant_Values, self.brush_Values)
# Dyntopo Stages - Construct vars

# GLOBAL VARS
dynStage_Active = 0 # 1 = SKETCH; 2 = DETAIL; 3 = POLISH; 0 = "NONE" # Por defecto ningún 'stage' está activado
dynMethod_Active = "NONE"
dynValues_ui = [] # valores mostrados en la UI # DEFECTO # Cambiarán al cambiar de stage o detailing (method aquí)

# IN LOAD / IF USE CUSTOM VALUES IS CHECKED, GO CREATE DYNSTAGES VALUES WITH PREFS VALUES
prefs = bpy.context.preferences.addons["NewSculptUI"].preferences
if prefs.dyntopo_UseCustomValues:
    rL = [prefs.relative_Low[0], prefs.relative_Low[1], prefs.relative_Low[2]]
    rM = [prefs.relative_Mid[0], prefs.relative_Mid[1], prefs.relative_Mid[2]]
    rH = [prefs.relative_High[0], prefs.relative_High[1], prefs.relative_High[2]]
    cL = [prefs.constant_Low[0], prefs.constant_Low[1], prefs.constant_Low[2]]
    cM = [prefs.constant_Mid[0], prefs.constant_Mid[1], prefs.constant_Mid[2]]
    cH = [prefs.constant_High[0], prefs.constant_High[1], prefs.constant_High[2]]
    bL = [prefs.brush_Low[0], prefs.brush_Low[1], prefs.brush_Low[2]]
    bM = [prefs.brush_Mid[0], prefs.brush_Mid[1], prefs.brush_Mid[2]]
    bH = [prefs.brush_High[0], prefs.brush_High[1], prefs.brush_High[2]]
    dynStage_Low = DyntopoStage("SKETCH", rL, cL, bL)
    dynStage_Mid = DyntopoStage("DETAILS", rM, cM, bM)
    dynStage_High = DyntopoStage("POLISH", rH, cH, bH)
# IF NOT, GO CREATE DYNSTAGES VALUES WITH DEFAULT VALUES
else:
    dynStage_Low = DyntopoStage("SKETCH", relative_Low, constant_Low, brush_Low)
    dynStage_Mid = DyntopoStage("DETAILS", relative_Mid, constant_Mid, brush_Mid)
    dynStage_High = DyntopoStage("POLISH", relative_High, constant_High, brush_High)
    
dyntopoStages = [dynStage_Low, dynStage_Mid, dynStage_High]

# ----------------------------------------------------------------- #
# ICONS // PREVIEW COLLECTION
# ----------------------------------------------------------------- #
from os import path
icon_dir = path.join(path.dirname(__file__), "icons")
preview_collections = {}

icons = {"mirror_icon" : "mirror_icon.png",
         "brush_icon"  : "brush_icon.png",
         "brushAdd_icon"  : "brushAdd_icon.png",
         "brushSave_icon"  : "brushSave_icon.png",
         "brushRemove_icon"  : "brushRemove_icon.png",
         "brushReset_icon"  : "brushReset_icon.png",
         "strokeSpace_icon" : "strokeSpace_icon.png",
         "strokeDots_icon" : "strokeDots_icon.png",
         "strokeDragDot_icon" : "strokeDragDot_icon.png",
         "strokeAnchored_icon" : "strokeAnchored_icon.png",
         "strokeAirbrush_icon" : "strokeAirbrush_icon.png",
         "strokeLine_icon" : "strokeLine_icon.png",
         "strokeCurve_icon" : "strokeCurve_icon.png",
         "stroke_icon" : "stroke_icon.png",
         "texture_icon"  : "texture_icon.png",
         "textureNew_icon"  : "textureNew_icon.png",
         "textureOpen_icon"  : "textureOpen_icon.png",
         "fallOff_icon" : "fallOff_icon.png",
         "frontFaces_icon"  : "frontFaces_icon.png",
         "dyntopo_icon"  : "dyntopo_icon.png",
         "dyntopoLowDetail_icon"  : "dyntopoLowDetail_icon.png",
         "dyntopoMidDetail_icon"  : "dyntopoMidDetail_icon.png",
         "dyntopoHighDetail_icon"  : "dyntopoHighDetail_icon.png",
         "dyntopoConstant_icon"  : "dyntopoConstant_icon.png",
         "dyntopoRelative_icon"  : "dyntopoRelative_icon.png",
         "dyntopoBrush_icon"  : "dyntopoBrush_icon.png",
         "dyntopoManual_icon"  : "dyntopoManual_icon.png",
         "separator_icon" : "separator_icon.png",
         "arrowUp_icon"  : "arrowUp_icon.png",
         "arrowDown_icon" : "arrowDown_icon.png",
         "mask_icon"  : "mask_icon.png",
         "maskInvert_icon"  : "maskInvert_icon.png",
         "maskClear_icon"  : "maskClear_icon.png",
        }

# ----------------------------------------------------------------- #
# PATHS // CHECKER ADDON PATH
# ----------------------------------------------------------------- #
# PATHS
currentDirectory = dirname(abspath(__file__))
addonsDirectory = dirname(currentDirectory)
compilationInfoPath = join(currentDirectory, "compilation_info.json")
addonName = basename(currentDirectory)
# CHEKER OF ADDON'S PATH
if addonName != "NewSculptUI": # CHANGE THIS
    message = ("\n\n"
        "The name of the folder containing this addon has to be 'NewSculptUI'.\n" # CHANGE THIS
        "Please rename it.")
    raise Exception(message)


# --------------------------------------------- #
# TOOL HEADER - UI - SCULPT MODE
# --------------------------------------------- #

class NSMUI_HT_toolHeader_sculpt(Header, UnifiedPaintPanel):
    bl_idname = "NSMUI_HT_ToolHeader_Sculpt"
    bl_label = "Header Toolbar"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_HEADER"
    bl_context = ".paint_common"
    bl_options = {'REGISTER', 'UNDO'}

    hasStartedToHandle : bpy.props.BoolProperty(default = False)
        
    def drawTexture(self, context, x):

        if(context.mode == "SCULPT"):
            settings = self.paint_settings(context)

            if not context.scene.drawBrushTexture:
                return

            if(settings.brush.texture != None):
                texture = settings.brush.texture

                try:
                    image = texture.image

                    if (not hasattr(self, "oldTexture")) or (self.oldTexture != image):
                        self.oldTexture = image
                        self.canDraw = True
                        texture.use_alpha = True
                        texture.use_calculate_alpha = True
                        image.alpha_mode = 'PREMUL'
                        #bpy.app.timers.register(functools.partial(self.fadeOut, False), first_interval=3.0)
                        
                    #elif self.oldTexture != image:
                    #    self.oldTexture = image
                    #    self.canDraw = True
                    #    texture.use_alpha = True
                    #    texture.use_calculate_alpha = True
                    #    image.alpha_mode = 'PREMUL'
                        #if bpy.app.timers.is_registered(self.fadeOut):
                        #    bpy.app.timers.unregister(self.fadeOut)
                        #bpy.app.timers.register(functools.partial(self.fadeOut, False), first_interval=3.0)
                        
                    if self.canDraw == True:
                        self.oldTexture = image
                        draw_brush_texture(image)

                except:
                    print("Cant Draw Image Texture! No Image asigned to the active texture!")

    #def fadeOut(self, fadeOut):
    #    self.canDraw = fadeOut

    def redraw():
        try:
            bpy.utils.unregister_class(VIEW3D_HT_tool_header)
            bpy.utils.unregister_class(NSMUI_HT_toolHeader_sculpt)
        except:
            pass
        bpy.utils.register_class(NSMUI_HT_toolHeader_sculpt)
        bpy.utils.register_class(VIEW3D_HT_tool_header)

    def draw(self, context):
        if(context.mode == "SCULPT"):
            #self.layout.template_header() # to change region
            # LOAD COLLECTION OF ICONS
            pcoll = preview_collections["main"]
            # VARIABLES
            toolHeader = NSMUI_HT_toolHeader_sculpt_tools
            brush = bpy.context.tool_settings.sculpt.brush
            settings = self.paint_settings(context)
            sculpt = context.tool_settings.sculpt
            capabilities = brush.sculpt_capabilities
            toolsettings = context.tool_settings
            activeBrush = brush
            ups = toolsettings.unified_paint_settings
            wm = context.window_manager
            brush = settings.brush

            # CALLBACK HANDLER DRAW TEXTURE OF BRUSH IF THERE IS
            # BRUSH TEXTURE PREVIEW
            if context.scene.drawBrushTexture:
                if self.hasStartedToHandle == False:
                    self.hasStartedToHandle = True
                    bpy.types.SpaceView3D.draw_handler_add(self.drawTexture, (context, None), 'WINDOW', 'POST_PIXEL')
            else:
                if self.hasStartedToHandle == True:
                    bpy.types.SpaceView3D.draw_handler_remove(self.drawTexture, (context, None), 'WINDOW', 'POST_PIXEL')
                    self.hasStartedToHandle = False

            # IF THERE'S NO BRUSH, JUST STOP DRAWING
            if brush is None:
                return

            if wm.toggle_brush_customIcon and (not wm.toggle_brush_menu):
                toolHeader.draw_brush_customIcon(self)
                
            toolHeader.draw_brushManager(self, sculpt, wm, wm.toggle_brush_menu,
                pcoll["brushAdd_icon"], wm.toggle_brushAdd,
                #pcoll["brushSave_icon"], wm.toggle_brushSave,
                pcoll["brushReset_icon"], wm.toggle_brushReset, # bpy.types.Scene.resetBrush_Active
                pcoll["brushRemove_icon"], wm.toggle_brushRemove) #bpy.types.Scene.removeBrush_Active

            # IF BRUSH IS MASK BRUSH
            if brush.sculpt_tool == 'MASK':
                #box = self.layout.box()
                #rw = box.row(align=True)
                rw = self.layout.row(align=True)
                rw.ui_units_x = 5.5
                rw.label(text="Tool :")
                rw.prop(brush, "mask_tool", text="")
            
            toolHeader.draw_separator(self, pcoll)

            if not wm.toggle_sliders: # bpy.types.Scene.sliders_Active [OLD]
                if wm.toggle_slider_brushSize: toolHeader.draw_slider_brushSize(self, toolsettings, brush, ups)
                if wm.toggle_slider_brushStrength: toolHeader.draw_slider_brushStrength(self, toolsettings, brush, ups)       
                if wm.toggle_slider_brushSmooth: toolHeader.draw_slider_brushSmooth(self, brush, capabilities)
                if wm.toggle_slider_spacing: toolHeader.draw_slider_spacing(self, brush)
                if wm.toggle_slider_topoRake: toolHeader.draw_slider_topoRake(self, context, brush, capabilities)
                if wm.toggle_slider_specificBrushType: toolHeader.draw_slider_specificBrushType(self, context, brush, capabilities)
                toolHeader.draw_separator(self, pcoll)

            if wm.toggle_brush_settings: toolHeader.draw_brushSettings(self, pcoll["brush_icon"])
            if wm.toggle_stroke_settings: toolHeader.draw_strokeSettings(self, pcoll["stroke_icon"])
            if wm.toggle_stroke_method: toolHeader.draw_strokeMethod(self, brush, pcoll)
            if wm.toggle_falloff: toolHeader.draw_fallOff(self, pcoll["fallOff_icon"])
            if wm.toggle_falloff_curvePresets: toolHeader.draw_fallOff_curvePresets(self, brush)
            toolHeader.draw_frontFaces(self, brush, pcoll["frontFaces_icon"])

            toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_maskSettings(self, wm.toggle_mask, pcoll["mask_icon"], pcoll["maskInvert_icon"], pcoll["maskClear_icon"])
            if wm.toggle_symmetry: toolHeader.draw_symmetry(self, sculpt, pcoll["mirror_icon"])

            toolHeader.draw_separator(self, pcoll)

            if wm.toggle_dyntopo and brush.sculpt_tool != 'MASK':
                toolHeader.draw_topologySettings(self, context, sculpt, pcoll)
                toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_textureSettings(self,
                pcoll["texture_icon"], pcoll["textureNew_icon"], pcoll["textureOpen_icon"], 
                wm.toggle_texture_new, wm.toggle_texture_open)
            toolHeader.draw_textureManager(self, brush, pcoll["texture_icon"])

            toolHeader.draw_separator(self, pcoll)

            if wm.toggle_UI_elements: toolHeader.draw_toggle_UI_elements(self)
            if wm.toggle_prefs: toolHeader.draw_toggle_preferences(self)

            # toolHeader.draw_blender_quick_preferences(self) # Preferencias rápidas de Blender para Sculpt

            # SUPPORT DEVELOPMENT
            if support:
                row = self.layout.row()
                prop = row.operator('wm.url_open', text="", icon='FUND')
                prop.url = "https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=BA3UXNSDLE55E&source=url"

            row = self.layout.split().row(align=True)

            # view3d_header_collections(self, context)

            self.layout.separator(factor=300.0)
            
        else:
            return None

# --------------------------------------------- #
#   UI TOOLS FOR SCULPT MODE's HEADER TOOL
# --------------------------------------------- #
class NSMUI_HT_toolHeader_sculpt_tools(NSMUI_HT_toolHeader_sculpt):

#   SPACING // SEPARATOR
    def draw_separator(self, pcoll):
        layout = self.layout
        split = layout.split()
        col = split.column()
        icon = pcoll["separator_icon"]
        col.label(text="", icon_value=icon.icon_id)

#   CUSTOM BRUSH ICON
    def draw_brush_customIcon(self):
        row = self.layout.row(align=True)
        row.operator("nsmui.ht_toolheader_brush_custom_icon", text="", icon='RESTRICT_RENDER_OFF')

#   BRUSH SELECTOR // ADD / RESET // REMOVE
    def draw_brushManager(self, sculpt, wm, isCollapse, icon_brushAdd, canAdd, icon_brushReset, canReset, icon_brushRemove, canRemove):
        layout = self.layout
        row = layout.row(align=True)
        row.ui_units_x = 9
        # BRUSH LIST
        row.template_ID_preview(sculpt, "brush", new="brush.add", rows=3, cols=8, hide_buttons=True)
        # NEW BRUSH BUTTON (DUPLICATE)
        if isCollapse:
            row.ui_units_x = 8
            NSMUI_HT_toolHeader_sculpt_tools.draw_brushOptions(self)
        else:
            if canAdd:
                row.operator("brush.add", text="", icon_value=icon_brushAdd.icon_id)     
            
            #if canSave:
            #    row.operator("nsmui.ht_toolheader_brush_save", text="", icon_value=icon_brushSave.icon_id)
            # RESET BRUSH BUTTON
            if canReset:
                row.ui_units_x = row.ui_units_x + 1
                row.operator("brush.reset", text="", icon_value=icon_brushReset.icon_id) # RESET BRUSH
            # DELETE BRUSH BUTTON
            if canRemove:
                row.ui_units_x = row.ui_units_x + 1
                row.operator("nsmui.ht_toolheader_brush_remove", text="", icon_value=icon_brushRemove.icon_id) # DELETE BRUSH

#   BRUSH options
    def draw_brushOptions(self):
        split = self.layout.split()
        col = split.column()
        sub = col.column(align=True)
        sub.popover(
            panel="NSMUI_PT_brush_optionsMenu",
            text="")  

#   BRUSH SIZE    
    def draw_slider_brushSize(self, toolsettings, brush, ups):
        layout = self.layout
        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        row.ui_units_x = 4.5
        # row.prop(ups, "use_unified_size", text="Size") # CHECKBOX PARA MARCAR EL UNIFIED SIZE
        if(toolsettings.unified_paint_settings.use_unified_size):
            row.prop(ups, "size", slider=True, text="R") # Size
        else:
            row.prop(brush, "size", slider=True, text="R") # Size
        row.prop(brush, "use_pressure_size", toggle=True, text="")

#   BRUSH STRENTH
    def draw_slider_brushStrength(self, toolsettings, brush, ups):
        layout = self.layout
        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        row.ui_units_x = 4.3
        if(toolsettings.unified_paint_settings.use_unified_strength): 
            row.prop(ups, "strength", slider=True, text="S") # Hardness
        else:
            row.prop(brush, "strength", slider=True, text="S") # Hardness
        row.prop(brush, "use_pressure_strength", toggle=True, text="")

#   BRUSH AUTOSMOOTH SLIDER
    def draw_slider_brushSmooth(self, brush, capabilities):
        split = self.layout.split()
        col = split.column()
        row = col.row(align=True)
        # auto_smooth_factor and use_inverse_smooth_pressure
        row.ui_units_x = 5.8
        if (capabilities.has_auto_smooth):
            row.prop(brush, "auto_smooth_factor", slider=True, text="Smooth")
            row.prop(brush, "use_inverse_smooth_pressure", toggle=True, text="")

#   BRUSH > STROKE > SPACING SLIDER
    def draw_slider_spacing(self, brush):
        col = self.layout.column()
        col.ui_units_x = 6
        # Airbrush
        if brush.use_airbrush:
            col.prop(brush, "rate", text="Rate", slider=True)
        # Space
        if brush.use_space:
            row = col.row(align=True)
            row.prop(brush, "spacing", text="Spacing")
            row.prop(brush, "use_pressure_spacing", toggle=True, text="")
        # Line and Curve
        if brush.use_line or brush.use_curve:
            row = col.row(align=True)
            row.prop(brush, "spacing", text="Spacing")

#   SLIDER FOR TOPOLOGY RAKE
    def draw_slider_topoRake(self, context, brush, capabilities):
        if (capabilities.has_topology_rake and context.sculpt_object.use_dynamic_topology_sculpting):
            col = self.layout.column()
            col.ui_units_x = 6
            row = col.row()
            row.prop(brush, "topology_rake_factor", slider=True)

#   SLIDERS SPECIFICALLY PER EACH BRUSH TYPE  
    def draw_slider_specificBrushType(self, context, brush, capabilities):
        col = self.layout.column()
        col.ui_units_x = 6
        # normal_weight
        if capabilities.has_normal_weight:
            row = col.row(align=True)
            row.prop(brush, "normal_weight", slider=True)

        # crease_pinch_factor
        if capabilities.has_pinch_factor:
            row = col.row(align=True)
            row.prop(brush, "crease_pinch_factor", slider=True, text="Pinch")

        # rake_factor
        if capabilities.has_rake_factor:
            row = col.row(align=True)
            row.prop(brush, "rake_factor", slider=True)

        if brush.sculpt_tool == 'MASK':
            col.prop(brush, "mask_tool")

        # plane_offset, use_offset_pressure, use_plane_trim, plane_trim
        if capabilities.has_plane_offset:
            col.ui_units_x = 5
            row = col.row(align=True)
            row.prop(brush, "plane_offset", slider=True, text="Offset")
            row.prop(brush, "use_offset_pressure", text="")
            row2 = self.layout.column().row()
            row2.ui_units_x = 2.7
            row2.prop(brush, "use_plane_trim", text="Trim")
            if brush.use_plane_trim:
                _col = self.layout.column()
                _col.ui_units_x = 4.5
                _row = _col.row()
                #_row.active = brush.use_plane_trim
                _row.prop(brush, "plane_trim", slider=True, text="Dist")

        # height
        if capabilities.has_height:
            row = col.row()
            row.prop(brush, "height", slider=True, text="Height")

        # use_persistent, set_persistent_base
        if capabilities.has_persistence:
            ob = context.sculpt_object
            do_persistent = True

            # not supported yet for this case
            for md in ob.modifiers:
                if md.type == 'MULTIRES':
                    do_persistent = False
                    break

            if do_persistent:
                row = col.row(align=True)
                row.prop(brush, "use_persistent")
                row.operator("sculpt.set_persistent_base")

#   BRUSH SETTINGS (DROPDOWN)
    def draw_brushSettings(self, icon):
        layout = self.layout
        split = layout.split()
        col = split.column()
        sub = col.column(align=True)
        sub.popover(panel="VIEW3D_PT_tools_brush",icon_value=icon.icon_id,text="")
        #VIEW3D_PT_sculpt_options_unified

#   BRUSH STROKE SETTINGS (DROPDOWN)
    def draw_strokeSettings(self, icon):
        layout = self.layout
        split = layout.split()
        col = split.column()
        sub = col.column(align=True)
        sub.popover(
            panel="VIEW3D_PT_tools_brush_stroke",
            icon_value=icon.icon_id,
            text="")          

#   BRUSH STROKE METHOD
    def draw_strokeMethod(self, brush, pcoll):
        row = self.layout.row(align=True)
        icon = strokeMethod_icon(brush.stroke_method, pcoll)
        row.ui_units_x = 4.5
        # row.label(text="", icon_value=icon.icon_id)
        row.prop(brush, "stroke_method", text="", icon_value=icon.icon_id)

#   BRUSH FALLOFF SETTINGS/CURVES (DROPDOWN)
    def draw_fallOff(self, icon):
        layout = self.layout
        split = layout.split()
        col = split.column()
        sub = col.column(align=True)
        sub.popover(
            panel="VIEW3D_PT_tools_brush_falloff",
            icon_value=icon.icon_id,
            text="")       

#   BRUSH FALLOFF CURVE PRESETS
    def draw_fallOff_curvePresets(self, brush):
        scn = bpy.types.Scene
        
        if scn.depress_Smooth == False: dp_Smooth = True
        else: dp_Smooth = False
        if scn.depress_Round == False: dp_Round = True
        else: dp_Round = False
        if scn.depress_Root == False: dp_Root = True
        else: dp_Root = False
        if scn.depress_Sharp == False: dp_Sharp = True
        else: dp_Sharp = False
        if scn.depress_Line == False: dp_Line = True
        else: dp_Line = False
        if scn.depress_Max == False: dp_Max = True
        else: dp_Max = False
        
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("nsmui.ot_curve_shape", icon='SMOOTHCURVE', depress=dp_Smooth).shape = 'SMOOTH'
        row.operator("nsmui.ot_curve_shape", icon='SPHERECURVE', depress=dp_Round).shape = 'ROUND'
        row.operator("nsmui.ot_curve_shape", icon='ROOTCURVE', depress=dp_Root).shape = 'ROOT'
        row.operator("nsmui.ot_curve_shape", icon='SHARPCURVE', depress=dp_Sharp).shape = 'SHARP'
        row.operator("nsmui.ot_curve_shape", icon='LINCURVE', depress=dp_Line).shape = 'LINE'
        row.operator("nsmui.ot_curve_shape", icon='NOCURVE', depress=dp_Max).shape = 'MAX'

#   FRONT FACES ONLY (TOGGLE)
    def draw_frontFaces(self, brush, icon):
        split = self.layout.split()
        col = split.column()
        col = col.row(align=True)
        col.prop(brush, "use_frontface", text="", icon_value=icon.icon_id)

#   MASK SETTINGS / INVERT / CLEAR
    def draw_maskSettings(self, showMaskMenu, icon_mask, icon_maskInvert, icon_maskClear):
        # MASK MENU
        row = self.layout.row(align=True)
        if showMaskMenu:
            row.menu("VIEW3D_MT_hide_mask", text=" Mask ", icon_value=icon_mask.icon_id)
        # MASK -> INVERT
        props = row.operator("paint.mask_flood_fill", text="", icon_value=icon_maskInvert.icon_id)
        props.mode = 'INVERT'
        # MASK -> CLEAR
        props = row.operator("paint.mask_flood_fill", text="", icon_value=icon_maskClear.icon_id)
        props.mode = 'VALUE'
        props.value = 0

#   SYMMETRY TOGGLES
    def draw_symmetry(self, sculpt, icon):
        # MIRRORS X, Y, Z
        col = self.layout.column()
        row = col.row(align=True)
        row.ui_units_x = 5
        row.operator("nsmui.ht_toolheader_symmetry_all", icon_value=icon.icon_id, text=" ")
        row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
        row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
        row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)

#   TOPOLOGY SETTINGS / DYNTOPO / MULTIRES
    def draw_topologySettings(self, context, sculpt, pcoll):
        mods = context.active_object.modifiers # Carga los modificadores del objeto activo
        ibool = False # Para comprobar si el objeto activo tiene el modificador multires
        # SCULPT --> MULTIRES
        # Si hay modificadores en el objeto activo
        if mods!=None:
            for modifier in mods:
            # Si el modificador 'modifier' es de tipo Multires
                if modifier.type == 'MULTIRES':
                    ibool = True
                    row = self.layout.row(align=True)
                    row.label(text="", icon="MOD_MULTIRES")
                    row.ui_units_x = 5
                    row.prop(modifier, "sculpt_levels", text="Sculpt")
                    row = self.layout.row(align=True)
                    row.ui_units_x = 3.6
                    row.operator("nsmui.ht_toolheader_multires_subdivide", text="Subdivide")
                    row = self.layout.row(align=True)
                    row.ui_units_x = 3.8
                    row.prop(sculpt, "show_low_resolution", text="Fast Nav", toggle=False)
                    break
        # SCULPT --> DYNAMIC TOPOLOGY
        # Si no hay multires y dyntopo está activado
        if ibool==False:
            dynStage_Active = context.window_manager.toggle_dyntopo_stage
            useStage = context.window_manager.toggle_stages
            sub = self.layout.row(align=True)
            sub.popover(panel="VIEW3D_PT_sculpt_dyntopo", text="")
            if(context.sculpt_object.use_dynamic_topology_sculpting==True):
                try:
                    bpy.utils.register_class(NSMUI_PT_dyntopo_stages)
                except:
                    pass
            # Si hay stage
                if not useStage:
                    n = 0 # CHIVATO PARA EL STAGE
                    dynMethod_Active = context.window_manager.toggle_dyntopo_detailing
                    iconLow = pcoll["dyntopoLowDetail_icon"]
                    iconMid = pcoll["dyntopoMidDetail_icon"]
                    iconHigh = pcoll["dyntopoHighDetail_icon"]

                    if(dynStage_Active == '1'):
                        n = 0
                    elif(dynStage_Active == '2'):
                        n = 1
                    elif(dynStage_Active == '3'):
                        n = 2
                # LOOK FOR ACTUAL DYN METHOD
                    if(dynMethod_Active == "RELATIVE"):
                        dynValues_ui = dyntopoStages[n].relative_Values
                        icon = pcoll["dyntopoRelative_icon"]
                    elif(dynMethod_Active == "CONSTANT"):
                        dynValues_ui = dyntopoStages[n].constant_Values
                        icon = pcoll["dyntopoConstant_icon"]
                    elif(dynMethod_Active == "BRUSH"):
                        dynValues_ui = dyntopoStages[n].brush_Values
                        icon = pcoll["dyntopoBrush_icon"]
                    elif(dynMethod_Active == "MANUAL"):
                        dynValues_ui = dyntopoStages[n].relative_Values
                        icon = pcoll["dyntopoManual_icon"]
                    #print(dynValues_ui) # debug de valores
                # PANEL DESPLEGABLE
                    sub.popover(panel="NSMUI_PT_dyntopo_stages", text="", icon_value=icon.icon_id)
                    col = self.layout.column()
                    row = col.row(align=True)
                    #row.ui_units_x = 4
                # BOTONES PARA OPCIONES/VALORES PARA DETAIL SIZE DE DYNTOPO SEGUN EL METHOD Y STAGE
                    if bpy.types.Scene.depressL == True: dpL = False
                    else: dpL = True
                    if bpy.types.Scene.depressM == True: dpM = False
                    else: dpM = True
                    if bpy.types.Scene.depressH == True: dpH = False
                    else: dpH = True
                    
                    row.operator("nsmui.ht_toolheader_dyntopo_any_l", text="", icon_value=iconLow.icon_id, depress=update_depress_M(dpL)).value = dynValues_ui[0] # LOW DETAIL
                    row.operator("nsmui.ht_toolheader_dyntopo_any_m", text="", icon_value=iconMid.icon_id, depress=update_depress_M(dpM)).value = dynValues_ui[1] # MID DETAIL
                    row.operator("nsmui.ht_toolheader_dyntopo_any_h", text="", icon_value=iconHigh.icon_id, depress=update_depress_H(dpH)).value = dynValues_ui[2] # HIGH DETAIL
            # Si no hay ningún 'Stage' activado
                else:
                    sub.popover(panel="NSMUI_PT_dyntopo_stages", text="", icon='STYLUS_PRESSURE') # NUEVO PANEL PARA LOS 'STAGES'
                    layout = self.layout
                    col = layout.column()
                    row = col.row(align=True)
                    row.ui_units_x = 6

                    scn = bpy.types.Scene
        
                    if scn.depress_dyntopo_lvl_1 == False: dp_lvl_1 = True
                    else: dp_lvl_1 = False
                    if scn.depress_dyntopo_lvl_2 == False: dp_lvl_2 = True
                    else: dp_lvl_2 = False
                    if scn.depress_dyntopo_lvl_3 == False: dp_lvl_3 = True
                    else: dp_lvl_3 = False
                    if scn.depress_dyntopo_lvl_4 == False: dp_lvl_4 = True
                    else: dp_lvl_4 = False
                    if scn.depress_dyntopo_lvl_5 == False: dp_lvl_5 = True
                    else: dp_lvl_5 = False
                    if scn.depress_dyntopo_lvl_6 == False: dp_lvl_6 = True
                    else: dp_lvl_6 = False

                    # A menor nivel, mayor detalle, es decir para detalles más pequeños
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_6", text="1", depress=dp_lvl_1) # Botón 1, primer nivel, nivel más alto de detalle
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_5", text="2", depress=dp_lvl_2)
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_4", text="3", depress=dp_lvl_3)
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_3", text="4", depress=dp_lvl_4)
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_2", text="5", depress=dp_lvl_5)
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_1", text="6", depress=dp_lvl_6) # Botón 6, último nivel, nivel más bajo de detalle
                    
            else:
                try:
                    bpy.utils.unregister_class(NSMUI_PT_dyntopo_stages)
                except:
                    pass

#   TEXTURE SETTINGS (DROPDOWN) / NEW TEXTURE / OPEN IMAGE
    def draw_textureSettings(self, icon_texture, icon_textureNew, icon_textureOpen, toggle_newTexture, toggle_openImage):
        sub = self.layout.column()
        sub.popover(panel="VIEW3D_PT_tools_brush_texture", icon_value=icon_texture.icon_id, text="")
        row = self.layout.row(align=True)
        if toggle_newTexture:
            row.operator("nsmui.ht_toolheader_new_texture", text="", icon_value=icon_textureNew.icon_id) # NEW TEXTURE
        if toggle_openImage:
            row.operator("image.open", text="", icon_value=icon_textureOpen.icon_id) # OPEN IMAGE TEXTURE

#   TEXTURE QUICK SELECTOR
    def draw_textureManager(self, brush, icon):
        texture = brush.texture
        row = self.layout.row(align=True)
        ## TEXTURES AND IMAGES
        if texture != None: # HAY TEXTURA
            if texture.image != None: # image_user -> image # LA TEXTURA TIENE IMAGEN
                row.template_ID_preview(brush, "texture", rows=3, cols=8, hide_buttons=True)
                row.template_ID_preview(texture, "image", rows=3, cols=8, hide_buttons=True) # open="image.open"
            else: # LA TEXTURA NOO TIENE IMAGEN
                row.ui_units_x = 5
                row.template_ID_preview(texture, "image", rows=3, cols=8, open="image.open", hide_buttons=False) # open="image.open"
        else: # NO HAY TEXTURA
            row.ui_units_x = 5
            row.template_ID_preview(brush, "texture", rows=3, cols=8, new="texture.new", hide_buttons=False)

#   PANEL FOR TOGGLE UI ELEMENTS
    def draw_toggle_UI_elements(self):
        sub = self.layout.split().column(align=True)
        sub.popover(panel="NSMUI_PT_th_settings",icon='HIDE_OFF',text="")

#   PREFERENCES PANEL
    def draw_toggle_preferences(self):
        sub = self.layout.split().column(align=True)
        sub.popover(panel="NSMUI_PT_Addon_Prefs",icon='PREFERENCES',text="")

#   BLENDER QUICK PREFERENCES FOR SCULPT
    def draw_blender_quick_preferences(self):
        sub = self.layout.split().column(align=True)
        sub.popover(panel="NSMUI_PT_Blender_QuickPrefs",icon='BLENDER',text="")
        
# --------------------------------------------- #
# HEADER UI
# --------------------------------------------- #
class NSMUI_HT_header_sculpt(Header):
    bl_idname = "NSMUI_HT_Header_Sculpt"
    bl_label = "Header Toolbar for Sculpt Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    bl_context = ".paint_common"

    def draw(self, context):
        if(context.mode == "SCULPT"):
            #if (bpy.context.space_data.show_region_tool_header == True):
            #    bpy.ops.screen.header_toggle_menus()
            #bpy.types.Area.show_menus = False
            wm = context.window_manager
            scn = context.scene
            pcoll = preview_collections["main"]

            temp = False
            if(bpy.context.space_data.show_region_tool_header == False):
                row = self.layout
                if(temp == False):
                    temp = True
                    icon = pcoll["arrowDown_icon"]
                else:
                    icon = pcoll["arrowUp_icon"]
                row.operator('nsmui.ot_header_tool_toggle', text="New Sculpt-Mode UI", icon_value=icon.icon_id) # id del operador, texto para el botón
                return None
            else: # activar herramientas del addon
                '''
            #   ARROW TO TOGGLE OFF TH.
                if(temp == False):
                    icon = pcoll["arrowUp_icon"]
                else:
                    icon = pcoll["arrowDown_icon"]
                self.layout.row().operator('nsmui.ot_header_tool_toggle', text="", icon_value=icon.icon_id)
                '''
                layout = self.layout
            #   REMESHERS
                if wm.toggle_remesher:
                    col = layout.column()
                    row = col.row(align=True)
                    row.ui_units_x = 7.5
                    #row.label(text="Remesher :")
                    row.popover(
                        panel="NSMUI_PT_remeshOptions",
                        icon='MODIFIER_ON', # EXPERIMENTAL
                        text=""
                    )
                    row.prop(wm, 'switch_remesher', text="", toggle=True, expand=False)

                #   INSTANT MESHES
                    if wm.switch_remesher == 'INSTANT_MESHES':
                        remesh = row.operator('object.instant_meshes_remesh', icon='PLAY', text="")
                        remesh.deterministic = scn.instantMeshes_deterministic
                        remesh.dominant = scn.instantMeshes_dominant
                        remesh.intrinsic = scn.instantMeshes_intrinsic
                        remesh.boundaries = scn.instantMeshes_boundaries
                        remesh.crease = scn.instantMeshes_crease
                        remesh.verts = scn.instantMeshes_verts
                        remesh.smooth = scn.instantMeshes_smooth
                        remesh.openUI = scn.instantMeshes_openInInstantMeshes
                        remesh.remeshIt = True
                #   QUADRIFLOW
                    elif wm.switch_remesher == 'QUADRIFLOW':
                        remesh = row.operator('object.quadriflow_remesh', icon='PLAY', text="")
                        remesh.resolution = scn.quadriflow_resolution
                        remesh.sharp = scn.quadriflow_sharp
                        remesh.adaptive = scn.quadriflow_adaptive
                        remesh.mcf = scn.quadriflow_mcf
                        remesh.sat = scn.quadriflow_sat
                        remesh.remeshIt = True
                #   DECIMATION
                    elif wm.switch_remesher == 'DECIMATION':
                        remesh = row.operator('object.decimation_remesh', icon='PLAY', text="")
                        remesh.decimation_ratio = scn.decimation_ratio
                        remesh.decimation_triangulate = scn.decimation_triangulate
                        remesh.decimation_symmetry = scn.decimation_symmetry
                        remesh.decimation_symmetry_axis = scn.decimation_symmetry_axis
                #   DYNTOPO'S FLOOD FILL
                    elif wm.switch_remesher == 'DYNTOPO':
                        remesh = row.operator('object.dyntopo_remesh', icon='PLAY', text="")
                        remesh.resolution = scn.dynremesh_resolution
                        remesh.force_symmetry = scn.dynremesh_forceSymmetry
                        remesh.symmetry_axis = scn.dynremesh_symmetry_axis
                #   MESHLAB
                    '''
                    elif wm.switch_remesher == 'MESHLAB':
                        remesh = row.operator('object.meshlab_remesh', icon='PLAY', text="")
                        #remesh.facescount = scn.meshlab_facescount
                    '''
                        
                    # LINE ABOVE, JUST TRICKY THING
                    sub = col.column(align=True)
                    sub = sub.box()
                    sub.label(text="")

# --------------------------------------------- #
# REMESH OPTIONS
# --------------------------------------------- #
class NSMUI_PT_remeshOptions(Panel):
    bl_label = "Remesh Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Remesh options for each remesh method"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        wm = context.window_manager
        prefs = context.preferences.addons["NewSculptUI"].preferences
        scn = context.scene
        layout = self.layout
        row = layout.row()
        col = row.column()
    #   INSTANT MESHES
        if wm.switch_remesher == 'INSTANT_MESHES':
            col.prop(scn, 'instantMeshes_deterministic')
            col.prop(scn, 'instantMeshes_dominant')
            col.prop(scn, 'instantMeshes_intrinsic')
            col.prop(scn, 'instantMeshes_boundaries')
            col.prop(scn, 'instantMeshes_crease')
            col.prop(scn, 'instantMeshes_verts')
            col.prop(scn, 'instantMeshes_smooth')
            col.prop(scn, 'instantMeshes_openInInstantMeshes')
            if(prefs.instantMeshes_filepath == "" or prefs.instantMeshes_filepath == None):
                col.label(text="Please select the path of")
                col.label(text="the Instant Meshes executable")
                col.prop(prefs, 'instantMeshes_filepath', text="Path")
    #   QUADRIFLOW
        elif wm.switch_remesher == 'QUADRIFLOW':
            col.prop(scn, 'quadriflow_resolution')
            col.prop(scn, 'quadriflow_sharp')
            col.prop(scn, 'quadriflow_adaptive')
            col.prop(scn, 'quadriflow_mcf')
            col.prop(scn, 'quadriflow_sat')
            if(prefs.quadriflow_filepath == "" or prefs.quadriflow_filepath == None):
                col.label(text="Please select the path of")
                col.label(text="the Quadriflow executable")
                col.prop(prefs, 'quadriflow_filepath', text="Path")
        #   QUADRIFLOW
        elif wm.switch_remesher == 'DECIMATION':
            col.prop(scn, 'decimation_ratio')
            col.prop(scn, 'decimation_triangulate')
            row = col.row(align=True)
            row.prop(scn, 'decimation_symmetry')
            row.prop(scn, 'decimation_symmetry_axis')
        #   DYNTOPO REMESH
        elif wm.switch_remesher == 'DYNTOPO':
            col.prop(scn, 'dynremesh_resolution')
            row = col.row()
            row.prop(scn, 'dynremesh_forceSymmetry')
            _row = row.split()
            _row.ui_units_x = 7
            _row.prop(scn, 'dynremesh_symmetry_axis', text="Axis")
        #   MESHLAB
        '''
        elif wm.switch_remesher == 'MESHLAB':
            col.prop(scn, 'meshlab_facescount')
        '''
            
            
 
# --------------------------------------------- #
# DYNTOPO STAGES UI PANEL
# --------------------------------------------- #
class NSMUI_PT_dyntopo_stages(Panel):
    bl_label = "DyntopoStages"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Stages Panel. Stages improve and divide the workflow in 3 stages and each one has 3 nice values to work with. (also depending of the detailing method)"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        dynStage_Active = context.window_manager.toggle_dyntopo_stage
        useStage = context.window_manager.toggle_stages
        if(context.sculpt_object.use_dynamic_topology_sculpting == True):
            pcoll = preview_collections["main"]
            method = context.window_manager.toggle_dyntopo_detailing
            icon1 = pcoll["dyntopoRelative_icon"]
            icon2 = pcoll["dyntopoConstant_icon"]
            icon3 = pcoll["dyntopoBrush_icon"]
            icon4 = pcoll["dyntopoManual_icon"]
            icon_H = pcoll["dyntopoHighDetail_icon"]
            icon_M = pcoll["dyntopoMidDetail_icon"]
            icon_L = pcoll["dyntopoLowDetail_icon"]
            wm = context.window_manager
        # STAGES - SKETCH - DETAIL - POLISH
            layout = self.layout
            row = layout.row(align=True)
            #row.label(text="Stage :   ")
            if useStage:
                row.label(text="DEFAULT MODE")
                row = layout.row(align=True)
                row.prop(wm, 'toggle_stages', text="USE STAGES !", toggle=True, invert_checkbox=True)
                
            else:
                row.label(text="Actual Stage :    " + dynStage_toString(dynStage_Active))
                row.prop(wm, 'toggle_stages', text="", icon='LOOP_BACK', toggle=True, expand=True)
                # STAGES
                col = layout.column()
                row = col.row(align=True)
                row.prop(wm, 'toggle_dyntopo_stage', text="Sketch", toggle=True, expand=True)
            
        # DETAIL METHODS
            col = layout.column()
            row = col.row(align=True)
            if method == 'CONSTANT':
                icon = icon2
            elif method == 'BRUSH':
                icon = icon3
            elif method == 'RELATIVE': # RELATIVE OR MANUAL
                icon = icon1
            elif method == 'MANUAL':
                icon = icon4
            row.label(icon_value=icon.icon_id, text="Detailing Method :   " + method) # Stages - Para niveles de Detalle especificados abajo
            col = layout.column()
            row = col.row(align=True)
            row.prop(wm, 'toggle_dyntopo_detailing', text="Relative", toggle=True, expand=True) #icon_value=icon1.icon_id

            if not useStage:
            # LOOK FOR ACTIVE STAGE
                n = 0
                if(dynStage_Active == '1'):
                    n = 0
                elif(dynStage_Active == '2'):
                    n = 1
                elif(dynStage_Active == '3'):
                    n = 2
            # VALUES FOR STAGES
                prefs = context.preferences.addons["NewSculptUI"].preferences # load preferences (for properties)
                rowH = self.layout.row(align=True)
                rowH.ui_units_x = 5
                rowH.scale_x = 5
                rowH.label(text="Values :") # Valores para el 'Stage' Activo
                rowH.ui_units_x = 9
                rowH.scale_x = 9
                rowH.prop(prefs, "dyntopo_UseCustomValues", toggle=False, text="Use Custom Values") # OUTLINER_DATA_GP_LAYER
                row = self.layout.row(align=True)
                if method == 'CONSTANT':
                    row.label(icon_value=icon_L.icon_id, text=str(dyntopoStages[n].constant_Values[0]))
                    row.label(icon_value=icon_M.icon_id, text=str(dyntopoStages[n].constant_Values[1]))
                    row.label(icon_value=icon_H.icon_id, text=str(dyntopoStages[n].constant_Values[2]))
                elif method == 'BRUSH':
                    row.label(icon_value=icon_L.icon_id, text=str(dyntopoStages[n].brush_Values[0]))
                    row.label(icon_value=icon_M.icon_id, text=str(dyntopoStages[n].brush_Values[1]))
                    row.label(icon_value=icon_H.icon_id, text=str(dyntopoStages[n].brush_Values[2]))
                elif method == 'RELATIVE' or 'MANUAL':
                    row.label(icon_value=icon_L.icon_id, text=str(dyntopoStages[n].relative_Values[0]))
                    row.label(icon_value=icon_M.icon_id, text=str(dyntopoStages[n].relative_Values[1]))
                    row.label(icon_value=icon_H.icon_id, text=str(dyntopoStages[n].relative_Values[2]))
                else:
                    row.label(text="NONE! Select a Stage!")

                self.layout.separator()
                
                if prefs.dyntopo_UseCustomValues:
                    _col = self.layout.column(align=True)
                    _col.prop(wm, "dyntopoStages_editValues", toggle=True, icon="GREASEPENCIL", text="Edit Values") # OUTLINER_DATA_GP_LAYER
                    if wm.dyntopoStages_editValues:
                        box = _col.box()
                        _row = box.row(align=True)

                        stage = wm.toggle_dyntopo_stage
                        if method == 'CONSTANT':
                            if stage == '3': # "Polish":
                                _row.prop(prefs, "constant_High", text="")
                            elif stage == '2': # "Details":
                                _row.prop(prefs, "constant_Mid", text="")
                            elif stage == '1': #  "Sketch":
                                _row.prop(prefs, "constant_Low", text="")

                        elif method == 'RELATIVE': # RELATIVE OR MANUAL
                            if stage == '3': # "Polish":
                                _row.prop(prefs, "relative_High", text="")
                            elif stage == '2': #  "Details":
                                _row.prop(prefs, "relative_Mid", text="")
                            elif stage == '1': #  "Sketch":
                                _row.prop(prefs, "relative_Low", text="")

                        elif method == 'BRUSH':
                            if stage == '3': #  "Polish":
                                _row.prop(prefs, "brush_High", text="")
                            elif stage == '2': #  "Details":
                                _row.prop(prefs, "brush_Mid", text="")
                            elif stage == '1': #  "Sketch":
                                _row.prop(prefs, "brush_Low", text="")
                        
                      

class NSMUI_PT_brush_optionsMenu(Panel):
    bl_label = "Brush Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Dropdown Menu for Brush Options! You can create/remove/reset/create custom icon (all based in active brush)"
    #   BRUSH OPTIONS
    
    def draw(self, context):
        scn = context.scene
        ups = context.tool_settings.unified_paint_settings
        brush = context.tool_settings.sculpt.brush
        #pressureSize = ups.use_unified_size.use_pressure_size
        #pressureStrength = ups.use_unified_strength.use_pressure_strength
        #pressureSpacing = ups.use_unified_spacing.use_pressure_spacing

        pcoll = preview_collections["main"]
        #wm = context.window_manager
        brush = context.tool_settings.sculpt.brush
        icon_brushAdd = pcoll["brushAdd_icon"]
        icon_brushReset = pcoll["brushReset_icon"]
        icon_brushRemove = pcoll["brushRemove_icon"]

        # 1ST ROW
        col = self.layout.column()
        row = col.row(align=True)
        row.scale_y = 1.5
        # NEW BRUSH BUTTON (DUPLICATE)
        row.operator("brush.add", text="New / Duplicate", icon_value=icon_brushAdd.icon_id)
        # row.operator("nsmui.ht_toolheader_brush_save", text="Save Changes", icon='OUTLINER_DATA_GP_LAYER')
        # 2ND ROW
        row = col.row(align=True)
        # RESET BRUSH BUTTON
        row.operator("brush.reset", text="Reset", icon_value=icon_brushReset.icon_id) # RESET BRUSH
        # DELETE BRUSH BUTTON
        row.operator("nsmui.ht_toolheader_brush_remove", text="Remove", icon_value=icon_brushRemove.icon_id) # DELETE BRUSH
        col.separator()

        # 3RD ROW
        row = col.row(align=True)
        row.scale_y = 1.5
        row.operator("nsmui.ht_toolheader_brush_custom_icon", text="Render Custom Brush Icon", icon='RESTRICT_RENDER_OFF')
        col.separator()

        # 4TH ROW
        #col.separator()
        row = col.row(align=True)
        row.scale_y = 1.2
        row.prop(scn, "renderCustomIcon_Alpha", text="Use Alpha", toggle=True)
        _active = not scn.renderCustomIcon_Alpha
        _row = row.column(align=True)#.row(align=True)
        _row.active = _active
        #text = color
        _row.prop(scn, "renderCustomIcon_Color", text="")

        #row.prop(scn, 'pressureSize', text="Pressure Size", toggle=True)
        #col.separator()
        # FUTURE
        # 1. Save Brush State
        # 2. Import/Export
        # 3. Toggle Aplha - DONE
        # 4. Change BG color - DONE

        # LOAD BRUSHES / IMPORT FROM JSON DATABASE
        # row.operator("nsmui.ot_read_json_data", text="Import All Brushes")

# --------------------------------------------- #
# PROPERTIES // UPDATERS                        #
# --------------------------------------------- #
#   DYNTOPO STAGE - ACTIVE
def get_dynStage(self):
    return self["dynStage_Active"]
def set_dynStage(self, value):
    #print(dynStage_Active)
    #print(self)
    #print(value)
    self["dynStage_Active"] = value
bpy.types.Scene.dynStage_Active = bpy.props.IntProperty(
        name="Dyn Stage",
        description = "Actual Stage for Dyntopo",
        default = 0, 
        get = get_dynStage,
        set = set_dynStage,
    )

# DEPRESS PROPS TO L/M/H Values of 'Stages'
def update_depress_L(value):
    bpy.types.Scene.depressL = not value
    return(bpy.types.Scene.depressL)
def update_depress_M(value):
    bpy.types.Scene.depressM = not value
    return(bpy.types.Scene.depressM)
def update_depress_H(value):
    bpy.types.Scene.depressH = not value
    return(bpy.types.Scene.depressH)
bpy.types.Scene.depressL = bpy.props.BoolProperty(default=True)
bpy.types.Scene.depressM = bpy.props.BoolProperty(default=True)
bpy.types.Scene.depressH = bpy.props.BoolProperty(default=True)

def update_dp_Smooth(value):
    bpy.types.Scene.depress_Smooth = not value
    return(bpy.types.Scene.depress_Smooth)
def update_dp_Round(value):
    bpy.types.Scene.depress_Round = not value
    return(bpy.types.Scene.depress_Round)


# Update Properties [Toggle] for all props
def update_property(self, context):
    if self==True:
        self = not self   

def update_dyntopo_detailing(self, context):
    method = context.window_manager.toggle_dyntopo_detailing
    update_dyntopo_stage(self, context)
    if method == 'RELATIVE':
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'RELATIVE'
    elif method == 'CONSTANT':
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'CONSTANT'
    elif method == 'BRUSH':
        bpy.context.scene.tool_settings.sculpt.detail_type_method = 'BRUSH'

def update_dyntopo_stage(self, context):
    bpy.types.Scene.depressL = False
    bpy.types.Scene.depressM = False
    bpy.types.Scene.depressH = False
# --------------------------------------------- #
# ------------------------------------------- #
#   FUNCIONES SUELTAS 
# ------------------------------------------- #
def dynStage_toString(_dynStage):
    s_dynStage =""
    if _dynStage == '1':
        s_dynStage = "SKETCH"
    elif _dynStage == '2':
        s_dynStage = "DETAIL"
    elif _dynStage == '3':
        s_dynStage = "POLISH"
    return s_dynStage

def strokeMethod_icon(method, pcoll):
    if method == 'SPACE':
        return pcoll["strokeSpace_icon"]
    elif method == 'DOTS':
        return pcoll["strokeDots_icon"]
    elif method == 'DRAG_DOT':
        return pcoll["strokeDragDot_icon"]
    elif method == 'ANCHORED':
        return pcoll["strokeAnchored_icon"]
    elif method == 'AIRBRUSH':
        return pcoll["strokeAirbrush_icon"]
    elif method == 'LINE':
        return pcoll["strokeLine_icon"]
    elif method == 'CURVE':
        return pcoll["strokeCurve_icon"]

# draw active brush texture
def draw_brush_texture(image):
    try:
        if image.gl_load():
            raise Exception()
    except:
        pass
    try:
        position = [100, 100]
        #size = image.size
        #if image.size[0] > image.size[1]:
        #    if(image.size[0] > 250):
        #        width = 250
        #        height = image.size[0]*250/image.size[1]
        #else:
        #    if(image.size[1] > 250):
        #        height = 250
        #        width = image.size[1]*250/image.size[0]
        #width, height = clampImageSize(width, height)
        #print(width)
        #print(height)
        draw_texture_2d(image.bindcode, position, 150, 150)
    except:
        pass


def clampImageSize(width, height):
    maxWidth = 250
    maxHeight = 250

    if(width > height): # is landscape?
        if(width > maxWidth): # is overWidth?
            height = height * maxWidth / width # makes height proportional to new clamped width
            width = maxWidth # clamps width to max

    else: # or is portrait?
        if(height > maxHeight): # is overHeight?
            width = width * maxHeight / height # makes width proportional to new clamped height
            height = maxHeight # clamps height to max
    return width, height
             

#################################################
#   REGISTRATION !!!!                      #
#################################################

from . import auto_load
auto_load.init()


def register():
    print('Hello addon!!')

    # ADDON PREFS
    try:
        register_class(NSMUI_AddonPreferences)
    except:
        pass

    # UNREGISTER ORIGINAL TOOL HEADER # changed - antes al inicio del script
    try:
        bpy.utils.unregister_class(VIEW3D_HT_tool_header)
    except:
        pass
    
    # AutoLoad Exterior Classes
    auto_load.register()

    # Register Classes
    
    register_class(NSMUI_HT_toolHeader_sculpt) # TOOL HEADER - SCULPT MODE
    register_class(NSMUI_HT_header_sculpt)     # HEADER      - SCULPT MODE
    register_class(NSMUI_PT_dyntopo_stages)
    register_class(NSMUI_PT_brush_optionsMenu)
    register_class(NSMUI_PT_remeshOptions)

    # Register Collections (ICONS)
    pcoll = bpy.utils.previews.new()
    for key, f in icons.items():
        pcoll.load(key, path.join(icon_dir, f), 'IMAGE')
    preview_collections["main"] = pcoll

    # WM PROPERTIES
    wm = bpy.types.WindowManager
    

    wm.toggle_brush_menu = bpy.props.BoolProperty(default=True, update=update_property, description="Collapse all brush options above to a menu.")
    wm.toggle_UI_elements = bpy.props.BoolProperty(default=True, update=update_property, description="Deprecated")
    wm.toggle_prefs = bpy.props.BoolProperty(default=True, update=update_property, description="Deprecated")
    wm.toggle_brush_customIcon = bpy.props.BoolProperty(default=True, update=update_property, description="Show button to render custom icon for the active brush based on the 3dviewport. The icon may refresh (up to) in 2 seconds in most cases due to changes in Blender internal.")
    wm.toggle_stages = bpy.props.BoolProperty(default=True, update=update_property, description="Switch between Stage Mode (per Stages) and Default Mode (per Levels [1-6]).")
    wm.toggle_brush_settings = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_brushAdd = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle 'Add brush' button to create a new brush as a duplicate of the active brush")
    #wm.toggle_brushSave = bpy.props.BoolProperty(default=False, update=update_property)
    wm.toggle_brushRemove = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle 'Remove Brush' to remove the active brush")
    wm.toggle_brushReset = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle 'Reset Brush' to reset the active brush to it's original state")
    wm.toggle_stroke_settings = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle Stroke Settings menu in the tool header")
    wm.toggle_stroke_method = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle Quick Stroke Method Switcher in the Tool Header")
    wm.toggle_falloff = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Falloff/Curves menu in the tool header")
    wm.toggle_falloff_curvePresets = bpy.props.BoolProperty(default=True, update=update_property, description="Show quick curve presets row in the tool header")

    wm.toggle_sliders = bpy.props.BoolProperty(default=True, update=update_property, description="Hide All Sliders that are active from the tool header. (Also from this menu)")
    wm.toggle_slider_brushSize = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Brush Size/Radius Slider in the Tool Header")
    wm.toggle_slider_brushStrength = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Brush Strength Slider in the Tool Header")
    wm.toggle_slider_brushSmooth = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Brush Autosmooth Slider in the Tool Header")
    wm.toggle_slider_spacing = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Brush Spacing Slider in the Tool Header if it's available")
    wm.toggle_slider_topoRake = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Brush Topology Rake Slider in the Tool Header if it's availbale")
    wm.toggle_slider_specificBrushType = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle Brush Type Specific Sliders in the Tool Header if they're available for the active brush")

    wm.toggle_remesher = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle Remesher Section in the header")
    wm.toggle_dyntopo = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle Dyntopo Section in the tool header")
    wm.toggle_mask = bpy.props.BoolProperty(default=False, update=update_property, description="Toggle Mask Menu in the tool header")
    wm.toggle_symmetry = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle Quick Symmetry in the tool header")
    wm.toggle_texture_new = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle 'New Texture' Button for creating a new texture in the tool header")
    wm.toggle_texture_open = bpy.props.BoolProperty(default=True, update=update_property, description="Toggle 'Open Image' Button for opening images in the tool header")
    wm.toggle_dyntopo_detailing = bpy.props.EnumProperty(
        items=(
            ('RELATIVE', "Relative", ""),
            ('CONSTANT', "Constant", ""),
            ('BRUSH', "Brush", "")
        ),
        default='RELATIVE',
        update=update_dyntopo_detailing,
        description="Switch between detailing method used for dynamic topology."
    )
    wm.toggle_dyntopo_stage = bpy.props.EnumProperty(
        items=(
            #('0', "", ""),
            ('1', "Sketch", ""),
            ('2', "Details", ""),
            ('3', "Polish", "")
        ),
        #default='0',
        update = update_dyntopo_stage,
        description="Switch between Stage. Stages improve and divide the workflow in 3 stages: Sketch, Details and Polish."
    )
    wm.switch_remesher = bpy.props.EnumProperty(
        items=(
            ('INSTANT_MESHES', "Instant Meshes", ""),
            ('QUADRIFLOW', "Quadriflow", ""),
            ('DECIMATION', "Decimation", ""),
            ('DYNTOPO', "Dynremesh", "")
            #('MESHLAB', "Meshlab", "")
        ),
        default='INSTANT_MESHES',
        #update =
        description="Switch between Remesher"
    )

    scn = bpy.types.Scene
    scn.depress_Smooth = bpy.props.BoolProperty(default=False, description="Smooth Curve Preset for the Active Brush.")
    scn.depress_Round = bpy.props.BoolProperty(default=False, description="Rounded Curve Preset for the Active Brush.")
    scn.depress_Root = bpy.props.BoolProperty(default=False, description="Root (dome) Curve Preset for the Active Brush.")
    scn.depress_Sharp = bpy.props.BoolProperty(default=False, description="Sharp (pinch) Curve Preset for the Active Brush.")
    scn.depress_Line = bpy.props.BoolProperty(default=False, description="Linear (piramid) Curve Preset for the Active Brush.")
    scn.depress_Max = bpy.props.BoolProperty(default=False, description="Quadratic Curve Preset for the Active Brush.")

    scn.depress_dyntopo_lvl_1 = bpy.props.BoolProperty(default=False, description="Level 1 of detail, the lower one. The more level the more detail !")
    scn.depress_dyntopo_lvl_2 = bpy.props.BoolProperty(default=False, description="Level 2 of detail. The more level the more detail !")
    scn.depress_dyntopo_lvl_3 = bpy.props.BoolProperty(default=False, description="Level 3 of detail. The more level the more detail !")
    scn.depress_dyntopo_lvl_4 = bpy.props.BoolProperty(default=False, description="Level 4 of detail. The more level the more detail !")
    scn.depress_dyntopo_lvl_5 = bpy.props.BoolProperty(default=False, description="Level 5 of detail. The more level the more detail !")
    scn.depress_dyntopo_lvl_6 = bpy.props.BoolProperty(default=False, description="Level 6 of detail, the greater one. The more level the more detail !")

    scn.drawBrushTexture = bpy.props.BoolProperty(default=False, description="Show Brush Texture Preview in the 3d Viewport")

    scn.renderCustomIcon_Alpha = bpy.props.BoolProperty(default=False, description="Toggle alpha for rendering the custom brush icon. NOTE: Not working in 'Sculpting' Workspace!")
    scn.renderCustomIcon_Color = FloatVectorProperty(name="Background Color for Custom Icon", subtype='COLOR', default=[0.0,0.0,0.0], min=0, max=1, description="Change Color of the background for rendering the custom brush icon")

    #   BRUSHES PANEL PROPS
    scn.show_brushes_fav = bpy.props.BoolProperty(description='Un/Fold Favorite Brushes.', default=True)
    scn.show_brushes_type = bpy.props.BoolProperty(description='Un/Fold Per Type Brushes.', default=True)
    scn.show_brushes_temp = bpy.props.BoolProperty(description='Un/Fold Recent Brushes.', default=False)
    scn.show_brushOptionsWith = bpy.props.BoolProperty(description='Show Brush Options in "Brushes" Panel', default=True)
    scn.recentBrushes_stayInPlace = bpy.props.BoolProperty(description='Stay Brushes in Place when selecting a Brush that is already on the List.', default=False)
    
    wm.toggle_pt_brushPreview = bpy.props.BoolProperty(default=True, update=update_property, description="Show Brush Preview.")
    wm.toggle_pt_brushFavs = bpy.props.BoolProperty(default=True, update=update_property, description="Show Favourite Brushes.")
    wm.toggle_pt_brushType = bpy.props.BoolProperty(default=True, update=update_property, description="Show Brushes per Type (based on active brush).")
    wm.toggle_pt_brushRecents = bpy.props.BoolProperty(default=True, update=update_property, description="Show Recent Brushes")
    wm.toggle_pt_brushShowOnlyIcons = bpy.props.BoolProperty(default=False, update=update_property, description="Show Only The Icons of the Brushes")
    wm.toggle_pt_brushes_collapse = bpy.props.BoolProperty(default=False, update=update_property, name="Collapse Brushes", description="Hide brush sub-panels and shows dropdown menus for adjust the actual brush.")

    wm.dyntopoStages_editValues =  bpy.props.BoolProperty(default=False, update=update_property, name="Edit Custom Values", description="Show custom values to be able of editing them")

    # INSTANT MESHES REMESHER PROPS
    scn.instantMeshes_deterministic = bpy.props.BoolProperty(name="Deterministic (slower)", description="Prefer (slower) deterministic algorithms", default=False)
    scn.instantMeshes_dominant = bpy.props.BoolProperty(name="Dominant", description="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh", default=False)
    scn.instantMeshes_intrinsic = bpy.props.BoolProperty(name="Intrinsic", description="Intrinsic mode (extrinsic is the default)", default=False)
    scn.instantMeshes_boundaries = bpy.props.BoolProperty(name="Boundaries", description="Align to boundaries (only applies when the mesh is not closed)", default=False)
    scn.instantMeshes_crease = bpy.props.IntProperty(name="Crease Degree", description="Dihedral angle threshold for creases", default=0, min=0, max=100)
    scn.instantMeshes_verts = bpy.props.IntProperty(name="Vertex Count", description="Desired vertex count of the output mesh", default=2000, min=10, max=50000)
    scn.instantMeshes_smooth = bpy.props.IntProperty(name="Smooth iterations", description="Number of smoothing & ray tracing reprojection steps (default: 2)", default=2, min=0, max=10)
    scn.instantMeshes_openInInstantMeshes = bpy.props.BoolProperty(name="Open in InstantMeshes", description="Opens the selected object in Instant Meshes and imports the result when you are done.", default=False)

    # QUADRIFLOW REMESHER PROPS
    scn.quadriflow_resolution = bpy.props.IntProperty(name="Resolution", description="Desired quad face count of the output mesh", default=2000, min=10, max=50000)
    scn.quadriflow_sharp = bpy.props.BoolProperty(name="Sharp Edges", description="Detect and preserve sharp edges", default=False)
    scn.quadriflow_adaptive = bpy.props.BoolProperty(name="Adaptive Scale", description="", default=False)
    scn.quadriflow_mcf = bpy.props.BoolProperty(name="Minimum Cost Flow", description="Enable Adaptive network simplex minimum-cost flow solver(slower)", default=False)
    scn.quadriflow_sat = bpy.props.BoolProperty(name="Aggresive SAT (Unix Only)", description="Tries to guarantee a watertight result mesh(requires the minisat and timeout programs in path)", default=False)

    # DECIMATION REMESH PROPS
    scn.decimation_type = bpy.props.EnumProperty(
        items=(('COLLAPSE', "Collapse", ""), ('UNSUBDIVIDE', "Un-Subdivide", ""), ('PLANAR', "Planar", "")),
        default='COLLAPSE', description="Decimation Type to apply"
    )
    scn.decimation_ratio = FloatProperty(name="% of Tris", subtype='PERCENTAGE', default=100, min=0, max=100, precision=2, description="Percentage of triangles. Less value = less triangles")
    scn.decimation_triangulate = bpy.props.BoolProperty(name="Triangulate", description="", default=False)
    scn.decimation_symmetry = bpy.props.BoolProperty(name="Symmetry", description="", default=False)
    scn.decimation_symmetry_axis = bpy.props.EnumProperty(
        items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")),
        default='X', name="Axis", description="Axis where apply symmetry"
    )

    # DYNREMESH / FLOOD FILL REMESH PROPS
    scn.dynremesh_resolution = FloatProperty(name="Resolution", subtype='FACTOR', default=100, min=1, max=300, precision=2, description="Mesh resolution. Higher value for a high mesh resolution")
    scn.dynremesh_forceSymmetry = bpy.props.BoolProperty(name="Force Symmetry", description="", default=False)
    scn.dynremesh_symmetry_axis = bpy.props.EnumProperty(
        items=(('POSITIVE_X', "X", ""), ('POSITIVE_Y', "Y", ""), ('POSITIVE_Z', "Z", "")),
        default='POSITIVE_X', name="Axis", description="Axis where apply symmetry"
    )

    # MESHLAB REMESH
    #scn.meshlab_facescount = IntProperty(name="facescount", description="Number of faces", default=5000, min=10, max=1000000)

    
    # REFERENCES PANEL PROPS
    # (Import Scene and Image just so the line is shorter)
    from bpy.types import Image
    scn.refImage = bpy.props.PointerProperty(name="Image", type=Image)

    # REGISTER ORIGINAL TOOL HEADER # changed - antes al final del código de la clase del tool header
    try:
        bpy.utils.register_class(VIEW3D_HT_tool_header)
    except:
        pass

    print("Registered New Sculpt Mode UI")


def unregister():
    # UnRegister Classes
    unregister_class(NSMUI_HT_toolHeader_sculpt) # TOOL HEADER - SCULPT MODE
    unregister_class(NSMUI_HT_header_sculpt)     # HEADER      - SCULPT MODE
    unregister_class(NSMUI_PT_dyntopo_stages)
    unregister_class(NSMUI_PT_brush_optionsMenu)
    unregister_class(NSMUI_AddonPreferences)
    unregister_class(NSMUI_PT_remeshOptions)

    # AutoLoad Exterior Classes
    auto_load.unregister()

    # UnRegister Collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    # PROPERTIES
    wm = bpy.types.WindowManager

    del wm.toggle_brush_menu
    del wm.toggle_UI_elements
    del wm.toggle_brush_customIcon

    del wm.toggle_sliders
    del wm.toggle_slider_brushSize
    del wm.toggle_slider_brushStrength
    del wm.toggle_slider_brushSmooth
    del wm.toggle_slider_spacing
    del wm.toggle_slider_topoRake
    del wm.toggle_slider_specificBrushType

    del wm.toggle_brush_settings
    del wm.toggle_brushAdd
    #del wm.toggle_brushSave
    del wm.toggle_brushRemove
    del wm.toggle_brushReset
    del wm.toggle_stroke_settings
    del wm.toggle_stroke_method
    del wm.toggle_falloff
    del wm.toggle_falloff_curvePresets
    del wm.toggle_remesher
    del wm.toggle_dyntopo
    del wm.toggle_mask
    del wm.toggle_symmetry
    del wm.toggle_texture_new
    del wm.toggle_texture_open
    del wm.toggle_dyntopo_detailing
    del wm.toggle_dyntopo_stage
    del wm.toggle_stages
    del wm.toggle_prefs

    del wm.switch_remesher

    scn = bpy.types.Scene
    del bpy.types.Scene.depress_Smooth
    del bpy.types.Scene.depress_Round
    del bpy.types.Scene.depress_Root
    del bpy.types.Scene.depress_Sharp
    del bpy.types.Scene.depress_Line
    del bpy.types.Scene.depress_Max

    del scn.depress_dyntopo_lvl_1
    del scn.depress_dyntopo_lvl_2
    del scn.depress_dyntopo_lvl_3
    del scn.depress_dyntopo_lvl_4
    del scn.depress_dyntopo_lvl_5
    del scn.depress_dyntopo_lvl_6

    del scn.drawBrushTexture

    del scn.renderCustomIcon_Alpha
    del scn.renderCustomIcon_Color

    # INSTANT MESHES REMESHER PROPS
    del scn.instantMeshes_deterministic
    del scn.instantMeshes_dominant
    del scn.instantMeshes_intrinsic
    del scn.instantMeshes_boundaries
    del scn.instantMeshes_crease
    del scn.instantMeshes_verts
    del scn.instantMeshes_smooth
    del scn.instantMeshes_openInInstantMeshes

    # QUADRIFLOW REMESHER PROPS
    del scn.quadriflow_resolution
    del scn.quadriflow_sharp
    del scn.quadriflow_adaptive
    del scn.quadriflow_mcf
    del scn.quadriflow_sat

    # DECIMATION REMESH PROPS
    del scn.decimation_type
    del scn.decimation_ratio
    del scn.decimation_triangulate
    del scn.decimation_symmetry
    del scn.decimation_symmetry_axis

    # DYNREMESH PROPS
    del scn.dynremesh_resolution
    del scn.dynremesh_forceSymmetry
    del scn.dynremesh_symmetry_axis

    # MESHLAB REMESH
    #del scn.meshlab_facescount

    # CLEAN REMESH TEMP FILES
    try:
        os.remove(os.path.join(tempfile.gettempdir(), 'original.obj'))
        os.remove(os.path.join(tempfile.gettempdir(), 'out.obj'))
    except:
        pass

    #   BRUSHES PANEL PROPS
    del scn.show_brushes_fav
    del scn.show_brushes_type
    del scn.show_brushes_temp
    del scn.recentBrushes_stayInPlace
    del scn.show_brushOptionsWith
    del wm.toggle_pt_brushes_collapse
    del wm.toggle_pt_brushPreview
    del wm.toggle_pt_brushFavs
    del wm.toggle_pt_brushType
    del wm.toggle_pt_brushRecents
    del wm.toggle_pt_brushShowOnlyIcons

    del wm.dyntopoStages_editValues

    print("Unregistered New Sculpt Mode UI")