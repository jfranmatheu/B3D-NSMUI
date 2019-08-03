import shutil
import tempfile
import subprocess
import os
import bpy
from bpy.types import Operator
from bpy.props import FloatProperty, BoolProperty, EnumProperty


def ShowMessageBox(message = "", title = "Message Box", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text=message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

class DyntopoRemesh(Operator):
    """Remesh by using Dyntopo Flood Fill"""
    bl_idname = "object.dyntopo_remesh"
    bl_label = "Dyntopo Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    resolution : FloatProperty(name="Resolution", subtype='FACTOR', default=100, min=1, max=300, precision=2, description="Mesh resolution. Higher value for a high mesh resolution")
    force_symmetry : BoolProperty(name="Force Symmetry", description="", default=False)
    symmetry_axis : EnumProperty(items=(('POSITIVE_X', "X", ""), ('POSITIVE_Y', "Y", ""), ('POSITIVE_Z', "Z", "")), default='POSITIVE_X', name="Axis", description="Axis where apply symmetry")
    
    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        try:
            tool_settings = context.tool_settings
            sculpt = tool_settings.sculpt
            detail_method = sculpt.detail_type_method
            sculpt.detail_type_method = 'CONSTANT'
            resolution = sculpt.constant_detail_resolution
            sculpt.constant_detail_resolution = self.resolution
            #bpy.ops.sculpt.set_detail_size()
            bpy.ops.sculpt.detail_flood_fill()
            if self.force_symmetry:
                symmetry_dir = sculpt.symmetrize_direction
                sculpt.symmetrize_direction = self.symmetry_axis
                bpy.ops.sculpt.symmetrize()
            sculpt.constant_detail_resolution = resolution
            sculpt.symmetrize_direction = symmetry_dir
            sculpt.detail_type_method = detail_method
        except:
            # Shows a message box with an error message when dyntopo is disabled
            ShowMessageBox("This remesher only works if Dyntopo is enabled", "Can't apply remesher", 'ERROR')
        
        return {'FINISHED'}


class DecimateRemesh(Operator):
    """Remesh by using Decimate Modifier"""
    bl_idname = "object.decimation_remesh"
    bl_label = "Decimation Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    decimation_type : bpy.props.EnumProperty(
        items=(('COLLAPSE', "Collapse", ""), ('UNSUBDIVIDE', "Un-Subdivide", ""), ('PLANAR', "Planar", "")),
        default='COLLAPSE', description="Decimation Type to apply"
    )
    decimation_ratio : FloatProperty(name="% of Triangles", subtype='PERCENTAGE', default=100, min=0, max=100, precision=2, description="Percentage of triangles. Less value = less triangles")
    decimation_triangulate : bpy.props.BoolProperty(name="Triangulate", description="", default=False)
    decimation_symmetry : bpy.props.BoolProperty(name="Symmetry", description="", default=False)
    decimation_symmetry_axis : bpy.props.EnumProperty(
        items=(('X', "X", ""), ('Y', "Y", ""), ('Z', "Z", "")),
        default='X', description="Axis where apply symmetry", name="Axis"
    )

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        obj = bpy.context.active_object 
        decimation = obj.modifiers.new(name="Remesh", type='DECIMATE')
        decimation.ratio = self.decimation_ratio/100 # % to factor range(0,1)
        decimation.use_collapse_triangulate = self.decimation_triangulate
        decimation.use_symmetry = self.decimation_symmetry
        decimation.symmetry_axis = self.decimation_symmetry_axis
        bpy.ops.object.modifier_apply(modifier="Remesh")

        return {'FINISHED'}

# credits to cgvirus
class InstantMeshesRemesh(bpy.types.Operator):
    """Remesh by using the Instant Meshes Remesher"""
    bl_idname = "object.instant_meshes_remesh"
    bl_label = "Instant Meshes Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    exported = False
    deterministic: bpy.props.BoolProperty(name="Deterministic (slower)", description="Prefer (slower) deterministic algorithms", default=False)
    dominant: bpy.props.BoolProperty(name="Dominant", description="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh", default=False)
    intrinsic: bpy.props.BoolProperty(name="Intrinsic", description="Intrinsic mode (extrinsic is the default)", default=False)
    boundaries: bpy.props.BoolProperty(name="Boundaries", description="Align to boundaries (only applies when the mesh is not closed)", default=False)
    crease: bpy.props.IntProperty(name="Crease Degree", description="Dihedral angle threshold for creases", default=0, min=0, max=100)
    verts: bpy.props.IntProperty(name="Vertex Count", description="Desired vertex count of the output mesh", default=2000, min=10, max=50000)
    smooth: bpy.props.IntProperty(name="Smooth iterations", description="Number of smoothing & ray tracing reprojection steps (default: 2)", default=2, min=0, max=10)
    remeshIt: bpy.props.BoolProperty(name="Start Remeshing", description="Activating it will start Remesh", default=True)
    openUI: bpy.props.BoolProperty(name="Open in InstantMeshes", description="Opens the selected object in Instant Meshes and imports the result when you are done.", default=False)

    loc = None
    rot = None
    scl = None
    meshname = None

    def execute(self, context):
        exe = context.preferences.addons["NewSculptUI"].preferences.instantMeshes_filepath
        
        if(exe == "" or exe == None):
            ShowMessageBox("You need to specify Instant Meshes filepath. It is included in the addon's folder by default", "Can't apply remesher", 'ERROR')
            return {'FINISHED'}
        orig = os.path.join(tempfile.gettempdir(), 'original.obj')
        output = os.path.join(tempfile.gettempdir(), 'out.obj')

        if self.remeshIt:
            if not self.exported:
                try:
                    os.remove(orig)
                except:
                    pass
                self.meshname = bpy.context.active_object.name
                mesh = bpy.context.active_object
                bpy.ops.export_scene.obj(filepath=orig,
                                         check_existing=False,
                                         axis_forward='-Z', axis_up='Y',
                                         use_selection=True,
                                         use_mesh_modifiers=True,
                                         use_edges=True,
                                         use_smooth_groups=False,
                                         use_smooth_groups_bitflags=False,
                                         use_normals=True,
                                         use_uvs=True, )

                self.exported = True
            mesh = bpy.data.objects[self.meshname]
            mesh.hide_viewport = False
            options = ['-c', str(self.crease),
                       '-v', str(self.verts),
                       '-S', str(self.smooth),
                       '-o', output]
            if self.deterministic:
                options.append('-d')
            if self.dominant:
                options.append('-D')
            if self.intrinsic:
                options.append('-i')
            if self.boundaries:
                options.append('-b')

            cmd = [exe] + options + [orig]
            print (cmd)

            if self.openUI:
                os.chdir(os.path.dirname(orig))
                shutil.copy2(orig, output)
                subprocess.run([exe, output])
                self.openUI = False
            else:
                subprocess.run(cmd)

            bpy.ops.import_scene.obj(filepath=output,
                                     use_split_objects=False,
                                     use_smooth_groups=False,
                                     use_image_search=False,
                                     axis_forward='-Z', axis_up='Y')
            imported_mesh = bpy.context.selected_objects[0]
            print(mesh, mesh.name)
            imported_mesh.name = mesh.name + '_remesh'
            for i in mesh.data.materials:
                print('setting mat: ' + i.name)
                imported_mesh.data.materials.append(i)
            for edge in imported_mesh.data.edges:
                edge.use_edge_sharp = False
            for other_obj in bpy.data.objects:
                other_obj.select_set(state=False)
            imported_mesh.select_set(state=True)
            imported_mesh.active_material.use_nodes = False
            imported_mesh.data.use_auto_smooth = False
            bpy.ops.object.shade_flat()
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            mesh.select_set(state=True)
            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.data_transfer(use_reverse_transfer=False,
                                         use_freeze=False, data_type='UV', use_create=True, vert_mapping='NEAREST',
                                         edge_mapping='NEAREST', loop_mapping='NEAREST_POLYNOR', poly_mapping='NEAREST',
                                         use_auto_transform=False, use_object_transform=True, use_max_distance=False,
                                         max_distance=1.0, ray_radius=0.0, islands_precision=0.1, layers_select_src='ACTIVE',
                                         layers_select_dst='ACTIVE', mix_mode='REPLACE', mix_factor=1.0)
            mesh.select_set(state=False)
            mesh.hide_viewport = True
            imported_mesh.select_set(state=False)
            os.remove(output)
            #bpy.context.space_data.overlay.show_wireframes = True

            return {'FINISHED'}
        else:
            return {'FINISHED'}

# credits to zebus3d
class QuadriflowRemesh(Operator):
    """Remesh by using the Quadriflow program"""
    bl_idname = "object.quadriflow_remesh"
    bl_label = "Quadriflow Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    exported = False
    resolution : bpy.props.IntProperty(name="Resolution", description="Desired quad face count of the output mesh", default=2000, min=10, max=50000)
    sharp: bpy.props.BoolProperty(name="Sharp Edges", description="Detect and preserve sharp edges", default=False)
    adaptive : bpy.props.BoolProperty(name="Adaptive Scale", description="", default=False)
    mcf: bpy.props.BoolProperty(name="Minimum Cost Flow", description="Enable Adaptive network simplex minimum-cost flow solver(slower)", default=False)
    sat : bpy.props.BoolProperty(name="Aggresive SAT (Unix Only)", description="Tries to guarantee a watertight result mesh(requires the minisat and timeout programs in path)", default=False)
    remeshIt : bpy.props.BoolProperty(name="Start Remeshing", description="Activating it will start Remesh", default=True)
    
    loc = None
    rot = None
    scl = None
    meshname = None

    @classmethod
    def poll(cls, context):
        return context.active_object is not None
 
    def execute(self, context):

        exe = context.preferences.addons["NewSculptUI"].preferences.quadriflow_filepath
        if(exe == "" or exe == None):
            ShowMessageBox("You need to specify Quaadriflow executable filepath. Compile it first if you don't have it (Linux/MacOS).", "Can't apply remesher", 'ERROR')
            return {'FINISHED'}

        orig = os.path.join(tempfile.gettempdir(),'original.obj')
        output = os.path.join(tempfile.gettempdir(),'out.obj')

        if self.remeshIt:

            if not self.exported:
                try:
                    os.remove(orig)
                except:
                    pass
                self.meshname = bpy.context.active_object.name
                mesh = bpy.context.active_object
                # self.loc = mesh.matrix_world.to_translation()
                # self.rot = mesh.matrix_world.to_euler('XYZ')
                # self.scl = mesh.matrix_world.to_scale()
                # bpy.ops.object.location_clear()
                # bpy.ops.object.rotation_clear()
                # bpy.ops.object.scale_clear()
                bpy.ops.export_scene.obj(filepath=orig,
                                            check_existing=False, 
                                            axis_forward='-Z', axis_up='Y',
                                            use_selection=True, 
                                            use_mesh_modifiers=True, 
                                            # use_mesh_modifiers_render=False, # Why isn't that working anymore?
                                            use_edges=True, 
                                            use_smooth_groups=False, 
                                            use_smooth_groups_bitflags=False, 
                                            use_normals=True, 
                                            use_uvs=True, 
                                            use_materials=False)
                self.exported = True
                # mesh.location = self.loc
                # mesh.rotation_euler = self.rot
                # mesh.scale = self.scl

            mesh = bpy.data.objects[self.meshname]
            mesh.hide_viewport = False
            options = []
            if self.sharp:
                options.append('-sharp')
            if self.adaptive:
                options.append('-adaptive')
            if self.mcf:
                options.append('-mcf')
            if self.sat:
                options.append('-sat')
            options.extend([
                    '-i', orig,
                    '-o', output, 
                    '-f', str(self.resolution)])
            
            cmd = [exe] + options

            print (cmd)
            
            subprocess.run(cmd)
            
            bpy.ops.import_scene.obj(filepath=output, 
                                    use_smooth_groups=False,
                                    use_image_search=False,
                                    axis_forward='-Z', axis_up='Y')
            imported_mesh = bpy.context.selected_objects[0]
            # imported_mesh.location = self.loc
            # imported_mesh.rotation_euler = self.rot
            # imported_mesh.scale = self.scl
            print(mesh, mesh.name)
            imported_mesh.name = mesh.name + '_remesh'
            for i in mesh.data.materials:
                print('setting mat: ' +i.name)
                imported_mesh.data.materials.append(i)
            for edge in imported_mesh.data.edges:
                edge.use_edge_sharp = False
            for other_obj in bpy.data.objects:
                other_obj.select_set(state= False)
            imported_mesh.select_set (state = True)
            bpy.ops.object.shade_flat()
            mesh.select_set (state = True)
            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.data_transfer(use_reverse_transfer=False, 
                                            use_freeze=False, data_type='UV', use_create=True, vert_mapping='NEAREST', 
                                            edge_mapping='NEAREST', loop_mapping='NEAREST_POLYNOR', poly_mapping='NEAREST', 
                                            use_auto_transform=False, use_object_transform=True, use_max_distance=False, 
                                            max_distance=1.0, ray_radius=0.0, islands_precision=0.1, layers_select_src='ACTIVE',
                                            layers_select_dst='ACTIVE', mix_mode='REPLACE', mix_factor=1.0)
            mesh.select_set(state= False)
            mesh.hide_viewport = True
            #mesh.hide_render = True
            imported_mesh.select_set(state= False)
            os.remove(output)
            return {'FINISHED'}
        else:
            return {'FINISHED'}

'''
class InstantMeshesRemesh_alt(Operator):
    """Remesh by using the Instant Meshes program"""
    bl_idname = "object.instant_meshes_remesh_alt"
    bl_label = "Instant Meshes Remesh"
    bl_options = {'REGISTER', 'UNDO'}

    exported = False
    deterministic: bpy.props.BoolProperty(name="Deterministic (slower)", description="Prefer (slower) deterministic algorithms", default=False)
    dominant: bpy.props.BoolProperty(name="Dominant", description="Generate a tri/quad dominant mesh instead of a pure tri/quad mesh", default=False)
    intrinsic: bpy.props.BoolProperty(name="Intrinsic", description="Intrinsic mode (extrinsic is the default)", default=False)
    boundaries: bpy.props.BoolProperty(name="Boundaries", description="Align to boundaries (only applies when the mesh is not closed)", default=False)
    crease: bpy.props.IntProperty(name="Crease Degree", description="Dihedral angle threshold for creases", default=0, min=0, max=100)
    verts: bpy.props.IntProperty(name="Vertex Count", description="Desired vertex count of the output mesh", default=2000, min=10, max=50000)
    smooth: bpy.props.IntProperty(name="Smooth iterations", description="Number of smoothing & ray tracing reprojection steps (default: 2)", default=2, min=0, max=10)
    remeshIt: bpy.props.BoolProperty(name="Start Remeshing", description="Activating it will start Remesh", default=False)
    openUI: bpy.props.BoolProperty(name="Open in InstantMeshes", description="Opens the selected object in Instant Meshes and imports the result when you are done.", default=True)

    loc = None
    rot = None
    scl = None
    meshname = None

    def execute(self, context):
        exe = context.preferences.addons["NewSculptUI"].preferences.instantMeshes_filepath
        
        if(exe == "" or exe == None):
            ShowMessageBox("You need to specify Instant Meshes filepath. It is included in the addon's folder by default", "Can't apply remesher", 'ERROR')
            return {'FINISHED'}
        orig = os.path.join(tempfile.gettempdir(), 'original.obj')
        output = os.path.join(tempfile.gettempdir(), 'out.obj')

        if self.remeshIt:

            if not self.exported:
                try:
                    os.remove(orig)
                except:
                    pass
                self.meshname = bpy.context.active_object.name
                mesh = bpy.context.active_object
                # self.loc = mesh.matrix_world.to_translation()
                # self.rot = mesh.matrix_world.to_euler('XYZ')
                # self.scl = mesh.matrix_world.to_scale()
                # bpy.ops.object.location_clear()
                # bpy.ops.object.rotation_clear()
                # bpy.ops.object.scale_clear()
                bpy.ops.export_scene.obj(filepath=orig,
                                         check_existing=False,
                                         axis_forward='-Z', axis_up='Y',
                                         use_selection=True,
                                         use_mesh_modifiers=True,
                                         # use_mesh_modifiers_render=False,
                                         use_edges=True,
                                         use_smooth_groups=False,
                                         use_smooth_groups_bitflags=False,
                                         use_normals=True,
                                         use_uvs=True, )

                self.exported = True
                # mesh.location = self.loc
                # mesh.rotation_euler = self.rot
                # mesh.scale = self.scl

            mesh = bpy.data.objects[self.meshname]
            mesh.hide_viewport = False
            options = ['-c', str(self.crease),
                       '-v', str(self.verts),
                       '-S', str(self.smooth),
                       '-o', output]
            if self.deterministic:
                options.append('-d')
            if self.dominant:
                options.append('-D')
            if self.intrinsic:
                options.append('-i')
            if self.boundaries:
                options.append('-b')

            cmd = [exe] + options + [orig]

            print (cmd)

            if self.openUI:
                os.chdir(os.path.dirname(orig))
                shutil.copy2(orig, output)
                subprocess.run([exe, output])
                self.openUI = False
            else:
                subprocess.run(cmd)

            bpy.ops.import_scene.obj(filepath=output,
                                     use_split_objects=False,
                                     use_smooth_groups=False,
                                     use_image_search=False,
                                     axis_forward='-Z', axis_up='Y')
            imported_mesh = bpy.context.selected_objects[0]
            # imported_mesh.location = self.loc
            # imported_mesh.rotation_euler = self.rot
            # imported_mesh.scale = self.scl
            print(mesh, mesh.name)
            imported_mesh.name = mesh.name + '_remesh'
            for i in mesh.data.materials:
                print('setting mat: ' + i.name)
                imported_mesh.data.materials.append(i)
            for edge in imported_mesh.data.edges:
                edge.use_edge_sharp = False
            for other_obj in bpy.data.objects:
                other_obj.select_set(state=False)
            imported_mesh.select_set(state=True)
            imported_mesh.active_material.use_nodes = False
            imported_mesh.data.use_auto_smooth = False

            bpy.ops.object.shade_flat()
            bpy.ops.mesh.customdata_custom_splitnormals_clear()

            mesh.select_set(state=True)
            bpy.context.view_layer.objects.active = mesh
            bpy.ops.object.data_transfer(use_reverse_transfer=False,
                                         use_freeze=False, data_type='UV', use_create=True, vert_mapping='NEAREST',
                                         edge_mapping='NEAREST', loop_mapping='NEAREST_POLYNOR', poly_mapping='NEAREST',
                                         use_auto_transform=False, use_object_transform=True, use_max_distance=False,
                                         max_distance=1.0, ray_radius=0.0, islands_precision=0.1, layers_select_src='ACTIVE',
                                         layers_select_dst='ACTIVE', mix_mode='REPLACE', mix_factor=1.0)
            mesh.select_set(state=False)
            #mesh.hide_viewport = True
            #mesh.hide_render = True
            mesh.hide_set(True)
            imported_mesh.select_set(state=False)
            os.remove(output)
            bpy.context.space_data.overlay.show_wireframes = True

            return {'FINISHED'}
        else:
            return {'FINISHED'}
'''