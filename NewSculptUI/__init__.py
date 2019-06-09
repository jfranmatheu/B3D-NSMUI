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
    "description" : "New UI for Sculpt Mode! :D",
    "blender" : (2, 80, 0),
    "version" : (0, 3, 2),
    "location" : "View3D > Tool Header // View3D > 'N' Panel: Sculpt)",
    "warning" : "This version is still in development. ;)",
    "category" : "Generic"
}

# IMPORTS # NECESITA LIMPIEZA!!!
import os
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
from bl_ui.space_view3d import VIEW3D_HT_tool_header
from bpy.props import StringProperty, IntProperty, FloatProperty
from bpy.utils import register_class, unregister_class

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
constant_Low = [95, 110, 125]
constant_Mid = [55, 65, 75]
constant_High = [20, 30, 40]
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
    def __init__(self, stage_Name, relative_Values = [], constant_Values =[], brush_Values = []):
        self.stage_Name = stage_Name
        self.relative_Values = relative_Values
        self.constant_Values = constant_Values
        self.brush_Values = brush_Values

    def __repr__(self):
        return "DyntopoStage[%s, %i[], %i[], %i[]]" % (self.stage_Name, self.relative_Values, self.constant_Values, self.brush_Values)
# Dyntopo Stages - Construct vars
dynStage_Low = DyntopoStage("SKETCH", relative_Low, constant_High, brush_Low) # (por un fallo están al revés los HIGH/LOW)
dynStage_Mid = DyntopoStage("DETAILS", relative_Mid, constant_Mid, brush_Mid)
dynStage_High = DyntopoStage("POLISH", relative_High, constant_Low, brush_High)
dyntopoStages = [dynStage_Low, dynStage_Mid, dynStage_High]
# GLOBAL VARS
dynStage_Active = 0 # 1 = SKETCH; 2 = DETAIL; 3 = POLISH; 0 = "NONE" # Por defecto ningún 'stage' está activado
dynMethod_Active = "NONE"
dynValues_ui = [3,6,9] # valores mostrados en la UI # DEFECTO # Cambiarán al cambiar de stage o detailing (method aquí)

# ----------------------------------------------------------------- #
#   SETTINGS FOR TOOL HEADER UI                                     #
# ----------------------------------------------------------------- #


# ----------------------------------------------------------------- #
# ICONS // PREVIEW COLLECTION
# ----------------------------------------------------------------- #
from os import path
icon_dir = path.join(path.dirname(__file__), "icons")
preview_collections = {}

icons = {"mirror_icon" : "mirror_icon.png",
         "brush_icon"  : "brush_icon.png",
         "brushAdd_icon"  : "brushAdd_icon.png",
         "brushRemove_icon"  : "brushRemove_icon.png",
         "brushReset_icon"  : "brushReset_icon.png",
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
    bl_options = {'REGISTER'}

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
            # LOAD COLLECTION OF ICONS
            pcoll = preview_collections["main"]
            # VARIABLES
            toolHeader = NSMUI_HT_toolHeader_sculpt_tools
            brush = bpy.context.tool_settings.sculpt.brush
            sculpt = context.tool_settings.sculpt
            capabilities = brush.sculpt_capabilities
            toolsettings = context.tool_settings
            settings = self.paint_settings(context)
            brush = settings.brush
            ups = toolsettings.unified_paint_settings
            wm = context.window_manager
            
            # IF THERE'S NO BRUSH, JUST STOP DRAWING
            
            if brush is None:
                return

            if wm.toggle_brush_customIcon: toolHeader.draw_brush_customIcon(self, context)
                
            toolHeader.draw_brushManager(self, sculpt, wm, 
                pcoll["brushAdd_icon"], wm.toggle_brushAdd,
                pcoll["brushReset_icon"], wm.toggle_brushReset, # bpy.types.Scene.resetBrush_Active
                pcoll["brushRemove_icon"], wm.toggle_brushRemove) #bpy.types.Scene.removeBrush_Active
            
            toolHeader.draw_separator(self, pcoll)

            if wm.toggle_sliders: # bpy.types.Scene.sliders_Active [OLD]
                if wm.toggle_slider_brushSize: toolHeader.draw_slider_brushSize(self, toolsettings, brush, ups)
                if wm.toggle_slider_brushStrength: toolHeader.draw_slider_brushStrength(self, toolsettings, brush, ups)       
                if wm.toggle_slider_brushSmooth: toolHeader.draw_slider_brushSmooth(self, brush, capabilities)
                if wm.toggle_slider_spacing: toolHeader.draw_slider_spacing(self, brush)
                toolHeader.draw_separator(self, pcoll)

            if wm.toggle_brush_settings: toolHeader.draw_brushSettings(self, pcoll["brush_icon"])
            if wm.toggle_stroke_settings: toolHeader.draw_strokeSettings(self, pcoll["stroke_icon"])
            if wm.toggle_stroke_method: toolHeader.draw_strokeMethod(self, brush)
            if wm.toggle_falloff: toolHeader.draw_fallOff(self, pcoll["fallOff_icon"])
            if wm.toggle_falloff_curvePresets: toolHeader.draw_fallOff_curvePresets(self, brush)
            toolHeader.draw_frontFaces(self, brush, pcoll["frontFaces_icon"])

            toolHeader.draw_separator(self, pcoll)

            if wm.toggle_mask: toolHeader.draw_maskSettings(self, pcoll["mask_icon"], pcoll["maskInvert_icon"], pcoll["maskClear_icon"])
            if wm.toggle_symmetry: toolHeader.draw_symmetry(self, sculpt, pcoll["mirror_icon"])

            toolHeader.draw_separator(self, pcoll)

            if wm.toggle_dyntopo: 
                toolHeader.draw_topologySettings(self, context, sculpt, pcoll)
                toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_textureSettings(self,
                pcoll["texture_icon"], pcoll["textureNew_icon"], pcoll["textureOpen_icon"], 
                wm.toggle_texture_new, wm.toggle_texture_open)
            toolHeader.draw_textureManager(self, brush, pcoll["texture_icon"])

            toolHeader.draw_separator(self, pcoll)

            if wm.toggle_UI_elements: toolHeader.draw_toggle_UI_elements(self)
            if wm.toggle_prefs: toolHeader.draw_toggle_preferences(self)

            # self.layout.template_palette(toolsettings.image_paint, "palette", color=True)

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
    def draw_brush_customIcon(self, context):
        row = self.layout.row(align=True)
        row.operator("nsmui.ht_toolheader_brush_custom_icon", text="", icon='RESTRICT_RENDER_OFF')

#   BRUSH SELECTOR // ADD / RESET // REMOVE
    def draw_brushManager(self, sculpt, wm, icon_brushAdd, canAdd, icon_brushReset, canReset, icon_brushRemove, canRemove):
        layout = self.layout
        row = layout.row(align=True)
        row.ui_units_x = 9
        # BRUSH LIST
        row.template_ID_preview(sculpt, "brush", new="brush.add", rows=3, cols=8, hide_buttons=True)
        # NEW BRUSH BUTTON (DUPLICATE)
        if canAdd:
            row.operator("brush.add", text="", icon_value=icon_brushAdd.icon_id)     
        # RESET BRUSH BUTTON
        if canReset:
            row.ui_units_x = row.ui_units_x + 1
            row.operator("brush.reset", text="", icon_value=icon_brushReset.icon_id) # RESET BRUSH
        # DELETE BRUSH BUTTON
        if canRemove:
            row.ui_units_x = row.ui_units_x + 1
            row.operator("nsmui.ht_toolheader_brush_remove", text="", icon_value=icon_brushRemove.icon_id) # DELETE BRUSH

#   BRUSH SIZE    
    def draw_slider_brushSize(self, toolsettings, brush, ups):
        layout = self.layout
        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        row.ui_units_x = 8
        # row.prop(ups, "use_unified_size", text="Size") # CHECKBOX PARA MARCAR EL UNIFIED SIZE
        if(toolsettings.unified_paint_settings.use_unified_size):
            row.prop(ups, "size", slider=True, text="Size") # ups -> tool_settings.unified_paint_settings.size
        else:
            row.prop(brush, "size", slider=True, text="Size")
        row.prop(brush, "use_pressure_size", toggle=True, text="")

#   BRUSH STRENTH
    def draw_slider_brushStrength(self, toolsettings, brush, ups):
        layout = self.layout
        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        #row.ui_units_x = 6
        if(toolsettings.unified_paint_settings.use_unified_strength): 
            row.prop(ups, "strength", slider=True, text="Hardness") # ups -> tool_settings.unified_paint_settings.strength
        else:
            row.prop(brush, "strength", slider=True, text="Hardness")
        row.prop(brush, "use_pressure_strength", toggle=True, text="")

#   BRUSH AUTOSMOOTH SLIDER
    def draw_slider_brushSmooth(self, brush, capabilities):
        split = self.layout.split()
        col = split.column()
        row = col.row(align=True)
        # auto_smooth_factor and use_inverse_smooth_pressure
        row.ui_units_x = 6
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
    def draw_strokeMethod(self, brush):
        row = self.layout.row(align=True)
        row.ui_units_x = 4
        row.prop(brush, "stroke_method", text="")

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
        col = self.layout.column(align=True)
        row = col.row(align=True)
        row.operator("brush.curve_preset", icon='SMOOTHCURVE', text="").shape = 'SMOOTH'
        row.operator("brush.curve_preset", icon='SPHERECURVE', text="").shape = 'ROUND'
        row.operator("brush.curve_preset", icon='ROOTCURVE', text="").shape = 'ROOT'
        row.operator("brush.curve_preset", icon='SHARPCURVE', text="").shape = 'SHARP'
        row.operator("brush.curve_preset", icon='LINCURVE', text="").shape = 'LINE'
        row.operator("brush.curve_preset", icon='NOCURVE', text="").shape = 'MAX'

#   FRONT FACES ONLY (TOGGLE)
    def draw_frontFaces(self, brush, icon):
        split = self.layout.split()
        col = split.column()
        col = col.row(align=True)
        col.prop(brush, "use_frontface", text="", icon_value=icon.icon_id)

#   MASK SETTINGS / INVERT / CLEAR
    def draw_maskSettings(self, icon_mask, icon_maskInvert, icon_maskClear):
        # MASK MENU
        row = self.layout.row(align=True)
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
                    # A menor nivel, mayor detalle, es decir para detalles más pequeños
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_6", text="1") # Botón 1, primer nivel, nivel más alto de detalle
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_5", text="2")
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_4", text="3")
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_3", text="4")
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_2", text="5")
                    row.operator("nsmui.ht_toolheader_dyntopo_lvl_1", text="6") # Botón 6, último nivel, nivel más bajo de detalle
                    
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
        sub.popover(panel="NSMUI_PT_th_settings",icon='VISIBLE_IPO_ON',text="")

#   PREFERENCES PANEL
    def draw_toggle_preferences(self):
        sub = self.layout.split().column(align=True)
        sub.popover(panel="NSMUI_PT_Prefs",icon='PREFERENCES',text="")
# --------------------------------------------- #
# HEADER UI
# --------------------------------------------- #
class NSMUI_HT_header_sculpt(bpy.types.Header):
    bl_idname = "NSMUI_HT_Header_Sculpt"
    bl_label = "Header Toolbar for Sculpt Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"
    bl_context = ".paint_common"

    def draw(self, context):
        layout = self.layout
        tool_mode = context.mode
        if(tool_mode == "SCULPT"):
            pcoll = preview_collections["main"]
            row = layout
            temp = False
            if(bpy.context.space_data.show_region_tool_header == False):
                if(temp == False):
                    icon = pcoll["arrowDown_icon"]
                else:
                    icon = pcoll["arrowUp_icon"]
                row.operator('nsmui.ot_header_tool_toggle', text="New Sculpt-Mode UI", icon_value=icon.icon_id) # id del operador, texto para el botón
                return None
            else:
                if(temp == False):
                    icon = pcoll["arrowUp_icon"]
                else:
                    icon = pcoll["arrowDown_icon"]
                row.operator('nsmui.ot_header_tool_toggle', text="", icon_value=icon.icon_id)            

# --------------------------------------------- #
# DYNTOPO STAGES UI PANEL
# --------------------------------------------- #
class NSMUI_PT_dyntopo_stages(Panel):
    bl_label = "DyntopoStages"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_category = 'Sculpt'
    bl_label = "Dyntopo Stages"
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
                self.layout.label(text="Values :") # Valores para el 'Stage' Activo
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

#################################################
#   REGISTRATION !!!!                      #
#################################################

from . import auto_load
auto_load.init()

def register():
    # UNREGISTER ORIGINAL TOOL HEADER # changed - antes al inicio del script
    try:
        bpy.utils.unregister_class(VIEW3D_HT_tool_header)
    except:
        pass

    # Register Classes
    register_class(NSMUI_HT_toolHeader_sculpt) # TOOL HEADER - SCULPT MODE
    register_class(NSMUI_HT_header_sculpt)     # HEADER      - SCULPT MODE
    register_class(NSMUI_PT_dyntopo_stages)

    # AutoLoad Exterior Classes
    auto_load.register()

    # Register Collections (ICONS)
    pcoll = bpy.utils.previews.new()
    for key, f in icons.items():
        pcoll.load(key, path.join(icon_dir, f), 'IMAGE')
    preview_collections["main"] = pcoll

    # WM PROPERTIES
    wm = bpy.types.WindowManager
    wm.toggle_UI_elements = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_prefs = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_brush_customIcon = bpy.props.BoolProperty(default=False, update=update_property)
    wm.toggle_stages = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_brush_settings = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_brushAdd = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_brushRemove = bpy.props.BoolProperty(default=False, update=update_property)
    wm.toggle_brushReset = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_stroke_settings = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_stroke_method = bpy.props.BoolProperty(default=False, update=update_property)
    wm.toggle_falloff = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_falloff_curvePresets = bpy.props.BoolProperty(default=False, update=update_property)
    wm.toggle_sliders = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_slider_brushSize = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_slider_brushStrength = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_slider_brushSmooth = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_slider_spacing = bpy.props.BoolProperty(default=False, update=update_property)
    wm.toggle_dyntopo = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_mask = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_symmetry = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_texture_new = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_texture_open = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_dyntopo_detailing = bpy.props.EnumProperty(
        items=(
            ('RELATIVE', "Relative", ""),
            ('CONSTANT', "Constant", ""),
            ('BRUSH', "Brush", "")
        ),
        default='RELATIVE',
        update=update_dyntopo_detailing,
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
    )
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

    # AutoLoad Exterior Classes
    auto_load.unregister()

    # UnRegister Collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    # PROPERTIES
    wm = bpy.types.WindowManager
    del wm.toggle_UI_elements
    del wm.toggle_brush_customIcon
    del wm.toggle_sliders
    del wm.toggle_slider_brushSize
    del wm.toggle_slider_brushStrength
    del wm.toggle_slider_brushSmooth
    del wm.toggle_slider_spacing
    del wm.toggle_brush_settings
    del wm.toggle_brushAdd
    del wm.toggle_brushRemove
    del wm.toggle_brushReset
    del wm.toggle_stroke_settings
    del wm.toggle_stroke_method
    del wm.toggle_falloff
    del wm.toggle_falloff_curvePresets
    del wm.toggle_dyntopo
    del wm.toggle_mask
    del wm.toggle_symmetry
    del wm.toggle_texture_new
    del wm.toggle_texture_open
    del wm.toggle_dyntopo_detailing
    del wm.toggle_dyntopo_stage
    del wm.toggle_stages
    del wm.toggle_prefs

    print("Unregistered New Sculpt Mode UI")