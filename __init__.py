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
    "description" : "New UI for Sculpt Mode",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 2),
    "location" : "View3D",
    "warning" : "This version is still in development.",
    "category" : "Generic"
}


# IMPORTS # NECESITA LIMPIEZA!!!
import os
import bpy 
import traceback
from bpy.types import Operator, AddonPreferences, Header, Panel, Brush, UIList, Menu, Texture
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

from bpy.utils import register_class, unregister_class
unregister_class(VIEW3D_HT_tool_header)


# ICONS // UI // COLLECTIONS
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
         "separator_icon" : "separator_icon.png",
         "arrowUp_icon"  : "arrowUp_icon.png",
         "arrowDown_icon" : "arrowDown_icon.png",
         "mask_icon"  : "mask_icon.png",
         "maskInvert_icon"  : "maskInvert_icon.png",
         "maskClear_icon"  : "maskClear_icon.png",
            }

# Panel
#from . ht_ui_header import NSMUI_HT_header # Now ON __init__.py
from . ht_ot_header import NSMUI_OT_header_tool_toggle, NSMUI_OT_header_tool_2
# Tool Header
# from . ht_ui_toolHeader import NSMUI_HT_toolHeader # Now ON __init__.py
from . ht_op_toolHeader import NSMUI_OT_toolHeader_symmetry_all
# Header
from . pt_ui_panel import NSMUI_PT_panel
from . pt_ot_panel import NSMUI_OT_panel_setup

# CLASSES (IMPORTED)
classes = (

    NSMUI_OT_header_tool_toggle, 
    NSMUI_OT_header_tool_2,

    NSMUI_OT_toolHeader_symmetry_all, 
    
    NSMUI_PT_panel,
    NSMUI_OT_panel_setup)

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
#   CLASSES -- UI --                            #
# --------------------------------------------- #

# VARIABLES GLOBALES PARA MENU DE AJUSTES #


# TOOL HEADER OVERRIDE # YA NO ES OVERRIDE, SE CAMBIO Y AHORA FUNCIONA MEJOR AUNQUE NO SE EVITA QUE LA UI ORIGINAL SE DIBUJE
# LOS ELEMENTOS SE SITÚAN EN POSICIÓN ANTERIOR A LOS DE LA CLASE NSMUI_HT_toolHeader DEL ADDON
# AQUÍ SE INCLUYEN TMB VERSIONES DEL TOOL HEADER PARA LOS DEMÁS MODOS
class VIEW3D_HT_tool_head(Header): #OVERRIDE
    bl_space_type = 'VIEW_3D'
    bl_region_type = "TOOL_HEADER"

    def draw(self, context):
        if context.mode != "SCULPT":
            layout = self.layout
            layout.row(align=True).template_header()

            if context.mode == "OBJECT": # SOME TEST
                layout = self.layout
                layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
                layout.operator("object.select_all", text="Inverse").action = 'INVERT'
                layout.operator("object.select_random", text="Random")

b_Brush_Reset = False # default
b_Brush_Remove = False # default
# SCULPT MODE UI - NEW TOOL HEADER
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
        # scene = context.scene
        # tool_mode = context.mode

        if(context.mode == "SCULPT"):
            layout = self.layout
            row = layout.row() # define una fila
            
        # COLLECTION OF ICONS
            pcoll = preview_collections["main"]

        # VARS
            brush = bpy.context.tool_settings.sculpt.brush
            sculpt = context.tool_settings.sculpt
            capabilities = brush.sculpt_capabilities
            toolsettings = context.tool_settings
            settings = self.paint_settings(context)
            brush = settings.brush
            ups = toolsettings.unified_paint_settings

        # BUTTON - CHANGE SPACE TYPE OF THE WINDOW 
            #layout = self.layout
            #layout.row(align=True).template_header()

    # SCULPT --> BRUSH SELECTOR / CREATE BRUSH / RENAME BRUSH
        # IF THERE'S NO BRUSH, JUST STOP DRAWING
            if brush is None:
                return
        # DEFAULT AND BASIC SCULPT SETTINGS -> RADIUS SLIDER + STRENGTH SLIDER + ADD/SUBSTRACT
            # brush_basic_sculpt_settings(layout, context, sculpt.brush, compact=True)
        # DEFAULT DROP_MENUS OF TOOL HEADER // Brush // Texture // Stroke // Falloff // Display //
            # layout.popover_group(space_type='VIEW_3D', region_type='UI', context=".paint_common", category="Tool")

            layout = self.layout
            row = layout.row(align=True)
            row.ui_units_x = 10
            # col.template_ID_preview(sculpt, "brush", new="brush.add", rows=7, cols=3, hide_buttons=True) # OLD ONE
        # BRUSH LIST
            row.template_ID_preview(sculpt, "brush", new="brush.add", rows=3, cols=8, hide_buttons=True)
        # NEW BRUSH BUTTON (DUPLICATE)
            icon = pcoll["brushAdd_icon"]
            row.operator("brush.add", text="", icon_value=icon.icon_id)     
            #icon = pcoll["brushReset_icon"]
        # RESET BRUSH BUTTON
            if(b_Brush_Reset == False):
                icon = pcoll["brushReset_icon"]
                row.operator("brush.reset", text="", icon_value=icon.icon_id) # RESET BRUSH
        # DELETE BRUSH BUTTON
            if (b_Brush_Remove == True):
                icon = pcoll["brushRemove_icon"]
                row.operator("brush.reset", text="", icon_value=icon.icon_id) # RESET BRUSH

            # row.prop(brush, "texture", toggle=True, text="") # dropdown lista de texturas en una fila

    # SPACING // SEPARATOR
            layout = self.layout
            split = layout.split()
            col = split.column()
            icon = pcoll["separator_icon"]
            col.label(text="", icon_value=icon.icon_id)

    # SCULPT --> SIZE
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

    # SCULPT STRENTH
            layout = self.layout
            split = layout.split()
            col = split.column()
            row = col.row(align=True)
            row.ui_units_x = 6

            if(toolsettings.unified_paint_settings.use_unified_strength): 
                row.prop(ups, "strength", slider=True, text="Hardness") # ups -> tool_settings.unified_paint_settings.strength
            else:
                row.prop(brush, "strength", slider=True, text="Hardness")
            row.prop(brush, "use_pressure_strength", toggle=True, text="")

    # SCULPT --> AUTOSMOOTH        

            layout = self.layout
            split = layout.split()
            col = split.column()
            row = col.row(align=True)

            # auto_smooth_factor and use_inverse_smooth_pressure
            row.ui_units_x = 6
            if (capabilities.has_auto_smooth):
                row.prop(brush, "auto_smooth_factor", slider=True, text="Smooth")
                row.prop(brush, "use_inverse_smooth_pressure", toggle=True, text="")

        # SPACING // SEPARATOR
            layout = self.layout
            split = layout.split()
            col = split.column()
            icon = pcoll["separator_icon"]
            col.label(text="", icon_value=icon.icon_id)

    # SCULPT --> BRUSH OPTIONS

            icon = pcoll["brush_icon"]
            layout = self.layout
            split = layout.split()
            col = split.column()
            col.alignment = 'CENTER'

            sub = col.column(align=True)
            sub.popover(
            panel="VIEW3D_PT_tools_brush",icon_value=icon.icon_id,text="")
            #VIEW3D_PT_sculpt_options_unified

    # SCULPT --> BRUSH - STROKE

            icon = pcoll["stroke_icon"]
            layout = self.layout
            split = layout.split()
            col = split.column()

            sub = col.column(align=True)
            sub.popover(
                panel="VIEW3D_PT_tools_brush_stroke",
                icon_value=icon.icon_id,
                text="")

    # SCULPT --> BRUSH - FALLOFF

            icon = pcoll["fallOff_icon"]
            layout = self.layout
            split = layout.split()
            col = split.column()
      
            sub = col.column(align=True)
            sub.popover(
                panel="VIEW3D_PT_tools_brush_falloff",
                icon_value=icon.icon_id,
                text="")

    # SCULPT --> FRONT FACES        

            icon = pcoll["frontFaces_icon"]
            layout = self.layout
            split = layout.split()
            col = split.column()
            col = col.row(align=True)
            col.prop(brush, "use_frontface", text="", icon_value=icon.icon_id)
                
        # SPACING // SEPARATOR
            layout = self.layout
            split = layout.split()
            col = split.column()
            icon = pcoll["separator_icon"]
            col.label(text="", icon_value=icon.icon_id)

    # MASK TOOLS
        # MASK MENU
            row = self.layout.row(align=True)
            icon = pcoll["mask_icon"]
            row.menu("VIEW3D_MT_hide_mask", text=" Mask ", icon_value=icon.icon_id)
        # MASK -> INVERT
            icon = pcoll["maskInvert_icon"]
            props = row.operator("paint.mask_flood_fill", text="", icon_value=icon.icon_id)
            props.mode = 'INVERT'
        # MASK -> CLEAR
            icon = pcoll["maskClear_icon"]
            props = row.operator("paint.mask_flood_fill", text="", icon_value=icon.icon_id)
            props.mode = 'VALUE'
            props.value = 0
            

    # SCULPT --> SYMMETRY TOOLS
            icon = pcoll["mirror_icon"]
            split = layout#.split()
        # MIRROR ICON
            col = split.column()
            #col.label(nsmui.ht_toolheader_symmetry_all, text="Mirror:", icon_value=icon.icon_id)

        # MIRRORS X, Y, Z
            col = split.column()
            row = col.row(align=True)
            row.ui_units_x = 5
            #row.label(nsmui.ht_toolheader_symmetry_all, text="", icon_value=icon.icon_id, toggle=True)
            row.operator("nsmui.ht_toolheader_symmetry_all", icon_value=icon.icon_id, text=" ")
            row.prop(sculpt, "use_symmetry_x", text="X", toggle=True)
            row.prop(sculpt, "use_symmetry_y", text="Y", toggle=True)
            row.prop(sculpt, "use_symmetry_z", text="Z", toggle=True)

        # SPACING // SEPARATOR
            layout = self.layout
            split = layout.split()
            col = split.column()
            icon = pcoll["separator_icon"]
            col.label(text="", icon_value=icon.icon_id)
    
    # SCULPT --> DYNAMIC TOPOLOGY

            #icon = pcoll["dyntopo_icon"]
            layout = self.layout
            split = layout
            col = split.column()
            row = col.row(align=True)
            
            sub = split
            sub.popover(
                panel="VIEW3D_PT_sculpt_dyntopo",
                #icon_value=icon.icon_id,
                text="")

        # DEFAULT VALUES FOR DETAIL SIZE
        # NOTe: THIS WILL CHANGE IN A MORE DYNAMIC AND CUSTOM WAY
            #row.label(nsmui.ht_toolheader_symmetry_all, text="", icon_value=icon.icon_id, toggle=True)
            row.ui_units_x = 6
            row.operator("nsmui.ht_toolheader_dyntopo_2", text="2")
            row.operator("nsmui.ht_toolheader_dyntopo_4", text="4")
            row.operator("nsmui.ht_toolheader_dyntopo_6", text="6")
            row.operator("nsmui.ht_toolheader_dyntopo_8", text="8")
            row.operator("nsmui.ht_toolheader_dyntopo_10", text="10")
            row.operator("nsmui.ht_toolheader_dyntopo_12", text="12")
        
        # SPACING // SEPARATOR
            layout = self.layout
            split = layout.split()
            col = split.column()
            icon = pcoll["separator_icon"]
            col.label(text="", icon_value=icon.icon_id)

        # SCULPT --> BRUSH TEXTURE TOOLS
           
            icon = pcoll["texture_icon"]
            layout = self.layout
            split = layout
            col = split.column()
            sub = col.column(align=True)
            sub.popover(panel="VIEW3D_PT_tools_brush_texture", icon_value=icon.icon_id, text="")

            icon = pcoll["textureNew_icon"]
            layout = self.layout
            split = layout.split()
            col = split.column()
            row = col.row(align=True)
            row = self.layout.row(align=True)
            row.operator("nsmui.ht_toolheader_new_texture", text="", icon_value=icon.icon_id) # NEW TEXTURE
            icon = pcoll["textureOpen_icon"]
            row.operator("image.open", text="", icon_value=icon.icon_id) # OPEN IMAGE TEXTURE
            
    # TEXTURES - QUICK SELECTOR
            texture = brush.texture
            icon = pcoll["texture_icon"]
            layout = self.layout
            col = layout
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
        ##
        
            # row.operator("image.reload", text="Reload")

            ####### NEXT ###########################
            ## tex = context.texture
            # layout.template_image(tex, "image", tex.image_user) # PARA VER Y SELECCIONAR LAS IMAGENES IMPORTADAS
            # self.layout.prop(tex, "use_color_ramp", text="") # COLOR RAMP PARA LA TEXTURA
            # self.layout.prop(tex, "use_alpha", text="") # BROCHA COMO ALPHA O NO
            # PREVIEW DE LA TEXTURA // SE USARA PARA PREVIEW DE LA TEXTURA EN EL 3DVIEWPORT AL HACER HOVER


            ## slot = getattr(context, "texture_slot", None)
            ## idblock = context_tex_datablock(context)
            # if idblock:
            #    layout.template_preview(tex, parent=idblock, slot=slot)
            # else:
            #    layout.template_preview(tex, slot=slot)

        # SPACING // SEPARATOR
            layout = self.layout
            split = layout.split()
            col = split.column()
            icon = pcoll["separator_icon"]
            col.label(text="", icon_value=icon.icon_id)
            layout = self.layout
            layout.separator(factor=40.0)
            
        else:
            return None

        try:
            #bpy.utils.unregister_class(VIEW3D_HT_tool_header)
            bpy.utils.register_class(VIEW3D_HT_tool_header)
        except:
            pass
        

    # SCULPT --> 

# SCULPT MODE UI - NEW HEADER
class NSMUI_HT_header_sculpt(bpy.types.Header):
    bl_idname = "NSMUI_HT_Header_Sculpt"
    bl_label = "Header Toolbar for Sculpt Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"

    def draw(self, context):

        layout = self.layout
        tool_mode = context.mode

        if(tool_mode == "SCULPT"):
            # COLLECTION OF ICONS
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
            

# PAINT MODE UI - NEW TOOL HEADER
class NSMUI_HT_toolHeader_paint(Header):
    bl_idname = "NSMUI_HT_ToolHeader_Paint"
    bl_label = "Header Toolbar for Paint Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOL_HEADER"

    def draw(self, context):

        if(context.mode == "PAINT_TEXTURE"):
            # COLLECTION OF ICONS
            pcoll = preview_collections["main"]

        # PAINT
            layout = self.layout
            row = layout.row() # define una fila            
            
# PAINT MODE UI - NEW HEADER
class NSMUI_HT_header_paint(bpy.types.Header):
    bl_idname = "NSMUI_HT_Header_Paint"
    bl_label = "Header Toolbar for Sculpt Mode"
    bl_space_type = "VIEW_3D"
    bl_region_type = "HEADER"

    def draw(self, context):

        layout = self.layout
        tool_mode = context.mode

        if(tool_mode == "PAINT_TEXTURE"):
            # COLLECTION OF ICONS
            pcoll = preview_collections["main"]

        # PAINT
            layout = self.layout

# --------------------------------------------- #

#   FACTORY REGISTRATION OF CLASSES 
#register, unregister = bpy.utils.register_classes_factory(classes)

#################################################
#   AUTO-REGISTRATION !!!!                             #
#################################################

from . import auto_load
auto_load.init()

def register():
    # Register Classes
    register_class(VIEW3D_HT_tool_head)      # OVERRITE CLASS
    register_class(NSMUI_HT_toolHeader_sculpt) # TOOL HEADER - SCULPT MODE
    register_class(NSMUI_HT_header_sculpt)     # HEADER      - SCULPT MODE
    register_class(NSMUI_HT_toolHeader_paint)  # TOOL HEADER - PAINT MODE
    register_class(NSMUI_HT_header_paint)      # HEADER      - PAINT MODE
    # AutoLoad Exterior Classes
    auto_load.register()
    # Register Collections
    pcoll = bpy.utils.previews.new()
    for key, f in icons.items():
        pcoll.load(key, path.join(icon_dir, f), 'IMAGE')
    preview_collections["main"] = pcoll
    

    print("Registered New Sculpt Mode UI")

def unregister():
    # UnRegister Classes
    unregister_class(VIEW3D_HT_tool_head)      # OVERRITE CLASS
    unregister_class(NSMUI_HT_toolHeader_sculpt) # TOOL HEADER - SCULPT MODE
    unregister_class(NSMUI_HT_header_sculpt)     # HEADER      - SCULPT MODE
    unregister_class(NSMUI_HT_toolHeader_paint)  # TOOL HEADER - PAINT MODE
    unregister_class(NSMUI_HT_header_paint)      # HEADER      - PAINT MODE
    # AutoLoad Exterior Classes
    auto_load.unregister()
    # UnRegister Collections
    for pcoll in preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

    print("Unregistered New Sculpt Mode UI")

