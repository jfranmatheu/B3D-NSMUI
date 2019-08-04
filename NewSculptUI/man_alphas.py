import bpy
import os    
from bpy.types import Operator, Panel

class Alphas_OT_LoadAll_2(Operator):
    """Load All Alpha from Directory"""
    bl_idname = "texture.alphas_load_all_2"
    bl_label = "Autoload Texture Alphas"

    def execute(self, context):
        path = context.scene.alphas_path
        files = []
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                if '.png' in file:
                    files.append(os.path.join(r, file))

        for f in files:
            print(f)
        
        return {'FINISHED'}

def SelectFormats(formats):
    if formats == 'ALL':
        return set([".png", ".jpg", ".tif", ".tga", ".psd"])
    else:
        if formats == 'JPG':
            fileFormat = ".jpg"
        elif formats == 'PNG':
            fileFormat = ".png"
        elif formats == 'TGA':
            fileFormat = ".tga"
        elif formats == 'TIF':
            fileFormat = ".tif"
        elif formats == 'PSD':
            fileFormat = ".psd"
        return fileFormat

def ConvertToTextures(images, path):
    for img in images:
        fullname = os.path.join(path, img)
        tex = bpy.data.textures.new(img[:50]+'.alpha', type='IMAGE') # +'.autoload'
        tex.image = bpy.data.images.load(fullname)
        tex.use_alpha = True

import glob
class Alphas_OT_LoadAll(Operator):
    """Load All Alpha from Directory"""
    bl_idname = "texture.alphas_load_all"
    bl_label = "Load Texture Alphas"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scn = context.scene
        #print("path:"+context.scene.alphas_path)
        #print("abspath:"+bpy.path.abspath(context.scene.alphas_path))
        #path = bpy.path.abspath(context.scene.alphas_path)
        path = scn.alphas_path

        formats = scn.alphas_format
        oktypes = SelectFormats(formats)
        #print(oktypes)

    #   SUB-DIRS
        if scn.alphas_includeSubDirs:
        #   ALL FORMATS
            if formats == 'ALL':
                okfiles = []
                for t in oktypes:
                    for f in glob.glob(path + "**/*" + t, recursive=True):
                        okfiles.append(f)
                        #print(t)
                        #print(f)
                
        #   SPECIFIC FORMAT
            else:
                okfiles = [f for f in glob.glob(path + "**/*" + oktypes, recursive=True)]
    #   NOT SUB-DIRS
        else:
            dirfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            if formats != 'ALL':
                _oktypes = set([oktypes])
            okfiles = [f for f in dirfiles if f[-4:].lower() in _oktypes]
            
        print(okfiles)
        ConvertToTextures(okfiles, path)
            
        return {'FINISHED'}
    
class Alphas_OT_RemoveAll(Operator):
    """Remove All Alphas from Directory"""
    bl_idname = "texture.alphas_remove_all"
    bl_label = "Remove Texture Alphas"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        # LAS QUE CONTENGAN LA PARTÍCULA .alpha AÑADIDA AL CARGARLAS 
        # CAMBIAR ESTO POR ALGO MÁS CONVENIENTE EN FUTURO
        remove_these = [i for i in bpy.data.textures.keys() if 'alpha' in i.split('.')] 
        for item in remove_these:
            tex = bpy.data.textures[item]
            img = tex.image
            if not tex.users: # SIN USERS [TEXTURES]
                bpy.data.textures.remove(tex)
                img.user_clear()
                if not img.users: # SIN USERS [IMAGES]
                    bpy.data.images.remove(img)
        
        return {'FINISHED'}
    
class ALPHAS_PT_Manager(Panel):
    """Panel for Texture Manager"""
    bl_label = "Textures"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Sculpt"
    bl_context = ".paint_common"

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        obj = context.object
        row = layout.row(align=True)
        row.label(text="Directory :", icon='TEXTURE')
        row.prop(context.scene, "alphas_path", text="")
        row = layout.row(align=True)
        col = row.column(align=True)
        col.ui_units_x = 2
        col.prop(scn, 'alphas_format', expand=False, text="")
        row.prop(scn, 'alphas_includeSubDirs', text="Include Sub-Directories", toggle=False)
        row = layout.row()
        row.operator("texture.alphas_load_all", icon='ADD', text="Load Alphas from Dir")
        row = layout.row()
        row.operator("texture.alphas_remove_all", icon='REMOVE', text="Remove All Unused Alphas")

def register():
    
    bpy.types.Scene.alphas_includeSubDirs = bpy.props.BoolProperty(
        name="Include Sub-Directories", default=True
    )
    bpy.types.Scene.alphas_path = bpy.props.StringProperty(
        name="Alphas Path",
        description="Alphas Location",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.alphas_format = bpy.props.EnumProperty(
        name="Images Format",
        description="Just import images of this file format",
        items=(
            ('ALL', "All", ""),
            ('PNG', ".png", ""),
            ('TGA', ".tga", ""),
            ('TIFF', ".tif", ""),
            ('JPG', ".jpg", ""),
            ('PSD', ".psd", "")
        ),
        default='ALL'
    )

def unregister():
    del bpy.types.Scene.alphas_path
    del bpy.types.Scene.alphas_includeSubDirs
    del bpy.types.Scene.alphas_format