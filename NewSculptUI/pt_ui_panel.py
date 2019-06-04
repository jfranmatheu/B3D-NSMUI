import bpy

from bpy.types import Panel

class NSMUI_PT_th_settings(Panel):
    bl_idname = "NSMUI_PT_Panel_TH_Settings"
    bl_label = "Toggle UI Elements"
    bl_category = 'Sculpt'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if(context.mode != "SCULPT"):
            row = self.layout.row() # define una fila
            row.operator('nsmui.ot_panel_setup', text="Sculpt-Mode Setup") # id del operador, texto para el botón
        else:
            row = self.layout.row(align=True)
            row.operator('nsmui.ot_setting_brush_remove', text="Remove Brush") # id del operador, texto para el botón
            row.operator('nsmui.ot_setting_brush_reset', text="Reset Brush") # id del operador, texto para el botón
            row = self.layout.row(align=True)
            row.operator('nsmui.ot_setting_sliders', text="Sliders")

# CLASS FROM ADDON "Orbit" by LiquidBleu
# https://github.com/LiquideBleu/Orbit
class NSMUI_PT_Orbit_Prefs(bpy.types.Panel):
        bl_idname = "NSMUI_PT_Panel_Orbit_Prefs"
        bl_label = "Orbit Preferences"
        bl_space_type = 'VIEW_3D'
        bl_region_type = 'UI'
        bl_category = 'Sculpt'
        bl_options = {'DEFAULT_CLOSED'}

        def draw(self, context):
            layout = self.layout
            view = context.space_data
            
        # User preferences
            prefs  = context.preferences
            inputs = prefs.inputs
            
            row = layout.row()
            flow = layout.grid_flow()

        # Navigation
            flow.row().prop(inputs, "view_rotate_method", expand=True)
            flow.prop(inputs, "use_rotate_around_active")
            flow.prop(inputs, "use_mouse_depth_navigate")
            flow.prop(inputs, "use_zoom_to_mouse")
            flow.prop(inputs, "use_auto_perspective")