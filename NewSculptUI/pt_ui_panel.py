import bpy
import os
from bpy.types import Panel, Operator

class NSMUI_PT_th_settings(Panel):
    #bl_idname = "NSMUI_PT_Panel_TH_Settings"
    bl_label = "Toggle UI Elements"
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if(context.mode != "SCULPT"):
            row = self.layout.row() # define una fila
            row.operator('nsmui.ot_panel_setup', text="Sculpt-Mode Setup") # id del operador, texto para el botón
        else:
            wm = context.window_manager

            row = self.layout.row()
            row.label(text="Customize your UI !")
            row.separator()

        #   BRUSH MANAGER
            row = self.layout.row(align=True)
            row.label(text="Brush :")
            row.prop(wm, 'toggle_brush_menu', text="Collapse !", toggle=False)

            if not wm.toggle_brush_menu:
                row = self.layout.row(align=True)
                row.prop(wm, 'toggle_brushAdd', text="Add", toggle=True)
                row.prop(wm, 'toggle_brushRemove', text="Remove", toggle=True)
                row.prop(wm, 'toggle_brushReset', text="Reset", toggle=True)
                row = self.layout.row()
                row.prop(wm, 'toggle_brush_customIcon', text="Render Custom Brush Icon", toggle=True)

        #   SLIDERS
            row = self.layout.row(align=True)
            row.label(text="Sliders :")
            row.prop(wm, 'toggle_sliders', text="Hide All !", toggle=False) # si es false, el toggle es un checkbox
            if not wm.toggle_sliders: # SI NO ESTÁN OCULTOS
                row = self.layout.row(align=True)
                row.prop(wm, 'toggle_slider_brushSize', text="Size", toggle=True)
                row.prop(wm, 'toggle_slider_brushStrength', text="Strength", toggle=True)
                row.prop(wm, 'toggle_slider_brushSmooth', text="Smooth", toggle=True)
                row = self.layout.row()
                row.prop(wm, 'toggle_slider_spacing', text="Spacing", toggle=True)
        
        #   SETTINGS // BRUSH // STROKE // FALLOFF (CURVES)
            row = self.layout.row()
            row.label(text="Dropdowns :")
            row = self.layout.row(align=True)
            row.prop(wm, 'toggle_brush_settings', text="Brush", toggle=True)
            row.prop(wm, 'toggle_stroke_settings', text="Stroke", toggle=True)
            row.prop(wm, 'toggle_falloff', text="Falloff", toggle=True)
            row = self.layout.row(align=True)
            row.label(text="Others :")

        #   BRUSH / STROKE / FALLOFF SETTINGS
            row = self.layout.row(align=True)
            row.prop(wm, 'toggle_stroke_method', text="Stroke Method", toggle=True)
            row.prop(wm, 'toggle_falloff_curvePresets', text="Curve Presets", toggle=True)

        #   OTHERS
            row = self.layout.row()
            row.prop(wm, 'toggle_mask', text="Mask", toggle=False)
            row.prop(wm, 'toggle_symmetry', text="Symmetry", toggle=False)
            row = self.layout.row()
            row.prop(wm, 'toggle_dyntopo', text="Dyntopo", toggle=False)

        #   TEXTURE SETTINGS
            row = self.layout.row()
            row.label(text="Texture Settings :")
            row = self.layout.row(align=True)
            row.prop(wm, 'toggle_texture_new', text="New Texture", toggle=True)
            row.prop(wm, 'toggle_texture_open', text="Open Image", toggle=True)

        #   DROPDOWN PANEL SETTINGS / VISIBILITY AND PREFERENCES
            row = self.layout.row()
            row.label(text="Settings :")
            row = self.layout.row(align=True)
            row.prop(wm, 'toggle_UI_elements', text="Personalization", toggle=True)
            row.prop(wm, 'toggle_prefs', text="Preferences", toggle=True)

            #   PRESETS
            row.separator()
            row = self.layout.row()
            box = self.layout.box()
            row = box.row()
            row.label(text="UI PRESETS :")
            row = box.row()
            row.operator('nsmui.ht_toolheader_ui_preset_default', text="Default")
            row = box.row()
            row.operator('nsmui.ht_toolheader_ui_preset_recommendation', text="Recommendation")
            row = box.row()
            row.label(text="Custom Preset Coming Soon!")
            
            
class NSMUI_PT_Prefs(bpy.types.Panel):
        # bl_idname = "NSMUI_PT_Panel_Prefs"
        bl_label = "Quick Preferences"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Sculpt'
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            layout = self.layout
            view = context.space_data
            
        # User prefs
            prefs  = context.preferences
            inputs = prefs.inputs
            view = prefs.view
            
            row = layout.row()
            flow = layout.grid_flow()

        # Navigation
            flow.label(text="NAVIGATION :")
            flow.row().prop(inputs, "view_rotate_method", expand=True)
            flow.prop(inputs, "use_rotate_around_active")
            flow.prop(inputs, "use_zoom_to_mouse")
            flow.prop(inputs, "use_mouse_depth_navigate")
            flow.prop(inputs, "use_auto_perspective")

            self.layout.separator()
        # Inputs
            self.layout.label(text="INPUTS :")
            flow = layout.grid_flow()
            flow.prop(inputs, "drag_threshold_tablet")
            flow.prop(inputs, "pressure_softness", text="Pressure Softness")

        # View
            self.layout.separator()

            self.layout.label(text="INTERFACE :")
            self.layout.prop(view, "use_mouse_over_open", text="Open Menus on Mouse Over")
            flow = layout.grid_flow().row(align=True)
            flow.prop(view, "open_toplevel_delay", text="Delay")
            flow.prop(view, "open_sublevel_delay", text="Sub Delay")


# RECENT BRUSHES
recentBrushes = []
class NSMUI_PT_Brushes_Recent(Panel):
    bl_label = "Recent Brushes"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        if(context.mode == "SCULPT"):
            activeBrush = bpy.context.tool_settings.sculpt.brush
            # RECENT BRUSHES
            length = len(recentBrushes)
            n = 6
            if length == 0: # or recentBrushes == [] # EMPTY LIST
                recentBrushes.append(activeBrush.name)
            elif length < n+1:
                if recentBrushes[length-1] == activeBrush.name:
                    pass
                elif length == n:
                    recentBrushes.pop(0)
                    recentBrushes.append(activeBrush.name)
                else:
                    recentBrushes.append(activeBrush.name)

            # print (length)
            # print(recentBrushes)

            col = self.layout.column() # define una fila
            for b in reversed(recentBrushes):
                # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                col.operator('nsmui.ot_change_brush', text=b, icon_value=bpy.data.brushes[b].preview.icon_id).nBrush = b

# RECENT BRUSHES
favBrushes = []
class NSMUI_PT_Brushes_Favs(Panel):
    bl_label = "Favourite Brushes"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    # bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        if(context.mode == "SCULPT"):
            activeBrush = bpy.context.tool_settings.sculpt.brush
            # RECENT BRUSHES
            length = len(favBrushes)

            row = self.layout.row(align=True)
            brushName = activeBrush.name
            row.operator('nsmui.ot_brush_fav_add', text="ADD", icon='ADD').nBrush = brushName
            row.operator('nsmui.ot_brush_fav_remove', text="REMOVE", icon='REMOVE').nBrush = brushName
            row = self.layout.row()
            # print (length)
            # print(recentBrushes)

            if length != 0:
                col = row.column() # define una fila
                col.separator()
                for b in favBrushes:
                    if b == brushName:
                        act = True
                    else:
                        act = False
                    col.scale_y = 1.1
                    col.scale_x = 1.1
                    # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    col.operator('nsmui.ot_change_brush', depress=act, text=b, icon_value=bpy.data.brushes[b].preview.icon_id).nBrush = b

class NSMUI_OT_brush_fav_remove(bpy.types.Operator):
    bl_idname = "nsmui.ot_brush_fav_remove"
    bl_label = "Remove Fav Brush"
    bl_description = "Remove Active Brush from Favourites."
    nBrush: bpy.props.StringProperty()
    def execute(self, nbrush):
        try:
            favBrushes.remove(self.nBrush)
        except:
            pass
        return {'FINISHED'}
class NSMUI_OT_brush_fav_add(bpy.types.Operator):
    bl_idname = "nsmui.ot_brush_fav_add"
    bl_label = "Add Fav Brush"
    bl_description = "Add Active Brush to Favourites."
    nBrush: bpy.props.StringProperty()
    def execute(self, nBrush):
        if self.nBrush in favBrushes:
            return {'FINISHED'}
        else:
            favBrushes.append(self.nBrush)
        return {'FINISHED'}


class NSMUI_PT_Brushes_ByType(Panel):
    #bl_idname = "NSMUI_PT_Panel_TH_RecentBrushes"
    bl_label = "Brushes by Type"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if(context.mode == "SCULPT"):
            brush = bpy.context.tool_settings.sculpt.brush
            #sculpt = context.tool_settings.sculpt
            col = self.layout.column() # define una fila
            col.label(text="BRUSHES")
            # BRUSH LIST
            for b in bpy.data.brushes:
                if (b.sculpt_tool == brush.sculpt_tool) and (not b.use_paint_vertex) and (b.use_paint_sculpt):
                    icon = bpy.data.brushes[b.name].preview
                    if b.name == brush.name:
                        act = True
                    else:
                        act = False
                    #icon.icon_size = (2,2)
                    col.scale_y = 1.1
                    col.scale_x = 1.1
                    col.operator('nsmui.ot_change_brush', depress=act, text=b.name, icon_value=icon.icon_id).nBrush = b.name


def enum_previews_from_directory_items(self, context):
    """EnumProperty callback"""
    enum_items = []

    if context is None:
        return enum_items

    wm = context.window_manager
    directory = wm.my_previews_dir

    # Get the preview collection (defined in register func).
    pcol = preview_collections["main"]

    if directory == pcol.my_previews_dir:
        return pcol.my_previews

    print("Scanning directory: %s" % directory)

    if directory and os.path.exists(directory):
        # Scan the directory for png files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)

        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            icon = pcol.get(name)
            if not icon:
                thumb = pcol.load(name, filepath, 'IMAGE')
            else:
                thumb = pcol[name]
            enum_items.append((name, name, "", thumb.icon_id, i))

    pcol.my_previews = enum_items
    pcol.my_previews_dir = directory
    return pcol.my_previews 



class PreviewsTestPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Custom Icon Previews [Test]"
    bl_idname = "BRUSH_PT_previews"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        row = layout.row()
        row.prop(wm, "my_previews_dir")

        row = layout.row()
        row.template_icon_view(wm, "my_previews")

        row = layout.row()
        row.prop(wm, "my_previews")
        #row.operator("my_previews")


# We can store multiple preview collections here,
# however in this example we only store "main"
preview_collections = {}

script_file = os.path.realpath(__file__)
addon_dir = os.path.dirname(script_file) # ADDON'S DIRECTORY
icons_folder = "/icons/"
icons_dir = addon_dir + "/Sculpt_Brushes" + icons_folder

def register():
    from bpy.types import WindowManager
    from bpy.props import (
        StringProperty,
        EnumProperty,
    )

    WindowManager.my_previews_dir = StringProperty(
        name="Folder Path",
        subtype='DIR_PATH',
        default=icons_dir
    )

    WindowManager.my_previews = EnumProperty(
        items=enum_previews_from_directory_items,
    )

    # Note that preview collections returned by bpy.utils.previews
    # are regular Python objects - you can use them to store custom data.
    #
    # This is especially useful here, since:
    # - It avoids us regenerating the whole enum over and over.
    # - It can store enum_items' strings
    #   (remember you have to keep those strings somewhere in py,
    #   else they get freed and Blender references invalid memory!).
    import bpy.utils.previews
    pcol = bpy.utils.previews.new()
    pcol.my_previews_dir = ""
    pcol.my_previews = ()

    preview_collections["main"] = pcol


def unregister():
    from bpy.types import WindowManager

    del WindowManager.my_previews

    for pcol in preview_collections.values():
        bpy.utils.previews.remove(pcol)
    preview_collections.clear()


if __name__ == "__main__":
    register()