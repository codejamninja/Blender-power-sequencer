"""Toggle mute a sequence as you click on it"""
import bpy
from math import floor

from .utils.find_strips_mouse import find_strips_mouse
from .utils.doc import doc_name, doc_idname, doc_brief, doc_description


class MouseToggleMute(bpy.types.Operator):
    """
    Toggle mute a sequence as you click on it
    """
    doc = {
        'name': doc_name(__qualname__),
        'demo': '',
        'description': doc_description(__doc__),
        'shortcuts': [
            ({'type': 'ACTIONMOUSE', 'value': 'PRESS', 'alt': True}, {}, 'Mouse Toggle Mute')
        ],
        'keymap': 'Sequencer'
    }
    bl_idname = doc_idname(doc['name'])
    bl_label = doc['name']
    bl_description = doc_brief(doc['description'])
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context is not None

    def invoke(self, context, event):
        sequencer = bpy.ops.sequencer

        # get current frame and channel the mouse hovers
        x, y = context.region.view2d.region_to_view(
            x=event.mouse_region_x, y=event.mouse_region_y)
        frame, channel = round(x), floor(y)

        # Strip selection
        sequencer.select_all(action='DESELECT')
        to_select = find_strips_mouse(context, frame, channel)

        if not to_select:
            return {"CANCELLED"}

        for s in to_select:
            s.mute = not s.mute
        return {"FINISHED"}

