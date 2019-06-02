import bpy

from bpy.types import Panel

class NSMUI_PT_panel(Panel):
    bl_idname = "NSMUI_PT_Panel"
    bl_label = "New Sculpt-Mode UI"
    #bl_category = "Test Addon"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    #bl_context = "SCULPT"

    def draw(self, context):

        if(context.mode != "SCULPT"):
            layout = self.layout
            row = layout.row() # define una fila
            row.operator('nsmui.ot_panel_setup', text="Sculpt-Mode Setup") # id del operador, texto para el botón

        
        #row = self.layout.column(align=True)
        #row = layout.row(align=True)

        # AÚN POR FIXEAR
        #row.operator('nsmui.ot_brush_remove', text="Activate Remove Brush Button")
        #row.operator('nsmui.ot_brush_reset', text="Activate Reset Brush Button")

