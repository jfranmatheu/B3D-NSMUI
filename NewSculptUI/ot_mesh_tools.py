import bpy
from bpy.types import Operator, Panel
from bpy.props import StringProperty, IntProperty, FloatProperty, BoolProperty, EnumProperty

def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

class NSMUI_OT_Close_Gaps(Operator):
    """Destroy those gaps from that broken mesh!"""
    bl_idname = "nsmui.close_gaps"
    bl_label = "Close Gaps"

    use : EnumProperty (
        items=(
            ('TRIS', "Tris", ""),
            ('QUADS', "Quads", "")
        ),
        default='TRIS',
        name="Use tris or quads",
        description="Close gap with tris or quads"
    )

    smooth_passes : IntProperty (
        default = 3,
        max = 10,
        min = 0,
        name = "Smooth Passes",
        description = "Number of smooth passes that will be applied after closing the gap"
    )

    keep_dyntopo : BoolProperty (
        default = True,
        name="Keep Dyntopo",
        description="Only works if you are using dyntopo"
    )

    def execute(self, context):
        usingDyntopo = bpy.context.sculpt_object.use_dynamic_topology_sculpting
        try:
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE', action='TOGGLE')
            bpy.ops.mesh.select_non_manifold()
            if self.use == 'TRIS':
                bpy.ops.mesh.fill()
            elif self.use == 'QUADS':
                try:
                    bpy.ops.mesh.fill_grid()
                except:
                    ShowMessageBox("The mesh is not compatible with 'Quads' mode or there's no gaps to close.", "Can't close gaps.", 'ERROR')
                    bpy.ops.mesh.fill()
                    #bpy.ops.mesh.fill_holes(sides=100)
            n = 0
            while n < self.smooth_passes:
                bpy.ops.mesh.vertices_smooth()
                n+=1
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='SCULPT')

            if self.keep_dyntopo and usingDyntopo:
                bpy.ops.sculpt.dynamic_topology_toggle()
        except:
            bpy.ops.object.mode_set(mode='SCULPT')
            if self.keep_dyntopo and usingDyntopo:
                bpy.ops.sculpt.dynamic_topology_toggle()
        return {'FINISHED'}

class NSMUI_PT_Close_Gaps_Options(Panel):
    bl_label = "Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Close gaps options"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row()
        row.prop(scn, 'closeGaps_use', expand=True, text="Tris")
        row = layout.row()
        row.prop(scn, 'closeGaps_smooth_passes')
        row = layout.row()
        row.prop(scn, 'closeGaps_keep_dyntopo')


class NSMUI_OT_Cutter(Operator):
    """Cut your sculpt as you want! Take care it cuts!"""
    bl_idname = "nsmui.cutter"
    bl_label = "Cutter"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        return {'FINISHED'}

class NSMUI_PT_Mask_Extractor_Options(Panel):
    bl_label = "Options"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_context = "NONE"
    bl_category = 'Sculpt'
    bl_description = "Mask Extractor options"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        scn = context.scene
        layout = self.layout
        row = layout.row()
        row.prop(scn, 'maskExtractor_Mode', expand=True, text="Solid")
        _row = layout.column()
        if scn.maskExtractor_Mode == 'FLAT':
            _row.active = False
        else:
            _row.active = True
        #row = layout.row()
        row = _row.row()
        row.prop(scn, 'maskExtractor_Thickness', slider=True)
        row = _row.row()
        row.prop(scn, 'maskExtractor_SuperSmooth', slider=True)
        row = _row.row()
        row.prop(scn, 'maskExtractor_SmoothPasses')

class NSMUI_OT_Mask_Extractor(Operator):
    """Extracts the masked area into a new mesh"""
    bl_idname = "nsmui.mask_extractor"
    bl_label = "Mask Extractor"
    bl_options = {'REGISTER', 'UNDO'}

    offset : FloatProperty(min = -10.0, max = 10.0, default = 0.1, name="Offset")
    thickness : FloatProperty(min = 0.0, max = 10.0, default = 0.5, name="Thickness")
    smoothPasses : IntProperty(min = 0, max = 30, default = 4, name="Smooth Passes")  
    mode : EnumProperty(name="Extract Mode",
                     items = (("SOLID","Solid",""),
                              ("SINGLE","One Sided",""),
                              ("FLAT","Flat","")),
                     default = "SOLID", description="Mode in how to apply the mesh extraction"
    )
    superSmooth : BoolProperty(default = False, name="Super Smooth")
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'SCULPT'
    
    def draw(self, context): 
        layout = self.layout
        layout.prop(self, "mode", text="Mode")
        layout.prop(self, "thickness", text="Thickness")
        #layout.prop(self, "offset", text="Offset")
        layout.prop(self, "smoothPasses", text="Smooth Passes")
    
    def execute(self, context):
        activeObj = context.active_object
        
        # This is a hackish way to support redo functionality despite sculpt mode having its own undo system.
        # The set of conditions here is not something the user can create manually from the UI.
        # Unfortunately I haven't found a way to make Undo itself work
        if  2>len(bpy.context.selected_objects)>0 and \
            context.selected_objects[0] != activeObj and \
            context.selected_objects[0].name.startswith("Extracted_"):
            rem = context.selected_objects[0]
            remname = rem.data.name
            bpy.data.scenes.get(context.scene.name).objects.unlink(rem) # checkear esto
            bpy.data.objects.remove(rem)
            # remove mesh to prevent memory being cluttered up with hundreds of high-poly objects
            bpy.data.meshes.remove(bpy.data.meshes[remname])
        
        # For multires we need to copy the object and apply the modifiers
        try:
            if activeObj.modifiers["Multires"]:
                use_multires = True
                objCopy = helper.objDuplicate(activeObj)
                context.view_layer.objects.active = objCopy
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.boolean.mod_apply()
        except:
            use_multires = False
            pass
            
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Automerge will collapse the mesh so we need it off.
        if context.scene.tool_settings.use_mesh_automerge:
            automerge = True
            bpy.data.scenes[context.scene.name].tool_settings.use_mesh_automerge = False
        else:
            automerge = False

        # Until python can read sculpt mask data properly we need to rely on the hiding trick
        #bpy.ops.mesh.select_all(action='SELECT')
        #bpy.ops.mesh.normals_make_consistent()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='HIDE', area='MASKED')
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type="FACE")
        bpy.ops.mesh.reveal()
        bpy.ops.mesh.duplicate_move(MESH_OT_duplicate=None, TRANSFORM_OT_translate=None)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode='EDIT')

        print(context.active_object)
        print(context.view_layer.objects.active)

        # For multires we already have a copy, so lets use that instead of separate.
        if use_multires == True:
            bpy.ops.mesh.select_all(action='INVERT')
            bpy.ops.mesh.delete(type='FACE')
            context.view_layer.objects.active = objCopy
        else:
            try:
                bpy.ops.mesh.separate(type="SELECTED")
                context.view_layer.objects.active = context.selected_objects[0] #bpy.context.window.scene.objects[0] #context.selected_objects[0]
            except:
                bpy.ops.object.mode_set(mode='SCULPT')
                bpy.ops.paint.hide_show(action='SHOW', area='ALL')
                return {'FINISHED'}
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Rename the object for disambiguation
        context.view_layer.objects.active.name = "Extracted_" + context.view_layer.objects.active.name
        #bpy.ops.object.mode_set(mode='EDIT')
        print(context.active_object)
        print(context.view_layer.objects.active)
        
        # Solid mode should create a two-sided mesh
        if self.mode == 'SOLID':
            '''
            if self.superSmooth:
                # Seleccion de borde entre malla extraida y malla original
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE', action='TOGGLE')
                bpy.ops.mesh.select_non_manifold()
                # Aumentar seleccion en 1
                bpy.ops.mesh.select_more()
                # Invertir
                bpy.ops.mesh.select_all(action='INVERT')
                # Añadir al vertex group 
                bpy.ops.object.vertex_group_add()
                bpy.ops.object.vertex_group_assign()
                # Guardar referencia para más tarde
                ob = context.object
                group = ob.vertex_groups.active
            '''
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = context.active_object
            if self.smoothPasses > 0: # aplicar smooth inicial solo si los pases son mayores a 0
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.iterations = self.smoothPasses
                bpy.ops.object.modifier_apply(modifier="Smooth")
            solidi = obj.modifiers.new(name="Solid", type='SOLIDIFY')
            solidi.thickness = self.thickness
            solidi.offset = 1 # add later
            solidi.thickness_clamp = 0
            solidi.use_rim = True
            solidi.use_rim_only = False
            bpy.ops.object.modifier_apply(modifier="Solid")
            if self.superSmooth: # post-smooth para suavizarlo mucho más
                #bpy.ops.object.vertex_group_select()
                #smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                #smooth.iterations = self.smoothPasses
                #smooth.vertex_group = group.name
                #bpy.ops.object.modifier_apply(modifier="Smooth")
                co_smooth = obj.modifiers.new(name="Co_Smooth", type='CORRECTIVE_SMOOTH')
                co_smooth.iterations = 30
                co_smooth.smooth_type = 'LENGTH_WEIGHTED'
                co_smooth.use_only_smooth = True
                bpy.ops.object.modifier_apply(modifier="Co_Smooth")

        elif self.mode == 'SINGLE':
            bpy.ops.object.mode_set(mode='OBJECT')
            obj = context.active_object
            if self.smoothPasses > 0 and self.superSmooth==False:
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.iterations = self.smoothPasses
                bpy.ops.object.modifier_apply(modifier="Smooth")
            solidi = obj.modifiers.new(name="Solid", type='SOLIDIFY')
            solidi.thickness = self.thickness
            solidi.offset = 1 # add later
            solidi.thickness_clamp = 0
            solidi.use_rim = True
            solidi.use_rim_only = True # only one sided
            bpy.ops.object.modifier_apply(modifier="Solid")
            if self.superSmooth: # post-smooth para suavizarlo mucho más
                # Seleccion de borde entre malla extraida y malla original
                bpy.ops.object.mode_set(mode='EDIT')
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT', action='TOGGLE')    
                bpy.ops.mesh.select_non_manifold()
                # Invertir
                bpy.ops.mesh.select_all(action='INVERT')
                # Añadir al vertex group 
                bpy.ops.object.vertex_group_add()
                bpy.ops.object.vertex_group_assign()
                # Aplica smooth
                bpy.ops.object.mode_set(mode='OBJECT')
                smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
                smooth.factor = 1.5
                smooth.iterations = 30 # valor máximo
                smooth.vertex_group = context.object.vertex_groups.active.name # usa vertex group
                bpy.ops.object.modifier_apply(modifier="Smooth")
                # trick scale to close up the extracted mesh to original mesh due to smooth # not necessary now

            
        elif self.mode == 'FLAT':
            pass
            ''' OLD
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            n = 0
            while n < self.smoothPasses:
                bpy.ops.mesh.vertices_smooth()
                n+=1
            #bpy.ops.mesh.solidify(thickness=0)
            '''

            # later will add close mesh bool
            
        # clear mask on the extracted mesh
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.mask_flood_fill(mode='VALUE', value=0)
        
        bpy.ops.object.mode_set(mode='OBJECT')

        # make sure to recreate the odd selection situation for redo
        if use_multires:
            bpy.ops.object.select_pattern(pattern=context.active_object.name, case_sensitive=True, extend=False)

        #bpy.ops.object.select_all(action = 'DESELECT')

        #context.view_layer.objects.active = activeObj
        
        # restore automerge
        if automerge:
            bpy.data.scenes[context.scene.name].tool_settings.use_mesh_automerge = True

        # restore mode for original object
        bpy.ops.object.mode_set(mode='SCULPT')
        bpy.ops.paint.hide_show(action='SHOW', area='ALL')
        #if(usingDyntopo):
        #    bpy.ops.sculpt.dynamic_topology_toggle()
        return {'FINISHED'}