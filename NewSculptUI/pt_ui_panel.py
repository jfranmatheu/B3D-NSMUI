import bpy
import os
from bpy.types import Panel, Operator
import gpu
import bgl
from gpu_extras.batch import batch_for_shader

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
    bl_description = "Customize your interface toggling UI elements as your want!"

    def draw(self, context):
        if(context.mode != "SCULPT"):
            row = self.layout.row() # define una fila
            row.operator('nsmui.ot_panel_setup', text="Sculpt-Mode Setup") # id del operador, texto para el botón
        else:
            wm = context.window_manager

            row = self.layout.row()
            row.label(text="Customize here the Tool Header !")
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
                row.prop(wm, 'toggle_slider_brushSize', text="Radious", toggle=True)
                row.prop(wm, 'toggle_slider_brushStrength', text="Strength", toggle=True)
                row.prop(wm, 'toggle_slider_brushSmooth', text="Smooth", toggle=True)
                row = self.layout.row(align=True)
                row.prop(wm, 'toggle_slider_spacing', text="Spacing", toggle=True)
                row.prop(wm, 'toggle_slider_topoRake', text="Topo Rake", toggle=True)
                row = self.layout.row()
                row.prop(wm, 'toggle_slider_specificBrushType', text="Specifics per Brush Type", toggle=True)
                
        
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
        bl_description = "Quick addon + Blender preferences!"

        def draw(self, context):
            scn = context.scene
            wm = context.window_manager

            layout = self.layout
            #layout.use_property_split = True
            layout.use_property_decorate = False  # No animation.

            layout.row().label(text="ADDON PREFS")
            box = layout.box()
            col = box.column()
            col.label(text="RMB Shortcut :")
            col.prop(scn, "deadzone_prop", text="Drag Threshold")
            _row = col.row(align=True)
            _row.label(text="Font Size", icon='FONTPREVIEW')
            _row.prop(scn, "textDisplaySize", text="")
            _row = col.row(align=True)
            _row.prop(scn, "sens_prop", text="Sensibility")
            _row.prop(scn, "invertAxis", text="Invert Axis", icon='ORIENTATION_VIEW')

            self.layout.separator()

            box = layout.box()
            col = box.column()
            col.label(text="'BRUSHES' PANEL :")
            #col.label(, text="[Recent Brushes]")
            _row = col.row(align=True)
            _row.label(icon='IMAGE_PLANE', text="") # BRUSH_DATA
            _row.prop(scn, "show_brushOptionsWith", text="Show Brush Options", toggle = True) 
            _row = col.row(align=True)
            _row.label(icon='SOLO_OFF', text="") # LONGDISPLAY
            _row.prop(wm, "toggle_pt_brushShowOnlyIcons", text="Show Icons Only", toggle = True)
            _row = col.row(align=True)
            _row.label(icon='RECOVER_LAST', text="")
            _row.prop(scn, "recentBrushes_stayInPlace", text="Keep Brushes in Place", toggle = True)
            

            self.layout.separator()

            box = layout.box()
            col = box.column()
            col.label(text="OTHERS :")
            _row = col.row(align=True)
            _row.label(icon='TEXTURE_DATA', text="") # BRUSH_DATA
            _row.prop(scn, "drawBrushTexture", text="Draw Brush Texture", toggle = False) 

            self.layout.separator()

            view = context.space_data

        # User prefs
            layout.row().label(text="BLENDER QUICK PREFS")
            prefs  = context.preferences
            inputs = prefs.inputs
            view = prefs.view
            
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

            self.layout.separator()
        # View
            #self.layout.label(text="INTERFACE :")
            #self.layout.prop(view, "use_mouse_over_open", text="Open Menus on Mouse Over")
            flow = layout.grid_flow().row(align=True).box()
            flow.label(text="INTERFACE :")
            flow.prop(view, "use_mouse_over_open", text="Open Menus on Mouse Over")
            flow = flow.row(align=True)
            flow.prop(view, "open_toplevel_delay", text="Delay")
            flow.prop(view, "open_sublevel_delay", text="Sub Delay")

            self.layout.separator()

            flow = layout.grid_flow().box()
            flow.label(text="VIEW :")
            #flow.prop(view, "lens", text="Focal Length")
            view = context.space_data
            col = flow.column()
            subcol = col.column()
            subcol.active = bool(view.region_3d.view_perspective != 'CAMERA' or view.region_quadviews)
            subcol.prop(view, "lens", text="Focal Length")

            


# RECENT BRUSHES
recentBrushes = []
class NSMUI_PT_Brushes_Recent(Panel):
    bl_label = "Recent Brushes"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        if(context.mode == "SCULPT"):
            try:
                scn = context.scene
                activeBrush = context.tool_settings.sculpt.brush
                # RECENT BRUSHES
                length = len(recentBrushes)
                n = 6
                if length == 0: # or recentBrushes == [] # EMPTY LIST
                    recentBrushes.append(activeBrush)
                elif length < n+1:
                    if activeBrush in recentBrushes:
                        if not scn.recentBrushes_stayInPlace:
                            recentBrushes.remove(activeBrush)
                            recentBrushes.append(activeBrush)
                    elif length == n:
                        recentBrushes.pop(0)
                        recentBrushes.append(activeBrush)
                    else:
                        recentBrushes.append(activeBrush)
            except:
                pass
            # print (length)
            # print(recentBrushes)
            col = self.layout.column() # define una fila
            for b in reversed(recentBrushes):
                # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                col.operator('nsmui.ot_change_brush', text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name


from bpy.utils import register_class, unregister_class
# BRUSHES MAIN PANEL
class NSMUI_PT_Brushes(Panel, UnifiedPaintPanel):
    bl_label = "Brushes"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    # bl_options = {'DEFAULT_CLOSED'}

    def invoke(self, context):
        bpy.types.SpaceView3D.draw_handler_add(self.draw, (self, context), 'WINDOW', 'POST_PIXEL')


    def draw(self, context):
        if(context.mode == "SCULPT"):
            scn = context.scene

            wm = context.window_manager 

            try:
                sculpt = context.tool_settings.sculpt
                settings = self.paint_settings(context)
                
                brush = settings.brush
            except:
                pass
            

            layout = self.layout
            
            #sub = layout.column()
            #sub.popover(panel="NSMUI_PT_brushes_visibility", icon='HIDE_OFF', text="")
            row = layout.row()
            row.prop(wm, 'toggle_pt_brushes_collapse', icon='COLLAPSEMENU', text="", toggle=True)
            row.separator(factor=1)
            split = row.split(align=True)
            if wm.toggle_pt_brushes_collapse: enb = False
            else: enb = True
            
            #row = layout.row(align=True)
            split.enabled = enb
            split.prop(wm, 'toggle_pt_brushPreview', icon='IMAGE_PLANE', text="", toggle=True)
            split.prop(wm, 'toggle_pt_brushFavs', icon='SOLO_ON', text="", toggle=True)
            split.prop(wm, 'toggle_pt_brushType', icon='IMGDISPLAY', text="", toggle=True)
            split.prop(wm, 'toggle_pt_brushRecents', icon='RECOVER_LAST', text="", toggle=True)


            if wm.toggle_pt_brushPreview:
                layout.use_property_decorate = False  # No animation.
                settings = self.paint_settings(context)
                try:
                    brush = settings.brush
                
                    row = layout.row()
                    row.column().template_ID_preview(settings, "brush", cols=4, rows=7, hide_buttons=True)

                    if scn.show_brushOptionsWith:
                        from. import preview_collections
                        pcoll = preview_collections["main"]
                        icon_brushAdd = pcoll["brushAdd_icon"]
                        icon_brushReset = pcoll["brushReset_icon"]
                        icon_brushRemove = pcoll["brushRemove_icon"]

                        col = row.column(align=True)
                        col.scale_y = 1.5
                        col.scale_x = 1.3
                        col.operator("brush.add", text="", icon_value=icon_brushAdd.icon_id) # DUPLICATE BRUSH
                        col.operator("brush.reset", text="", icon_value=icon_brushReset.icon_id) # RESET BRUSH
                        col.operator("nsmui.ht_toolheader_brush_remove", text="", icon_value=icon_brushRemove.icon_id) # DELETE BRUSH
                        col.operator("nsmui.ht_toolheader_brush_custom_icon", text="", icon='RESTRICT_RENDER_OFF') # RENDER CUSTOM ICON
                except:
                    pass

            if wm.toggle_pt_brushes_collapse:
                try:
                    popover_kw = {"space_type": 'VIEW_3D', "region_type": 'UI', "category": "Tool"}
                    layout.popover_group(context=".paint_common", **popover_kw)
                except:
                    pass
      
            else:
                count = 0
                if wm.toggle_pt_brushFavs == True: count = count + 1
                if wm.toggle_pt_brushType == True: count = count + 1
                if wm.toggle_pt_brushRecents == True: count = count + 1
                #print(count)

                layout = self.layout
                
                if count > 1:
                    if wm.toggle_pt_brushFavs:
                        box = layout.box()
                        box.scale_y = 0.6
                        box.scale_x = 0.6
                        row = box.column().row()

                        if scn.show_brushes_fav:
                            row.prop(scn, "show_brushes_fav", icon="DOWNARROW_HLT", text="Favourites", emboss=False)
                            NSMUI_PT_Brushes_Favs.draw(self, context)
                        else:
                            row.prop(scn, "show_brushes_fav", icon="RIGHTARROW", text="Favourites", emboss=False)

                    if wm.toggle_pt_brushType:
                        box = layout.box()
                        box.scale_y = 0.6
                        box.scale_x = 0.6
                        row = box.column().row()

                        if scn.show_brushes_type:
                            row.prop(scn, "show_brushes_type", icon="DOWNARROW_HLT", text="Per Type", emboss=False)
                            NSMUI_PT_Brushes_ByType.draw(self, context)
                        else:
                            row.prop(scn, "show_brushes_type", icon="RIGHTARROW", text="Per Type", emboss=False)

                    if wm.toggle_pt_brushRecents:
                        box = layout.box()
                        box.scale_y = 0.6
                        box.scale_x = 0.6
                        row = box.column().row()

                        if scn.show_brushes_temp:
                            row.prop(scn, "show_brushes_temp", icon="DOWNARROW_HLT", text="Recent Brushes", emboss=False)
                            NSMUI_PT_Brushes_Recent.draw(self, context)
                        else:
                            row.prop(scn, "show_brushes_temp", icon="RIGHTARROW", text="Recent Brushes", emboss=False)
                
                elif wm.toggle_pt_brushFavs:
                    layout.separator()
                    NSMUI_PT_Brushes_Favs.draw(self, context)

                elif wm.toggle_pt_brushType:
                    layout.separator()
                    NSMUI_PT_Brushes_ByType.draw(self, context)

                elif wm.toggle_pt_brushRecents:
                    layout.separator()
                    NSMUI_PT_Brushes_Recent.draw(self, context)


# FAV BRUSHES
favBrushes = []
class NSMUI_PT_Brushes_Favs(NSMUI_PT_Brushes):
    bl_context = None
    #bl_category = 'Favorites'
    # bl_options = {'DEFAULT_CLOSED'}
        
    def draw(self, context):
            wm = context.window_manager
            try:
                activeBrush = context.tool_settings.sculpt.brush

                row = self.layout.row(align=True)
                brushName = activeBrush.name
                row.operator('nsmui.ot_brush_fav_add', text="ADD", icon='ADD').nBrush = brushName
                row.operator('nsmui.ot_brush_fav_remove', text="REMOVE", icon='REMOVE').nBrush = brushName
                row = self.layout.row()
                # print (length)
                # print(recentBrushes)
            except:
                pass
            
            # RECENT BRUSHES
            length = len(favBrushes)
            
            for region in context.area.regions:
                if region.type == "UI":
                    width = region.width
                    break
            #print(width)
            
            k = 0   
            i = 1
            if wm.toggle_pt_brushShowOnlyIcons:
                #if length != 0:
                
                col = self.layout.grid_flow()
                
                if width > 420:
                    i = 10
                    colY = 1.6
                    colX = 1.6
                elif width > 350:
                    i = 8
                    colY = 1.8
                    colX = 1.8
                elif width > 280:
                    i = 6
                    colY = 2
                    colX = 2
                elif width > 230:
                    i = 5
                    colY = 2
                    colX = 2
                else:
                    i = 4
                    colY = 1.8
                    colX = 1.8

                col.scale_x = colX
                col.scale_y = colY

                for b in favBrushes:
                    if b.name == brushName:
                        act = True
                    else:
                        act = False
                    #row.template_icon(icon_value=bpy.data.brushes[b].preview.icon_id, scale=5)
                    # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    k = k + 1
                    if k == 1:
                        col = col.row()
                    #col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    col.operator('nsmui.ot_change_brush', depress=act, text="", icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name
                    if k == i:
                        col = self.layout.column()
                        col.scale_x = colX
                        col.scale_y = colY
                        k = 0
            else:
                if width > 280: 
                    i = 2 
                if width > 420: 
                    i = 3
                if length != 0:
                    #col = row.column() # define una fila
                    #col.separator()
                    col = self.layout.grid_flow()
                    col.scale_y = 1.1
                    col.scale_x = 1.1

                for b in favBrushes:
                    if b.name == brushName:
                        act = True
                    else:
                        act = False
                    #row.template_icon(icon_value=bpy.data.brushes[b].preview.icon_id, scale=5)
                    # col.label(text=b, icon_value=bpy.data.brushes[b].preview.icon_id) # SOLO PREVIEW
                    if i == 1:
                        col.operator('nsmui.ot_change_brush', depress=act, text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name
                    else:
                        k = k + 1
                        if k == 1:
                            col = col.row()
                        col.operator('nsmui.ot_change_brush', depress=act, text=b.name, icon_value=bpy.data.brushes[b.name].preview.icon_id).nBrush = b.name
                        if k == i:
                            col = self.layout.column()
                            col.scale_y = 1.1
                            col.scale_x = 1.1
                            k = 0
                    

class NSMUI_OT_brush_fav_remove(bpy.types.Operator):
    bl_idname = "nsmui.ot_brush_fav_remove"
    bl_label = "Remove Fav Brush"
    bl_description = "Remove Active Brush from Favourites."
    nBrush: bpy.props.StringProperty()
    def execute(self, nbrush):
        try:
            favBrushes.remove(bpy.data.brushes[self.nBrush])
        except:
            pass
        return {'FINISHED'}
class NSMUI_OT_brush_fav_add(bpy.types.Operator):
    bl_idname = "nsmui.ot_brush_fav_add"
    bl_label = "Add Fav Brush"
    bl_description = "Add Active Brush to Favourites."
    nBrush: bpy.props.StringProperty()
    def execute(self, nBrush):
        if  bpy.data.brushes[self.nBrush] in favBrushes:
            return {'FINISHED'}
        else:
            favBrushes.append(bpy.data.brushes[self.nBrush])
        return {'FINISHED'}


class NSMUI_PT_Brushes_ByType(NSMUI_PT_Brushes):
    bl_context = "NONE"
    # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        try:   
            brush = context.tool_settings.sculpt.brush
            #sculpt = context.tool_settings.sculpt
            i = 1
            for region in context.area.regions:
                if region.type == "UI":
                    width = region.width
                    break
            #print(width)
            if width > 280: 
                i = 2 
                if width > 420: 
                    i = 3
            col = self.layout.column() # define una fila
            # BRUSH LIST
            k = 0
            for b in bpy.data.brushes:
                if (b.sculpt_tool == brush.sculpt_tool) and (not b.use_paint_vertex) and (b.use_paint_sculpt):
                    icon = bpy.data.brushes[b.name].preview
                    if b.name == brush.name:
                        act = True
                    else:
                        act = False
                    #icon.icon_size = (2,2)
                    if i == 1:
                        col.scale_y = 1.1
                        col.scale_x = 1.1
                        col.operator('nsmui.ot_change_brush', depress=act, text=b.name, icon_value=icon.icon_id).nBrush = b.name
                    else:
                        k = k + 1
                        if k == 1:
                            col = col.row()
                        col.operator('nsmui.ot_change_brush', depress=act, text=b.name, icon_value=icon.icon_id).nBrush = b.name
                        if k == i:
                            col = self.layout.column()
                            k = 0
        except:
            pass

# PROPERTY IS REFERENCE IMAGE

# REFERENCES PANEL
refImages = [] # TO STORE REFERENCE IMAGES
refImagesToDraw = [] # TOGGLE WHICH IMAGE WILL BE DRAWN
position = (200,200)
width = 100
height = 100
oldTexture = None
class NSMUI_PT_References(Panel):
    bl_label = "References"
    bl_category = 'Brushes'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = ".paint_common"
    bl_options = {'DEFAULT_CLOSED'}

    def drawImage():
        count = 0
        numImagesToDraw = len(refImages)
        for canDraw in refImagesToDraw:
            if (count <= numImagesToDraw and canDraw):
                draw_texture_2d(refImages[count], count+1)
                print(count)
                count += 1
    
    bpy.types.SpaceView3D.draw_handler_add(drawImage, (), 'WINDOW', 'POST_PIXEL')

    def draw(self, context):
        if(context.mode != "SCULPT"):
            return

        layout = self.layout
        # Select an image to add bool property true and add it to the references list
        layout.template_ID(context.scene, "refImage", open="image.open")
        row = layout.row(align=True)
        #row.label(text="ADD")
        #row.label(text="REMOVE")
        try:
            image = context.scene.refImage
            if(image in refImages):
                pass # no mostrar botón de añadir si la imagen ya está añadida
            else: 
                row.operator('nsmui.ot_reference_add', text="ADD REFERENCE", icon='ADD').refName = image.name
        except:
            pass

        col = self.layout.column()
        count = 1
        if refImages == None: 
            return
        for img in refImages:
            n = count - 1
            active = refImagesToDraw[n]
            row = col.row(align=True)
            row.operator('nsmui.ot_reference_toggle',text="", icon='HIDE_OFF', depress=active).refNum = n
            name = "Ref. " + str(count)
            row.prop(img, "name", text=name)
            _row = row.row()
            _row.alert = True
            _row.operator('nsmui.ot_reference_remove', text="", icon='REMOVE').refName = img.name
            count += 1

#from bpy import *



# Transparent color to replace pixels with
transparentColor = (1.0, 0.2, 0.2, 1.0)
def draw_texture_2d(image, count):
    shader = gpu.shader.from_builtin('2D_IMAGE')
    if(count == 1):
        mul = 1
    else:
        mul = 0.75 * count
    batch = batch_for_shader(
        shader, 'TRI_FAN',
        {
            "pos": ((100, 100*count*mul), (200, 100*count*mul), (200, 200*count), (100, 200*count)),
            "texCoord": ((0, 0), (1, 0), (1, 1), (0, 1)),
        },
    )
    # not working, just for textures not images
    try:
        image.use_alpha = True
    except:
        pass
    try:
        image.use_calculate_alpha = True
    except:
        pass

    if image.gl_load():
        raise Exception()

    '''
    # INTERATE OVER PIXELS TO CHANGE ABSOLUTE BLACK TO TRANSPARENT
    num_pixels = len(image.pixels)
    if image.file_format == 'PNG':
        for px in range(0, num_pixels, 16):
            count = 0
            for i in range(4):
                if i == 1:
                    if(image.pixels[px+i] == 1.0):
                        if(image.pixels[px+i+1] == 1.0):
                            if(image.pixels[px+i+2] == 1.0):
                                image.pixels[px+i+3] = (1.0)
                count += 1
    '''      
    '''
    if image.file_format == 'PNG':
        px = image.size # Get original size of the image
        pxWidth = px[0] # Width of the original image
        pxHeight = px[1] # Height of the original image
        x = 0 # count for width pixels
        y = 0 # count for height pixels
        while x <= pxWidth: # iterate over wisth pixels
            while y <= pxHeight: # iterate over height pixels
                ##currentPixel = image.getPixelI(x, y) # get actual pixel color (r, g, b, a)
                ##currentPixel = image.pixels[offs+i])
                currentPixel = get_pixel(image, x, y)
                # if color is absolute black
                if ((currentPixel[0] == 0) and (currentPixel[1] == 0) and (currentPixel[2] == 0)):
                    ##image.setPixelI(x, y, (0, 0, 0, 0)) # turn it back to transparent
                    set_pixel(image, x, y, transparentColor)
                y += 1 # increment pixel in height
            x += 1 # increment pixel in width
    '''
    
    # DRAW IMAGE
    bgl.glActiveTexture(bgl.GL_TEXTURE0)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, image.bindcode)

    shader.bind()
    shader.uniform_int("image", 0)
    batch.draw(shader)

def set_pixel(image, x, y, color):
    offs = (x + int(y*width)) * 4
    for i in range(4):
        image.pixels[offs+i] = color[i]

def get_pixel(image, x, y):
    color=[]
    offs = (x + int(y*width)) * 4
    for i in range(4):
        color.append( image.pixels[offs+i] )
    return color

# ADD A REFERENCE IMAGE TO THE LIST     
class NSMUI_OT_reference_add(bpy.types.Operator):
    bl_idname = "nsmui.ot_reference_add"
    bl_label = "Add Reference"
    bl_description = "Add reference image"
    refName: bpy.props.StringProperty()
    def execute(self, refName):
        if  bpy.data.images[self.refName] in refImages:
            return {'FINISHED'}
        else:
            refImages.append(bpy.data.images[self.refName])
            index = refImages.index(bpy.data.images[self.refName])
            refImagesToDraw.insert(index, False)
        return {'FINISHED'}

# REMOVE A REFERENCE IMAGE FROM THE LIST
class NSMUI_OT_reference_remove(bpy.types.Operator):
    bl_idname = "nsmui.ot_reference_remove"
    bl_label = "Remove Reference"
    bl_description = "Remove reference image"
    refName: bpy.props.StringProperty()
    def execute(self, refName):
        try:
            index = refImages.index(bpy.data.images[self.refName])
            refImagesToDraw.pop(index)
            refImages.remove(bpy.data.images[self.refName])
        except:
            pass
        return {'FINISHED'}

class NSMUI_OT_reference_toggle(bpy.types.Operator):
    bl_idname = "nsmui.ot_reference_toggle"
    bl_label = "Activate Reference"
    bl_description = "Make visible the reference"
    refNum: bpy.props.IntProperty()
    def execute(self, refNum):
        try:
            if refImagesToDraw[self.refNum] == True:
                refImagesToDraw[self.refNum] = False
            else:
                refImagesToDraw[self.refNum] = True
        except:
            pass
        return {'FINISHED'}

###########################
###########################
###########################



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