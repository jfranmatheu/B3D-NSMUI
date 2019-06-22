import bpy

from bpy.types import (
    Header,
    Menu,
    Panel,
)


class NSMUI_OT_header_tool_toggle(bpy.types.Operator):
    bl_idname = "nsmui.ot_header_tool_toggle"
    bl_label = "new_header_tools_for_sculpt_mode"
    bl_description = "Toggle New Tool Header"

    def execute(self, context):
        if (bpy.context.space_data.show_region_tool_header == True):
            bpy.context.space_data.show_region_tool_header = False
        
        elif (bpy.context.space_data.show_region_tool_header == False):
            bpy.context.space_data.show_region_tool_header = True

        elif (bpy.ops.screen.header_toggle_menus == True and bpy.context.space_data.show_region_tool_header == False):
            bpy.context.space_data.show_region_tool_header = True
            bpy.ops.screen.header_toggle_menus()
        
        elif (bpy.ops.screen.header_toggle_menus == False and bpy.context.space_data.show_region_tool_header == True):
           bpy.context.space_data.show_region_tool_header = False
           bpy.ops.screen.header_toggle_menus()
        
        bpy.ops.screen.header_toggle_menus()

        return {'FINISHED'}

class NSMUI_OT_header_tool_2(bpy.types.Operator):
    bl_idname = "nsmui.ot_header_tool_2"
    bl_label = "new_header_tools_for_sculpt_mode"
    bl_description = ""

    def execute(self, context):
        bpy.context.space_data.show_region_tool_header = False
        if(bpy.ops.screen.header_toggle_menus()==False):
            bpy.ops.screen.header_toggle_menus()
        return {'FINISHED'}