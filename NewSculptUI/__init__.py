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
    "version" : (0, 2, 0),
    "location" : "View3D > Tool Header // View3D > 'N' Panel: Sculpt)",
    "warning" : "This version is still in development. ;)",
    "category" : "Generic"
}

# IMPORTS # NECESITA LIMPIEZA!!!
import os
import bpy 
import traceback
from bpy.types import Operator, AddonPreferences, Header, Panel, Brush, UIList, Menu, Texture, Scene
from bl_ui.utils import PresetPanel
import bpy.utils.previews
from os.path import dirname, join, abspath, basename
from bpy import context, types
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
dynStage_Low = DyntopoStage("SKETCH", relative_High, constant_Low, brush_High) # (por un fallo están al revés los HIGH/LOW)
dynStage_Mid = DyntopoStage("DETAILS", relative_Mid, constant_Mid, brush_Mid)
dynStage_High = DyntopoStage("POLISH", relative_Low, constant_High, brush_Low)
dyntopoStages = [dynStage_Low, dynStage_Mid, dynStage_High]
# GLOBAL VARS
dynStage_Active = 0 # 1 = SKETCH; 2 = DETAIL; 3 = POLISH; 0 = "NONE" # Por defecto ningún 'stage' está activado
dynMethod_Active = "NONE"
dynValues_ui = [3,6,9] # valores mostrados en la UI # DEFECTO # Cambiarán al cambiar de stage o detailing (method aquí)

# ----------------------------------------------------------------- #
#   SETTINGS FOR TOOL HEADER UI                                     #
# ----------------------------------------------------------------- #
class ToolHeader_Settings:
    def __init__(self, dyntopo=True, sliders = [], brush_Reset=True, brush_Remove=True):
        self.dyntopo = dyntopo
        self.sliders = sliders
        self.brush_Reset = brush_Reset
        self.brush_Remove = brush_Remove
    
    def __repr__(self):
        return "ToolHeader_Settings[%b, %b[], %b, %b]" % (self.dyntopo, self.sliders, self.brush_Reset, self.brush_Remove)
th_settings_sliders_default = [True, True, True]
th_settings_default = ToolHeader_Settings(True, th_settings_sliders_default, True, True)

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

            # IF THERE'S NO BRUSH, JUST STOP DRAWING
            if brush is None:
                return
            
            toolHeader.draw_brushManager(self, sculpt, pcoll["brushAdd_icon"],
                pcoll["brushReset_icon"], bpy.types.Scene.resetBrush_Active,
                pcoll["brushRemove_icon"], bpy.types.Scene.removeBrush_Active)
            
            toolHeader.draw_separator(self, pcoll)

            if (bpy.types.Scene.sliders_Active == True):
                toolHeader.draw_slider_brushSize(self, toolsettings, brush, ups)
                toolHeader.draw_slider_brushStrength(self, toolsettings, brush, ups)       
                toolHeader.draw_slider_brushSmooth(self, brush, capabilities)
                toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_brushSettings(self, pcoll["brush_icon"])
            toolHeader.draw_strokeSettings(self, pcoll["stroke_icon"])
            toolHeader.draw_fallOff(self, pcoll["fallOff_icon"])
            toolHeader.draw_frontFaces(self, brush, pcoll["frontFaces_icon"])

            toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_maskSettings(self, pcoll["mask_icon"], pcoll["maskInvert_icon"], pcoll["maskClear_icon"])
            toolHeader.draw_symmetry(self, sculpt, pcoll["mirror_icon"])

            toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_topologySettings(self, context, pcoll)
                    
            toolHeader.draw_separator(self, pcoll)

            toolHeader.draw_textureSettings(self, pcoll["texture_icon"], pcoll["textureNew_icon"], pcoll["textureOpen_icon"])
            toolHeader.draw_textureManager(self, brush, pcoll["texture_icon"])

            toolHeader.draw_separator(self, pcoll)
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

#   BRUSH SELECTOR // ADD / RESET // REMOVE
    def draw_brushManager(self, sculpt, icon_brushAdd, icon_brushReset, canReset, icon_brushRemove, canRemove):
        layout = self.layout
        row = layout.row(align=True)
        row.ui_units_x = 9
        # BRUSH LIST
        row.template_ID_preview(sculpt, "brush", new="brush.add", rows=3, cols=8, hide_buttons=True)
        # NEW BRUSH BUTTON (DUPLICATE)
        row.operator("brush.add", text="", icon_value=icon_brushAdd.icon_id)     
        # RESET BRUSH BUTTON
        if(canReset == True):
            row.ui_units_x = row.ui_units_x + 1
            row.operator("brush.reset", text="", icon_value=icon_brushReset.icon_id) # RESET BRUSH
        # DELETE BRUSH BUTTON
        if (canRemove == True):
            row.ui_units_x = row.ui_units_x + 1
            row.operator("brush.reset", text="", icon_value=icon_brushRemove.icon_id) # DELETE BRUSH

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
    def draw_topologySettings(self, context, pcoll):
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
                    break
        # SCULPT --> DYNAMIC TOPOLOGY
        # Si no hay multires y dyntopo está activado
        if ibool==False:
            dynStage_Active = bpy.types.Scene.dynStage_Active
            sub = self.layout.row(align=True)
            sub.popover(panel="VIEW3D_PT_sculpt_dyntopo", text="")
            if(context.sculpt_object.use_dynamic_topology_sculpting==True):
            # Si no hay ningún 'Stage' activado
                if dynStage_Active == 0:
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
            # Si hay stage
                else:
                    n = 0 # CHIVATO PARA EL STAGE
                    dynMethod_Active = bpy.context.scene.tool_settings.sculpt.detail_type_method # CARGAR VALOR DEL METODO ACTIVO
                    iconLow = pcoll["dyntopoLowDetail_icon"]
                    iconMid = pcoll["dyntopoMidDetail_icon"]
                    iconHigh = pcoll["dyntopoHighDetail_icon"]
                # LOOK FOR ACTUAL STAGE
                    if (dynStage_Active == 1): # SKETCH
                        n = 2
                    elif (dynStage_Active == 2): # DETAIL
                        n = 1
                    elif (dynStage_Active == 3): # POLISH
                        n = 0
                    
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
                    row.operator("nsmui.ht_toolheader_dyntopo_any", text="", icon_value=iconLow.icon_id).value = dynValues_ui[0] # LOW DETAIL
                    row.operator("nsmui.ht_toolheader_dyntopo_any", text="", icon_value=iconMid.icon_id).value = dynValues_ui[1] # MID DETAIL
                    row.operator("nsmui.ht_toolheader_dyntopo_any", text="", icon_value=iconHigh.icon_id).value = dynValues_ui[2] # HIGH DETAIL

#   TEXTURE SETTINGS (DROPDOWN) / NEW TEXTURE / OPEN IMAGE
    def draw_textureSettings(self, icon_texture, icon_textureNew, icon_textureOpen):
        layout = self.layout
        split = layout
        col = split.column()
        sub = col.column(align=True)
        sub.popover(panel="VIEW3D_PT_tools_brush_texture", icon_value=icon_texture.icon_id, text="")
        layout = self.layout
        split = layout.split()
        col = split.column()
        row = col.row(align=True)
        row = self.layout.row(align=True)
        row.operator("nsmui.ht_toolheader_new_texture", text="", icon_value=icon_textureNew.icon_id) # NEW TEXTURE
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

# --------------------------------------------- #
# HEADER UI
# --------------------------------------------- #
class NSMUI_HT_header_sculpt(bpy.types.Header):
    bl_idname = "NSMUI_HT_Header_Sculpt"
    bl_label = "Header Toolbar for Sculpt Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"

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
# DYNTOPO STAGES UI PANEL / OPERATOR
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
        dynStage_Active = bpy.types.Scene.dynStage_Active
        if(context.sculpt_object.use_dynamic_topology_sculpting == True):
            pcoll = preview_collections["main"]
            method = bpy.context.scene.tool_settings.sculpt.detail_type_method
            icon1 = pcoll["dyntopoRelative_icon"]
            icon2 = pcoll["dyntopoConstant_icon"]
            icon3 = pcoll["dyntopoBrush_icon"]
            icon4 = pcoll["dyntopoManual_icon"]
            icon_H = pcoll["dyntopoHighDetail_icon"]
            icon_M = pcoll["dyntopoMidDetail_icon"]
            icon_L = pcoll["dyntopoLowDetail_icon"]

        # STAGES - SKETCH - DETAIL - POLISH
            layout = self.layout
            row = layout.row(align=True)
            #s_dynStage = dynStage_toString(dynStage_Active)
            if dynStage_Active != 0:
                row.label(text="Stage :   " + dynStage_toString(dynStage_Active)) # Stages - Para niveles de Detalle especificados abajo
                row.operator("nsmui.ot_dyntopo_stages_change", text="", icon='LOOP_BACK').valor = 0 # EXIT STAGE, MAIN MODE
            else:
                row.label(text="Stage :   NONE")
            col = layout.column()
            row = col.row(align=True)
            row.operator("nsmui.ot_dyntopo_stages_change", text="SKETCH").valor = 1
            #props.valor: "LOW"
            row.operator("nsmui.ot_dyntopo_stages_change", text="DETAILS").valor = 2
            #props.valor = "MID"
            props = row.operator("nsmui.ot_dyntopo_stages_change", text="POLISH")
            props.valor = 3

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
            row.operator("nsmui.ht_toolheader_dyntopo_relative", text="Relative", icon_value=icon1.icon_id)
            row.operator("nsmui.ht_toolheader_dyntopo_constant", text="Constant", icon_value=icon2.icon_id)
            row.operator("nsmui.ht_toolheader_dyntopo_brush", text="Brush", icon_value=icon3.icon_id)

            if dynStage_Active != 0:
            # LOOK FOR ACTIVE STAGE
                n = 0
                if(dynStage_Active == 1):
                    n = 2
                elif(dynStage_Active == 2):
                    n = 1
                elif(dynStage_Active == 3):
                    n = 0
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

    # AÑADE TEXTO INFORMATIVO JUNTO AL DROPDOWN (FUERA)
    #def draw_header(self, context):
    #    row = self.layout.column(align=True)
    #    row.label(text="DYN")

class NSMUI_OT_dyntopo_stages_change(Operator):
    bl_idname = "nsmui.ot_dyntopo_stages_change"
    bl_label = "CosasCosasCosas"
    #valor: bpy.props.StringProperty(name="Valor", default="NONE")
    valor: bpy.props.IntProperty(name="Valor", default=0)
    #valor = "NONE"
    def execute(self, valor):
        #print(bpy.types.Scene.dynStage_Active)
        bpy.types.Scene.dynStage_Active = self.valor
        #print(bpy.types.Scene.dynStage_Active)
        #print(self.valor)
        if(dynMethod_Active == "RELATIVE"):
            dynValues_ui = dyntopoStages[valor].relative_Values
        elif(dynMethod_Active == "CONSTANT"):
            dynValues_ui = dyntopoStages[valor].constant_Values
        elif(dynMethod_Active == "BRUSH"):
            dynValues_ui = dyntopoStages[valor].brush_Values

        NSMUI_HT_toolHeader_sculpt.redraw()
        return {'FINISHED'}

# --------------------------------------------- #
# PROPERTIES                                    #
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
        min = 0,
        max = 3,
        get = get_dynStage,
        set = set_dynStage,
    )
# --------------------------------------------- #
#   SCULPTMODE > BRUSH > REMOVE BUTTON - TOOL HEADER SETTINGS
bpy.types.Scene.removeBrush_Active = bpy.props.BoolProperty(
        name="Dyn Stage",
        description = "Actual Stage for Dyntopo",
        default = False, 
    )
bpy.types.Scene.removeBrush_Active = False # Inicializar valor por defecto
#   SCULPTMODE > BRUSH > REMOVE BUTTON - TOOL HEADER SETTINGS
bpy.types.Scene.resetBrush_Active = bpy.props.BoolProperty()
bpy.types.Scene.resetBrush_Active = True # Inicializar valor por defecto
#   SCULPTMODE > SLIDERS - TOOL HEADER SETTINGS
bpy.types.Scene.sliders_Active = bpy.props.BoolProperty()
bpy.types.Scene.resetBrush_Active = True # Inicializar valor por defecto

# ------------------------------------------- #
#   FUNCIONES SUELTAS 
# ------------------------------------------- #
def dynStage_toString(_dynStage):
    s_dynStage =""
    if _dynStage == 1:
        s_dynStage = "SKETCH"
    elif _dynStage == 2:
        s_dynStage = "DETAIL"
    elif _dynStage == 3:
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
    register_class(NSMUI_OT_dyntopo_stages_change)
    register_class(NSMUI_PT_dyntopo_stages)

    # AutoLoad Exterior Classes
    auto_load.register()

    # Register Collections
    pcoll = bpy.utils.previews.new()
    for key, f in icons.items():
        pcoll.load(key, path.join(icon_dir, f), 'IMAGE')
    preview_collections["main"] = pcoll

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
    unregister_class(NSMUI_OT_dyntopo_stages_change)
    unregister_class(NSMUI_PT_dyntopo_stages)

    # AutoLoad Exterior Classes
    auto_load.unregister()

    # UnRegister Collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    print("Unregistered New Sculpt Mode UI")