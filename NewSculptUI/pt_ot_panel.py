import bpy

class NSMUI_OT_panel_setup(bpy.types.Operator):
    bl_idname = "nsmui.ot_panel_setup"
    bl_label = "change_ui_for_new_sculpt_mode"
    bl_description = "Setup New Sculpt Mode UI"
    def execute(self, context):
        blendfile = "./ws/NewSMUI_Workspace.blend"
        section   = "/Workspaces/"
        object    = "Sculpt"
        
        path  = blendfile + section + object
        direc = blendfile + section
        workspace  = object

        # CANCELS ANIMATION AND RESET FRAME POSITION
        #bpy.ops.spcreen.animation_cancel(restore_frame=True)

        # APPEND OF CUSTOM WORKSPACE
        

        # CHANGE TO 'SCULPTING' WORKSPACE
        bpy.context.window.workspace = bpy.data.workspaces["Sculpting"]
        # bpy.ops.workspace.add() # add or duplicate

        
        if(bpy.context.object.mode == "SCULPT"):
            # SHOW TOOL SETTINGS HEADER AND HEADER
            bpy.context.space_data.show_region_header = True        # bpy.types.SpaceView3D.show_region_header

            if(bpy.context.space_data.show_region_tool_header == False):
                bpy.context.space_data.show_region_tool_header = True # bpy.types.SpaceView3D.show_region_tool_header
            
            # SHADING TYPE FOR SCULPTING
            # bpy.data.screens["Sculpting"].shading.type = 'SOLID'

        # CHANGE TO SCULPT MODE # NO NEED --> SCULPTING WORKSPACE JUST DO IT
        else:    
            # bpy.ops.object.mode_set(mode='SCULPT') # ESTABLECE, ACTIVA
            bpy.ops.sculpt.sculptmode_toggle() # ACTIVA / DESACTIVA
        return {'FINISHED'}

class NSMUI_OT_change_brush(bpy.types.Operator):
    bl_idname = "nsmui.ot_change_brush"
    bl_label = "change_ui_for_new_sculpt_mode"
    bl_description = "Change actual brush to selected one."
    nBrush: bpy.props.StringProperty()

    def execute(self, nbrush):
        bpy.context.tool_settings.sculpt.brush = bpy.data.brushes[self.nBrush]
        return {'FINISHED'}

