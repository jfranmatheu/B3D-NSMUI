import bpy
import os
from bpy.types import Panel, Operator

from bl_ui.properties_paint_common import (
        UnifiedPaintPanel,
        brush_texture_settings,
        brush_texpaint_common,
        brush_mask_texture_settings,
        brush_basic_sculpt_settings
        )
from bl_ui.utils import PresetPanel

class NSMUI_PT_th_settings(Panel):
    #bl_idname = "NSMUI_PT_Panel_TH_Settings"
    bl_label = "Toggle UI Elements"
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE" # Set it o ".paint_common" to see it on 'N' panel
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
            #row = self.layout.row()
            #row.label(text="Settings :")
            #row = self.layout.row(align=True)
            #row.prop(wm, 'toggle_UI_elements', text="Personalization", toggle=True)
            #row.prop(wm, 'toggle_prefs', text="Preferences", toggle=True)
            
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
        bl_context = "NONE" # Set it o ".paint_common" to see it on 'N' panel
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            scn = context.scene

            layout = self.layout
            layout.row().label(text="ADDON PREFS")
            box = layout.box()
            col = box.column()
            col.label(text="RMB Shortcut :")
            col.prop(scn, "deadzone_prop", text="Drag Threshold")
            col.prop(scn, "sens_prop", text="Sensibility")

            self.layout.separator()

            view = context.space_data

        # User prefs
            layout = self.layout
            layout.row().label(text="BLENDER QUICK PREFS")
            prefs  = context.preferences
            inputs = prefs.inputs
            view = prefs.view
            
            row = layout.row()
            flow = layout.grid_flow().box()

        # Navigation
            flow.label(text="NAVIGATION :")
            flow.row().prop(inputs, "view_rotate_method", expand=True)
            flow.prop(inputs, "use_rotate_around_active")
            flow.prop(inputs, "use_zoom_to_mouse")
            flow.prop(inputs, "use_mouse_depth_navigate")
            flow.prop(inputs, "use_auto_perspective")

            self.layout.separator()
        # Inputs
            #self.layout.label(text="INPUTS :")
            flow = layout.grid_flow().box()
            flow.label(text="INPUTS :")
            flow.prop(inputs, "drag_threshold_tablet")
            flow.prop(inputs, "pressure_softness", text="Pressure Softness")

        # View
            self.layout.separator()
            #self.layout.label(text="INTERFACE :")
            #self.layout.prop(view, "use_mouse_over_open", text="Open Menus on Mouse Over")
            flow = layout.grid_flow().row(align=True).box()
            flow.label(text="INTERFACE :")
            flow.prop(view, "use_mouse_over_open", text="Open Menus on Mouse Over")
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
'''
#   'BRUSHES' PANEL VISIBILITY SETTINGS
class NSMUI_PT_brushes_visibility(Panel):
    bl_label = "Toggle UI Elements"
    bl_description = "Toggle UI Elements of Brushes Panel."
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        wm = context.window_manager
        row = self.layout.row()
        row.label(text="''Brushes'' PANEL :")
        row.prop(wm, 'toggle_PT_brushes_collapse', text="Collapse !", toggle=False)
        row = self.layout.row(align=True)
        row.prop(wm, 'toggle_PT_brushPreview', text="Preview", toggle=True)
        row.prop(wm, 'toggle_PT_brushFavs', text="Favs", toggle=True)
        row.prop(wm, 'toggle_PT_brushType', text="Type", toggle=True)
'''
# BRUSHES MAIN PANEL
class NSMUI_PT_Brushes(Panel, UnifiedPaintPanel):
    bl_label = "Brushes"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    # bl_options = {'DEFAULT_CLOSED'}
    def draw(self, context):
        if(context.mode == "SCULPT"):
            scn = context.scene
            wm = context.window_manager

            layout = self.layout
            #sub = layout.column()
            #sub.popover(panel="NSMUI_PT_brushes_visibility", icon='HIDE_OFF', text="")
            row = self.layout.row(align=True)
            
            row.prop(wm, 'toggle_pt_brushes_collapse', icon='COLLAPSEMENU', text="", toggle=True)
            row.separator()
            #row.split()
            if not wm.toggle_pt_brushes_collapse:
                row.prop(wm, 'toggle_pt_brushPreview', icon='IMAGE_PLANE', text="", toggle=True)
                row.prop(wm, 'toggle_pt_brushFavs', icon='SOLO_ON', text="", toggle=True)
                row.prop(wm, 'toggle_pt_brushType', icon='IMGDISPLAY', text="", toggle=True)
            
            '''
            b = context.tool_settings.sculpt.brush.name
            from. import preview_collections
            pcoll = preview_collections["main"]
            icon_brushAdd = pcoll["brushAdd_icon"]
            icon_brushReset = pcoll["brushReset_icon"]
            icon_brushRemove = pcoll["brushRemove_icon"]

            row = self.layout.row()
        
            col = row.column(align=True)
            col.scale_y = 1.2
            col.scale_x = 1.2
            col.operator("brush.add", text="", icon_value=icon_brushAdd.icon_id) # DUPLICATE BRUSH
            col.operator("brush.reset", text="", icon_value=icon_brushReset.icon_id) # RESET BRUSH
            col.operator("nsmui.ht_toolheader_brush_remove", text="", icon_value=icon_brushRemove.icon_id) # DELETE BRUSH
            col.operator("nsmui.ht_toolheader_brush_custom_icon", text="", icon='RESTRICT_RENDER_OFF') # RENDER CUSTOM ICON

            row = row.split()
        
            row.template_icon(icon_value=bpy.data.brushes[b].preview.icon_id, scale=5)
            '''
            if wm.toggle_pt_brushPreview:
                layout.use_property_decorate = False  # No animation.

                settings = self.paint_settings(context)
                brush = settings.brush
            
                layout.column().template_ID_preview(settings, "brush", cols=4, rows=7, hide_buttons=True)

            if wm.toggle_pt_brushes_collapse:
                popover_kw = {"space_type": 'VIEW_3D', "region_type": 'UI', "category": "Tool"}
                self.layout.popover_group(context=".paint_common", **popover_kw)

                #NSMUI_PT_Brushes_Favs.bl_context = ".paint_common"
                #NSMUI_PT_Brushes_ByType.bl_context = ".paint_common"
                #NSMUI_PT_Brushes_Favs.redraw()
                
            
            else:
                if wm.toggle_pt_brushFavs and wm.toggle_pt_brushType:
                    box = layout.box()
                    box.scale_y = 0.6
                    box.scale_x = 0.6
                    row = box.column().row()

                    if scn.show_brushes_fav:
                        row.prop(scn, "show_brushes_fav", icon="DOWNARROW_HLT", text="Favourites", emboss=False)
                        NSMUI_PT_Brushes_Favs.draw(self, context)
                    else:
                        row.prop(scn, "show_brushes_fav", icon="RIGHTARROW", text="Favourites", emboss=False)
                
                    box = layout.box()
                    box.scale_y = 0.6
                    box.scale_x = 0.6
                    row = box.column().row()

                    if scn.show_brushes_type:
                        row.prop(scn, "show_brushes_type", icon="DOWNARROW_HLT", text="Per Type", emboss=False)
                        NSMUI_PT_Brushes_ByType.draw(self, context)
                    else:
                        row.prop(scn, "show_brushes_type", icon="RIGHTARROW", text="Per Type", emboss=False)
                
                elif wm.toggle_pt_brushFavs and (not wm.toggle_pt_brushType):
                    layout.separator()
                    NSMUI_PT_Brushes_Favs.draw(self, context)

                elif (not wm.toggle_pt_brushFavs) and wm.toggle_pt_brushType:
                    layout.separator()
                    NSMUI_PT_Brushes_ByType.draw(self, context)
                     


# FAV BRUSHES
favBrushes = []
class NSMUI_PT_Brushes_Favs(NSMUI_PT_Brushes):
    bl_context = None
    bl_category = 'Favorites'
    # bl_options = {'DEFAULT_CLOSED'}
    

    @classmethod
    def poll(cls, context):
        return (context.paint_common is not None)

    def redraw():
        from bpy.utils import register_class, unregister_class
        try:
            unregister_class(NSMUI_PT_Brushes_Favs)
        except:
            pass
        NSMUI_PT_Brushes_Favs.bl_context = ".paint_common"
        try:
            register_class(NSMUI_PT_Brushes_Favs)
        except:
            pass
        

    def draw(self, context):
            
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
                #col = row.column() # define una fila
                #col.separator()
                col = self.layout.grid_flow()
                for b in favBrushes:
                    if b == brushName:
                        act = True
                    else:
                        act = False
                    #col.scale_y = 1.1
                    #col.scale_x = 1.1
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


class NSMUI_PT_Brushes_ByType(NSMUI_PT_Brushes):
    bl_context = "NONE"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
            brush = bpy.context.tool_settings.sculpt.brush
            #sculpt = context.tool_settings.sculpt
            col = self.layout.column() # define una fila
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

def update_property(self, context):
    if self:
        self = not self

def collapseBrushPanel(self, context):
    wm = context.window_manager
    if self:
        self = not self
    if wm.toggle_pt_brushes_collapse == True:
        NSMUI_PT_Brushes_Favs.bl_context = ".paint_common"
        
        NSMUI_PT_Brushes_ByType.bl_context = ".paint_common"
    else:
        NSMUI_PT_Brushes_Favs.bl_context = "NONE"
        NSMUI_PT_Brushes_ByType.bl_context = "NONE"


def register():
    bpy.types.Scene.show_brushes_fav = bpy.props.BoolProperty(name='Show Fav Brushes', default=True)
    bpy.types.Scene.show_brushes_type = bpy.props.BoolProperty(name='Show Per Type Bruhes', default=True)
    bpy.types.Scene.show_brushes_temp = bpy.props.BoolProperty(name='Show Recent Brushes', default=False)

    wm = bpy.types.WindowManager
    wm.toggle_pt_brushes_collapse = bpy.props.BoolProperty(default=False, update=collapseBrushPanel)
    wm.toggle_pt_brushPreview = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_pt_brushFavs = bpy.props.BoolProperty(default=True, update=update_property)
    wm.toggle_pt_brushType = bpy.props.BoolProperty(default=True, update=update_property)

    

def unregister():
    del bpy.types.Scene.show_brushes_fav
    del bpy.types.Scene.show_brushes_type
    del bpy.types.Scene.show_brushes_temp

    wm = bpy.types.WindowManager
    del wm.toggle_pt_brushes_collapse
    del wm.toggle_pt_brushPreview
    del wm.toggle_pt_brushFavs
    del wm.toggle_pt_brushType

# PREVIEWS CUSTOM ICONS # NOT USED NOW
'''

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


'''