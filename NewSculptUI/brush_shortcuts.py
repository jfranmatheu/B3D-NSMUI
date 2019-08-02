#  ***** BEGIN GPL LICENSE BLOCK *****
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  ***** END GPL LICENSE BLOCK *****

# INFORMATION ############################################
# THIS CODE IS BASED ON THE ADDON BRUSH QUICKSET BY Jean Ayer
# EXTENDED, IMPROVED AND SOME BUG_ FIXES BY jfranmatheu
##########################################################

from mathutils import Color
import bpy
import blf
import bgl
import gpu
from gpu_extras.batch import batch_for_shader

vertex_shader = '''
    uniform mat4 ModelViewProjectionMatrix;

    in vec2 pos;
    in vec4 color;
    out vec4 col;

    void main()
    {
    	gl_Position = ModelViewProjectionMatrix * vec4(pos, 0.0, 1.0);
        col = color;
    }
'''

fragment_shader = '''
    in vec4 col;

    void main()
    {
        gl_FragColor = col;
    }
'''

rectpoints = (
    (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
)

circlepoints = (
( 0.0 ,  1.0 ),
( -0.19509 ,  0.980785 ),
( -0.382683 ,  0.92388 ),
( -0.55557 ,  0.83147 ),
( -0.707107 ,  0.707107 ),
( -0.83147 ,  0.55557 ),
( -0.92388 ,  0.382683 ),
( -0.980785 ,  0.19509 ),
( -1.0 ,  0.0 ),
( -0.980785 ,  -0.19509 ),
( -0.92388 ,  -0.382683 ),
( -0.83147 ,  -0.55557 ),
( -0.707107 ,  -0.707107 ),
( -0.55557 ,  -0.83147 ),
( -0.382683 ,  -0.92388 ),
( -0.19509 ,  -0.980785 ),
( 0.0 ,  -1.0 ),
( 0.195091 ,  -0.980785 ),
( 0.382684 ,  -0.923879 ),
( 0.555571 ,  -0.831469 ),
( 0.707107 ,  -0.707106 ),
( 0.83147 ,  -0.55557 ),
( 0.92388 ,  -0.382683 ),
( 0.980785 ,  -0.195089 ),
( 1.0 ,  0.0 ),
( 0.980785 ,  0.195091 ),
( 0.923879 ,  0.382684 ),
( 0.831469 ,  0.555571 ),
( 0.707106 ,  0.707108 ),
( 0.555569 ,  0.83147 ),
( 0.382682 ,  0.92388 ),
( 0.195089 ,  0.980786 ),
)

circleindices = (
( 1 ,  0 ,  31 ),
( 1 ,  31 ,  30 ),
( 2 ,  1 ,  30 ),
( 15 ,  13 ,  18 ),
( 30 ,  29 ,  28 ),
( 3 ,  30 ,  28 ),
( 4 ,  3 ,  28 ),
( 27 ,  5 ,  28 ),
( 3 ,  2 ,  30 ),
( 5 ,  27 ,  26 ),
( 6 ,  5 ,  26 ),
( 6 ,  26 ,  25 ),
( 7 ,  6 ,  25 ),
( 7 ,  25 ,  24 ),
( 8 ,  7 ,  24 ),
( 8 ,  24 ,  23 ),
( 9 ,  8 ,  23 ),
( 9 ,  23 ,  22 ),
( 10 ,  9 ,  22 ),
( 10 ,  22 ,  21 ),
( 11 ,  10 ,  21 ),
( 11 ,  21 ,  20 ),
( 12 ,  11 ,  20 ),
( 12 ,  20 ,  19 ),
( 13 ,  12 ,  19 ),
( 13 ,  19 ,  18 ),
( 17 ,  15 ,  18 ),
( 14 ,  13 ,  15 ),
( 15 ,  17 ,  16 ),
( 5 ,  4 ,  28 ),
)

def draw_callback_px(self, context):
    # circle graphic, text, and slider
    brush = bpy.context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities
    unify_settings = bpy.context.tool_settings.unified_paint_settings
    strength = unify_settings.strength if self.uni_str else self.brush.strength
    size = unify_settings.size if self.uni_size else self.brush.size
    smooth = brush.auto_smooth_factor if capabilities.has_auto_smooth else None
    
    vertices = []
    colors = []
    indices = []

    showText = ""
    text = ""
    font_id = 0
    font_id_Size = 0
    do_text = False
    do_textSize = False
    #do_textSmooth = False

    if self.graphic:
        # circle inside brush
        starti = len(vertices)
        for x, y in circlepoints:
            vertices.append((int(size * x) + self.cur[0], int(size * y) + self.cur[1]))
            colors.append((self.brushcolor.r, self.brushcolor.g, self.brushcolor.b, strength * 0.25))
        for i in circleindices:
            indices.append((starti + i[0], starti + i[1], starti + i[2]))

    # STRENGTH
    if self.text != 'NONE' and self.doingstr:
        showText = "Strength: "
        if self.text == 'MEDIUM':
            fontsize = 16
        elif self.text == 'LARGE':
            fontsize = 22
        else:
            fontsize = 12

        blf.size(font_id, fontsize, 72)
        # Fonts with Shadow
        #blf.shadow(font_id, 0, 0.0, 0.0, 0.0, 1.0)
        #blf.enable(font_id, blf.SHADOW)

        #if strength < 0.001:
        #    text = "0"
        #else:
        text = str(strength)[0:4]

        textsize = blf.dimensions(font_id, text)

        xpos = self.start[0] - self.offset[0] - 150
        ypos = self.start[1] + self.offset[1]
        blf.position(font_id, xpos, ypos, 0)

        # rectangle behind text
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(textsize[0] * x) + xpos, int(textsize[1] * y) + ypos))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0)) # 0.5 to 0 so BG is invisible
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        do_text = True

    # SIZE
    if self.textSize != 'NONE' and self.doingrad:
        showText = "Size: "
        if self.text == 'MEDIUM':
            fontsize = 16
        elif self.text == 'LARGE':
            fontsize = 22
        else:
            fontsize = 12

        blf.size(font_id_Size, fontsize, 72)
        # Fonts with Shadow
        #blf.shadow(font_id_Size, 0, 0.0, 0.0, 0.0, 1.0)
        #blf.enable(font_id_Size, blf.SHADOW)

        if size < 0.001:
            text = "0"
        else:
            text = str(size)[0:5]
        textsize = blf.dimensions(font_id_Size, text)

        xpos = self.start[0] - self.offset[0] - 100
        ypos = self.start[1] #+ self.offset[1]
        blf.position(font_id_Size, xpos, ypos, 0)

        # rectangle behind text
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(textsize[0] * x) + xpos, int(textsize[1] * y) + ypos))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0)) # 0.5 to 0  (Background Color)
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        do_textSize = True

    shader = gpu.types.GPUShader(vertex_shader, fragment_shader)
    batch = batch_for_shader(shader, 'TRIS', {"pos":vertices, "color":colors}, indices=indices)

    bgl.glEnable(bgl.GL_BLEND)
    shader.bind()
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

    if do_text:
        blf.draw(font_id, showText + text)
        #blf.disable(font_id, blf.SHADOW)

    if do_textSize:
        blf.draw(font_id_Size, showText + text)
        #blf.disable(font_id_Size, blf.SHADOW)

def applyChanges(self):
    unify_settings = bpy.context.tool_settings.unified_paint_settings
    
    if self.doingstr:
        if self.uni_str:
            modrate = self.strmod * 0.0025
            newval  = unify_settings.strength + modrate
            if 10.0 > newval > -0.1:
                unify_settings.strength = newval
                self.strmod_total += modrate
            
            
        else:
            modrate = self.strmod * 0.0025
            newval  = self.brush.strength + modrate
            if 10.0 > newval > -0.1:
                self.brush.strength = newval
                self.strmod_total += modrate
            

    if self.doingrad:
        if self.uni_size:
            newval = unify_settings.size + self.radmod
            if 2000 > newval > 0:
                unify_settings.size = newval
                self.radmod_total += self.radmod
        else:
            newval = self.brush.size + self.radmod
            if 2000 > newval > 0:
                self.brush.size = newval
                self.radmod_total += self.radmod



def revertChanges(self):
    unify_settings = bpy.context.tool_settings.unified_paint_settings

    if self.doingstr:
        if self.uni_str:
            unify_settings.strength -= self.strmod_total
        else:
            self.brush.strength -= self.strmod_total

    if self.doingrad:
        if self.uni_size:
            unify_settings.size -= self.radmod_total
        else:
            self.brush.size -= self.radmod_total

class PAINT_OT_brush_modal_quickset(bpy.types.Operator):
    bl_idname = "brush.modal_quickset"
    bl_label = "Brush QuickSet"

    axisaffect : bpy.props.EnumProperty(
        name        = "Axis Order",
        description = "Which axis affects which brush property",
        items       = [('YSTR', 'X: Radius, Y: Strength', ''),
                       ('YRAD', 'Y: Radius, X: Strength', '')],
        default     = 'YRAD')

    textSize : bpy.props.EnumProperty(
        name        = "Size Value",
        description = "Text display; only shows when strength adjusted",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'MEDIUM')

    keyaction : bpy.props.EnumProperty(
        name        = "Key Action",
        description = "Hotkey second press or initial release behaviour",
        items       = [('IGNORE', 'Key Ignored', ''),
                       ('CANCEL', 'Key Cancels', ''),
                       ('FINISH', 'Key Applies', '')],
        default     = 'FINISH')

    text : bpy.props.EnumProperty(
        name        = "Numeric",
        description = "Text display; only shows when strength adjusted",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE')

    slider : bpy.props.EnumProperty(
        name        = "Slider",
        description = "Slider display for strength visualization",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'NONE')

    deadzone : bpy.props.IntProperty(
        name        = "Deadzone",
        description = "Screen distance after which movement has effect",
        default     = 4,
        min         = 0)

    sens : bpy.props.FloatProperty(
        name        = "Sens",
        description = "Multiplier to affect brush settings by",
        default     = 1.0,
        min         = 0.1,
        max         = 2.0)

    graphic : bpy.props.BoolProperty(
        name        = "Graphic",
        description = "Transparent circle to visually represent strength",
        default     = True)

    lock : bpy.props.BoolProperty(
        name        = "Lock Axis",
        description = "When adjusting one value, lock the other",
        default     = True)


    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D'
                and context.mode in {'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'})

    def changeValues(self, context):
        scn = context.scene
        self.deadzone = scn.deadzone_prop
        self.sens = scn.sens_prop
        #self.slider = scn.textDisplaySize
        self.text = scn.textDisplaySize
        self.textSize = scn.textDisplaySize
        if scn.invertAxis:
            self.axisaffect = 'YSTR'
        else:
            self.axisaffect = 'YRAD'

    def modal(self, context, event):
        self.changeValues(context)
        sens = (self.sens * 0.5) if event.shift else (self.sens)
        self.cur = (event.mouse_region_x, event.mouse_region_y)
        diff = (self.cur[0] - self.prev[0], self.cur[1] - self.prev[1])

        if self.axisaffect == 'YRAD':
            # Y corresponds to radius
            if not self.doingrad:
                if self.lock:
                    if not self.doingstr and abs(self.cur[1] - self.start[1]) > self.deadzone:
                        self.doingrad = True
                        self.radmod = diff[1] * sens
                elif abs(self.cur[1] - self.start[1]) > self.deadzone:
                    self.doingrad = True
                    self.radmod = diff[1] * sens
            else:
                self.radmod = diff[1] * sens
            if not self.doingstr:
                if self.lock:
                    if not self.doingrad and abs(self.cur[0] - self.start[0]) > self.deadzone:
                        self.doingstr = True
                        self.strmod = diff[0] * sens
                elif abs(self.cur[0] - self.start[0]) > self.deadzone:
                    self.doingstr = True
                    self.strmod = diff[0] * sens
            else:
                self.strmod = diff[0] * sens
        else:
            # Y corresponds to strength
            if not self.doingrad:
                if self.lock:
                    if not self.doingstr and abs(self.cur[0] - self.start[0]) > self.deadzone:
                        self.doingrad = True
                        self.radmod = diff[0] * sens
                elif abs(self.cur[0] - self.start[0]) > self.deadzone:
                    self.doingrad = True
                    self.radmod = diff[0] * sens
            else:
                self.radmod = diff[0] * sens
            if not self.doingstr:
                if self.lock:
                    if not self.doingrad and abs(self.cur[1] - self.start[1]) > self.deadzone:
                        self.doingstr = True
                        self.strmod = diff[1] * sens
                elif abs(self.cur[1] - self.start[1]) > self.deadzone:
                    self.doingstr = True
                    self.strmod = diff[1] * sens
            else:
                self.strmod = diff[1] * sens

        context.area.tag_redraw()
        if event.type in {'LEFTMOUSE'} or self.action == 1:
            # apply changes, finished
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            applyChanges(self)
            return {'FINISHED'}
        elif event.type in {'ESC'} or self.action == -1:
            # do nothing, return to previous settings
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            revertChanges(self)
            return {'CANCELLED'}
        elif self.keyaction != 'IGNORE' and event.type in {self.hotkey} and event.value == 'RELEASE':
            # if key action enabled, prepare to exit
            if self.keyaction == 'FINISH':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = 1
            elif self.keyaction == 'CANCEL':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = -1
            return {'RUNNING_MODAL'}
        else:
            # continuation
            applyChanges(self)
            self.prev = self.cur
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}


    def invoke(self, context, event):
        if bpy.context.mode == 'SCULPT':
            self.brush = context.tool_settings.sculpt.brush
        elif bpy.context.mode == 'PAINT_TEXTURE':
            self.brush = context.tool_settings.image_paint.brush
        elif bpy.context.mode == 'PAINT_VERTEX':
            self.brush = context.tool_settings.vertex_paint.brush
        elif bpy.context.mode == 'PAINT_WEIGHT':
            self.brush = context.tool_settings.weight_paint.brush
        else:
            self.report({'WARNING'}, "Mode invalid - only paint or sculpt")
            return {'CANCELLED'}

        self.hotkey = event.type
        if self.hotkey == 'NONE':
            self.keyaction = 'IGNORE'
        self.action = 0
        unify_settings = context.tool_settings.unified_paint_settings
        self.uni_size = unify_settings.use_unified_size
        self.uni_str = unify_settings.use_unified_strength

        self.doingrad = False
        self.doingstr = False
        self.start = (event.mouse_region_x, event.mouse_region_y)
        self.prev = self.start
        self.radmod_total = 0.0
        self.strmod_total = 0.0
        self.radmod = 0.0
        self.strmod = 0.0

        # self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

        if self.graphic:
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

            self.brushcolor = self.brush.cursor_color_add
            if self.brush.sculpt_capabilities.has_secondary_color and self.brush.direction in {'SUBTRACT','DEEPEN','MAGNIFY','PEAKS','CONTRAST','DEFLATE'}:
                self.brushcolor = self.brush.cursor_color_subtract

        if self.text != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

            self.offset = (30, -37)

            self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi
        
        if self.slider != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

            if self.slider == 'LARGE':
                self.sliderheight = 16
                self.sliderwidth = 180
            elif self.slider == 'MEDIUM':
                self.sliderheight = 8
                self.sliderwidth = 80
            else:
                self.sliderheight = 3
                self.sliderwidth = 60

            if not hasattr(self, 'offset'):
                self.offset = (30, -37)

            if not hasattr(self, 'backcolor'):
                self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

            self.frontcolor = context.preferences.themes['Default'].view_3d.space.text_hi
        
        # enter modal operation
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def draw_callback_px_2(self, context):
    # circle graphic, text, and slider
    brush = bpy.context.tool_settings.sculpt.brush
    capabilities = brush.sculpt_capabilities
    unify_settings = bpy.context.tool_settings.unified_paint_settings
    size = unify_settings.size if self.uni_size else self.brush.size
    smooth = brush.auto_smooth_factor if capabilities.has_auto_smooth else None
    
    vertices = []
    colors = []
    indices = []

    smoothText = "Smooth: "
    text = ""
    font_id = 0
    do_textSmooth = False

    if self.graphic:
        # circle inside brush
        starti = len(vertices)
        for x, y in circlepoints:
            vertices.append((int(size * x) + self.cur[0], int(size * y) + self.cur[1]))
            colors.append((self.brushcolor.r, self.brushcolor.g, self.brushcolor.b, smooth * 0.25))
        for i in circleindices:
            indices.append((starti + i[0], starti + i[1], starti + i[2]))

    # SMOOTH
    if self.textSmooth != 'NONE' and self.doingsmooth:
        if self.textSmooth == 'MEDIUM':
            fontsize = 16
        elif self.textSmooth == 'LARGE':
            fontsize = 22
        else:
            fontsize = 12

        blf.size(font_id, fontsize, 72)
        # Font shadow
        #blf.shadow(font_id, 0, 0.0, 0.0, 0.0, 1.0)
        #blf.enable(font_id, blf.SHADOW)

        if smooth < 0.001:
            text = "0"
        else:
            text = str(smooth)[0:4] # 5 to 4
        textsize = blf.dimensions(font_id, text)

        xpos = self.start[0] - self.offset[0] - 150
        ypos = self.start[1] #+ self.offset[1]
        blf.position(font_id, xpos, ypos, 0)

        # rectangle behind text
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(textsize[0] * x) - xpos, int(textsize[1] * y) + ypos))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0))  #0.5 to 0
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        do_textSmooth = True
    
    # SMOOTH
    if self.slider != 'NONE' and self.doingsmooth:
        xpos = self.start[0] + self.offset[0] - self.sliderwidth + (44 if self.textSmooth == 'MEDIUM' else 64 if self.textSmooth == 'LARGE' else 24)
        #ypos = self.start[1] + self.offset[1] - self.sliderheight # + (1 if self.slider != 'SMALL' else 0)
        ypos = self.start[1] - self.sliderheight

        sliderscale = smooth

        # slider back rect
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(self.sliderwidth * x) + xpos, int(self.sliderheight * y) + ypos - 1))
            colors.append((self.backcolor.r, self.backcolor.g, self.backcolor.b, 0)) #0.5 to 0
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

        # slider front rect
        starti = len(vertices)
        # rectpoints: (0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)
        for x, y in rectpoints:
            vertices.append((int(self.sliderwidth * x * sliderscale) + xpos - 100, int(self.sliderheight * y * 0.75) + ypos))
            colors.append((self.frontcolor.r, self.frontcolor.g, self.frontcolor.b, 0.8))
        indices.extend((
            (starti, starti+1, starti+2), (starti+2, starti, starti+3)
        ))

    shader = gpu.types.GPUShader(vertex_shader, fragment_shader)
    batch = batch_for_shader(shader, 'TRIS', {"pos":vertices, "color":colors}, indices=indices)

    bgl.glEnable(bgl.GL_BLEND)
    shader.bind()
    batch.draw(shader)
    bgl.glDisable(bgl.GL_BLEND)

    if do_textSmooth:
        #blf.draw(font_id, smoothText)
        blf.draw(font_id, smoothText + text)
        #blf.disable(font_id, blf.SHADOW)

def applyChanges_2(self):
    brush = bpy.context.tool_settings.sculpt.brush

    if self.doingsmooth:
        if self.uni_smooth:
            modrate = self.smoothmod * 0.0025
            newval  = brush.auto_smooth_factor + modrate
            if 10.0 > newval > -0.1:
                brush.auto_smooth_factor = newval
                self.smoothmod_total += modrate
        else:
            modrate = self.smoothmod * 0.0025
            newval  = self.brush.auto_smooth_factor + modrate
            if 10.0 > newval > -0.1:
                self.brush.auto_smooth_factor = newval
                self.smoothmod_total += modrate

def revertChanges_2(self):
    brush = bpy.context.tool_settings.sculpt.brush
    if self.doingsmooth:
        if self.uni_smooth:
            brush.auto_smooth_factor -= self.smoothmod_total
        else:
            self.brush.auto_smooth_factor -= self.smoothmod_total

class PAINT_OT_brush_modal_quickset_2(bpy.types.Operator):
    bl_idname = "brush.modal_quickset_2"
    bl_label = "Brush QuickSet 2"

    axisaffect : bpy.props.EnumProperty(
        name        = "Axis Order",
        description = "Which axis affects which brush property",
        items       = [('YSTR', 'X: Radius, Y: Strength', ''),
                       ('YRAD', 'Y: Radius, X: Strength', '')],
        default     = 'YRAD')
    
    textSmooth : bpy.props.EnumProperty(
        name        = "Smooth Value",
        description = "Text display; only shows when strength adjusted",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE')

    keyaction : bpy.props.EnumProperty(
        name        = "Key Action",
        description = "Hotkey second press or initial release behaviour",
        items       = [('IGNORE', 'Key Ignored', ''),
                       ('CANCEL', 'Key Cancels', ''),
                       ('FINISH', 'Key Applies', '')],
        default     = 'FINISH')

    slider : bpy.props.EnumProperty(
        name        = "Slider",
        description = "Slider display for strength visualization",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE')

    deadzone : bpy.props.IntProperty(
        name        = "Deadzone",
        description = "Screen distance after which movement has effect",
        default     = 4,
        min         = 0)

    sens : bpy.props.FloatProperty(
        name        = "Sens",
        description = "Multiplier to affect brush settings by",
        default     = 1.0,
        min         = 0.1,
        max         = 2.0)

    graphic : bpy.props.BoolProperty(
        name        = "Graphic",
        description = "Transparent circle to visually represent strength",
        default     = True)

    lock : bpy.props.BoolProperty(
        name        = "Lock Axis",
        description = "When adjusting one value, lock the other",
        default     = True)


    @classmethod
    def poll(cls, context):
        return (context.area.type == 'VIEW_3D'
                and context.mode in {'SCULPT', 'PAINT_WEIGHT', 'PAINT_VERTEX', 'PAINT_TEXTURE'})


    def changeValues(self, context):
        scn = context.scene
        self.deadzone = scn.deadzone_prop
        self.sens = scn.sens_prop
        self.textSmooth = scn.textDisplaySize
        self.slider = scn.textDisplaySize
        if scn.invertAxis:
            self.axisaffect = 'YSTR'
        else:
            self.axisaffect = 'YRAD'
        
    def modal(self, context, event):
        self.changeValues(context)
        sens = (self.sens * 0.5) if event.shift else (self.sens)
        self.cur = (event.mouse_region_x, event.mouse_region_y)
        diff = (self.cur[0] - self.prev[0], self.cur[1] - self.prev[1])
        X = True
        if self.axisaffect == 'XRAD':
            # Y corresponds to Smooth
            if not self.doingspac:
                if self.lock:
                    if not self.doingsmooth and abs(self.cur[1] - self.start[1]) > self.deadzone:
                        self.doingspac = True
                        self.spacemod = diff[1] * sens
                elif abs(self.cur[1] - self.start[1]) > self.deadzone:
                    self.doingspac = True
                    self.spacemod = diff[1] * sens
            else:
                self.spacemod = diff[1] * sens
            if not self.doingsmooth:
                if self.lock:
                    if not self.doingspac and abs(self.cur[0] - self.start[0]) > self.deadzone:
                        self.doingsmooth = True
                        self.smoothmod = diff[0] * sens
                elif abs(self.cur[0] - self.start[0]) > self.deadzone:
                    self.doingsmooth = True
                    self.smoothmod = diff[0] * sens
            else:
                self.smoothmod = diff[0] * sens
        else:
            # Y corresponds to Spacing
            if not self.doingspac:
                if self.lock:
                    if not self.doingsmooth and abs(self.cur[0] - self.start[0]) > self.deadzone:
                        self.doingspac = True
                        self.spacemod = diff[0] * sens
                elif abs(self.cur[0] - self.start[0]) > self.deadzone:
                    self.doingspac = True
                    self.spacemod = diff[0] * sens
            else:
                self.spacemod = diff[0] * sens
            if not self.doingsmooth:
                if self.lock:
                    if not self.doingspac and abs(self.cur[1] - self.start[1]) > self.deadzone:
                        self.doingsmooth = True
                        self.smoothmod = diff[1] * sens
                elif abs(self.cur[1] - self.start[1]) > self.deadzone:
                    self.doingsmooth = True
                    self.smoothmod = diff[1] * sens
            else:
                self.smoothmod = diff[1] * sens

        context.area.tag_redraw()
        if event.type in {'LEFTMOUSE'} or self.action == 1:
            # apply changes, finished
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            applyChanges_2(self)
            return {'FINISHED'}
        elif event.type in {'ESC'} or self.action == -1:
            # do nothing, return to previous settings
            if hasattr(self, '_handle'):
                context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                del self._handle
            revertChanges(self)
            return {'CANCELLED'}
        elif self.keyaction != 'IGNORE' and event.type in {self.hotkey} and event.value == 'RELEASE':
            # if key action enabled, prepare to exit
            if self.keyaction == 'FINISH':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = 1
            elif self.keyaction == 'CANCEL':
                if hasattr(self, '_handle'):
                    context.space_data.draw_handler_remove(self._handle, 'WINDOW')
                    del self._handle
                self.action = -1
            return {'RUNNING_MODAL'}
        else:
            # continuation
            applyChanges_2(self)
            self.prev = self.cur
            return {'RUNNING_MODAL'}
        return {'CANCELLED'}


    def invoke(self, context, event):
        if bpy.context.mode == 'SCULPT':
            self.brush = context.tool_settings.sculpt.brush
        elif bpy.context.mode == 'PAINT_TEXTURE':
            self.brush = context.tool_settings.image_paint.brush
        elif bpy.context.mode == 'PAINT_VERTEX':
            self.brush = context.tool_settings.vertex_paint.brush
        elif bpy.context.mode == 'PAINT_WEIGHT':
            self.brush = context.tool_settings.weight_paint.brush
        else:
            self.report({'WARNING'}, "Mode invalid - only paint or sculpt")
            return {'CANCELLED'}

        self.hotkey = event.type
        if self.hotkey == 'NONE':
            self.keyaction = 'IGNORE'
        self.action = 0
        unify_settings = context.tool_settings.unified_paint_settings
        self.uni_size = unify_settings.use_unified_size
        self.uni_smooth = self.brush.auto_smooth_factor
        #self.uni_str = unify_settings.use_unified_strength
        self.smooth = self.brush.auto_smooth_factor

        self.doingsmooth = False
        self.doingspac = False
        self.start = (event.mouse_region_x, event.mouse_region_y)
        self.prev = self.start
        self.smoothmod_total = 0.0
        self.spacemod_total = 0.0
        #self.strmod_total = 0.0
        self.smoothmod = 0.0
        self.spacemod = 0.0
        #self.strmod = 0.0

        # self._handle = context.space_data.draw_handler_add(draw_callback_px, (self, context), 'WINDOW', 'POST_PIXEL')

        if self.graphic:
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px_2, (self, context), 'WINDOW', 'POST_PIXEL')

            self.brushcolor = self.brush.cursor_color_add
            if self.brush.sculpt_capabilities.has_secondary_color and self.brush.direction in {'SUBTRACT','DEEPEN','MAGNIFY','PEAKS','CONTRAST','DEFLATE'}:
                self.brushcolor = self.brush.cursor_color_subtract

        if self.textSmooth != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px_2, (self, context), 'WINDOW', 'POST_PIXEL')

            self.offset = (30, -37)

            self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

        if self.slider != 'NONE':
            if not hasattr(self, '_handle'):
                self._handle = context.space_data.draw_handler_add(draw_callback_px_2, (self, context), 'WINDOW', 'POST_PIXEL')

            if self.slider == 'LARGE':
                self.sliderheight = 16
                self.sliderwidth = 180
            elif self.slider == 'MEDIUM':
                self.sliderheight = 8
                self.sliderwidth = 80
            else:
                self.sliderheight = 3
                self.sliderwidth = 60

            if not hasattr(self, 'offset'):
                self.offset = (30, -37)

            if not hasattr(self, 'backcolor'):
                self.backcolor = Color((1.0, 1.0, 1.0)) - context.preferences.themes['Default'].view_3d.space.text_hi

            self.frontcolor = context.preferences.themes['Default'].view_3d.space.text_hi

        # enter modal operation
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def register():
    #bpy.utils.register_class(PAINT_OT_brush_modal_quickset)
    
    scn = bpy.types.Scene
    scn.deadzone_prop = bpy.props.IntProperty(
        name        = "Pixel Deadzone",
        description = "Screen distance after which movement has effect",
        default     = 4,
        min         = 0,
        max         = 16,
        subtype     = 'PIXEL',
        step        = 1,
        )

    scn.sens_prop = bpy.props.FloatProperty(
        name        = "Sensitivity",
        description = "Multiplier to affect brush settings by",
        default     = 1.0,
        min         = 0.2,
        max         = 2.0,
        step        = 0.1,
        precision   = 1,
        subtype     = 'FACTOR',
        unit        = 'NONE',
        )

    scn.textDisplaySize = bpy.props.EnumProperty(
        name        = "Text: Display Size",
        description = "Change Text Display Size",
        items       = [('NONE', 'None', ''),
                       ('LARGE', 'Large', ''),
                       ('MEDIUM', 'Medium', ''),
                       ('SMALL', 'Small', '')],
        default     = 'LARGE'
    )

    scn.invertAxis = bpy.props.BoolProperty(
        name        = "Invert Axis",
        description = "Invert Shortcut Directions",
        default     = False
    )

    cfg = bpy.context.window_manager.keyconfigs.addon
    if not cfg.keymaps.__contains__('Sculpt'):
        cfg.keymaps.new('Sculpt', space_type='EMPTY', region_type='WINDOW')
    kmi = cfg.keymaps['Sculpt'].keymap_items
    kmi.new('brush.modal_quickset', 'RIGHTMOUSE', 'PRESS')
    kmi.new('brush.modal_quickset_2', 'RIGHTMOUSE', 'PRESS', alt=True) # ESTO NO VA VER PQQQQ


def unregister():
    #bpy.utils.unregister_class(PAINT_OT_brush_modal_quickset)

    scn = bpy.types.Scene
    del scn.deadzone_prop
    del scn.sens_prop
    del scn.textDisplaySize
    del scn.invertAxis

    cfg = bpy.context.window_manager.keyconfigs.addon
    if cfg.keymaps.__contains__('Sculpt'):
        for kmi in cfg.keymaps['Sculpt'].keymap_items:
            if kmi.idname == 'brush.modal_quickset' or (kmi.idname == 'brush.modal_quickset_2'):
                if kmi.value == 'PRESS' and kmi.type == 'RIGHTMOUSE':
                    cfg.keymaps['Sculpt'].keymap_items.remove(kmi)
                    break
