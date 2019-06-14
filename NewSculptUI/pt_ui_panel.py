import bpy

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
    # bl_options = {'DEFAULT_CLOSED'}
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
                if(b.sculpt_tool == brush.sculpt_tool):
                    col.operator('nsmui.ot_change_brush', text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name

    