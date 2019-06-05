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
            self.layout.label(text="TOGGLE UI ELEMENTS !")
            wm = context.window_manager
            row = self.layout.row(align=True)
            row.label(text="Brush :")
            row.prop(wm, 'toggle_brushAdd', text="Add", toggle=True)
            row.prop(wm, 'toggle_brushRemove', text="Remove", toggle=True)
            row.prop(wm, 'toggle_brushReset', text="Reset", toggle=True)

            row = self.layout.row(align=True)
            row.label(text="Sliders :")
            row.prop(wm, 'toggle_sliders', text="All Sliders", toggle=False) # si es false, el toggle es un checkbox
            row = self.layout.row(align=True)
            row.prop(wm, 'toggle_slider_brushSize', text="Size", toggle=True)
            row.prop(wm, 'toggle_slider_brushStrength', text="Strength", toggle=True)
            row.prop(wm, 'toggle_slider_brushSmooth', text="Smooth", toggle=True)

            row = self.layout.row()
            row.prop(wm, 'toggle_mask', text="Mask", toggle=False)
            row.prop(wm, 'toggle_symmetry', text="Symmetry", toggle=False)
            row = self.layout.row()
            row.prop(wm, 'toggle_dyntopo', text="Dyntopo", toggle=False)

            row = self.layout.row()
            row.label(text="Texture Settings :")
            row = self.layout.row(align=True)
            row.prop(wm, 'toggle_texture_new', text="New Texture", toggle=True)
            row.prop(wm, 'toggle_texture_open', text="Open Image", toggle=True)

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