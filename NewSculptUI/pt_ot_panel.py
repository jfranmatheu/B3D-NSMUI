import bpy

class NSMUI_OT_panel_brush_remove(bpy.types.Operator):
    bl_idname = "nsmui.ot_brush_remove"
    bl_label = "Remove Brush Checkbox"
    bl_description = ""

    # bpy.ops.wm.append(idname=filename, filepath=directory)
    # bpy.ops.workspace.append_activate(idname=filename, filepath=directory)

    def execute(self, context):
        from . import b_Brush_Remove
        if (b_Brush_Remove == True):
            b_Brush_Remove = False
        else:
            b_Brush_Remove = True
        from . import NSMUI_HT_toolHeader_sculpt as TH
        TH.redraw()
        return {'FINISHED'}

class NSMUI_OT_panel_brush_reset(bpy.types.Operator):
    bl_idname = "nsmui.ot_brush_reset"
    bl_label = "Reset Brush Checkbox"
    bl_description = ""

    # bpy.ops.wm.append(idname=filename, filepath=directory)
    # bpy.ops.workspace.append_activate(idname=filename, filepath=directory)

    def execute(self, context):
        from . import b_Brush_Reset
        if (b_Brush_Reset == True):
            b_Brush_Reset = False
        else:
            b_Brush_Reset = True
        from . import NSMUI_HT_toolHeader_sculpt as TH
        TH.redraw()
        return {'FINISHED'}


class NSMUI_OT_panel_setup(bpy.types.Operator):
    bl_idname = "nsmui.ot_panel_setup"
    bl_label = "change_ui_for_new_sculpt_mode"
    bl_description = ""

    # bpy.ops.wm.append(idname=filename, filepath=directory)
    # bpy.ops.workspace.append_activate(idname=filename, filepath=directory)

    def execute(self, context):
        blendfile = "./ws/NewSMUI_Workspace.blend"
        section   = "/Workspaces/"
        object    = "Sculpt"
        
        path  = blendfile + section + object
        direc = blendfile + section
        workspace  = object

        # CANCELS ANIMATION AND RESET FRAME POSITION
        #bpy.ops.spcreen.animation_cancel(restore_frame=True)

        # CHANGE PREFERENCES - INPUTS
        #bpy.types.PreferencesInput.use_zoom_to_mouse = True
        #bpy.types.PreferencesInput.use_mouse_depth_navigate = True
        #bpy.types.PreferencesInput.use_auto_perspective = True
        #bpy.types.PreferencesInput.use_rotate_around_active = True

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