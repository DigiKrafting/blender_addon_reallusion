# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
        "name": "iClone",
        "description": "iClone Tools",
        "author": "Digiography.Studio",
        "version": (1, 0, 0),
        "blender": (2, 79, 0),
        "location": "Info Toolbar, File -> Import, File -> Export",
        "wiki_url":    "https://github.com/Digiography/blender_addon_iclone/wiki",
        "tracker_url": "https://github.com/Digiography/blender_addon_iclone/issues",
        "category": "System",
}

import bpy

from . import ds_ic

class ds_ic_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_ic_exe = bpy.props.StringProperty(
                name="iClone Executable",
                subtype='FILE_PATH',
                default="C:\Program Files\Reallusion\iClone 7\Bin64\iClone.exe",
        )    
        option_ic_cc_exe = bpy.props.StringProperty(
                name="iClone Character Creator Executable",
                subtype='FILE_PATH',
                default="C:\Program Files\Reallusion\Character Creator 2 for iClone\Bin64\CharacterCreator.exe",
        )    
        option_ic_3dx_exe = bpy.props.StringProperty(
                name="iClone 3DX Executable",
                subtype='FILE_PATH',
                default="C:\Program Files (x86)\Reallusion\iClone 3DXchange 7\Bin\iClone3DXchange.exe",
        )      
        option_export_folder = bpy.props.StringProperty(
                name="Export Folder Name",
                default="eXport",
        )     
        option_textures_folder = bpy.props.StringProperty(
                name="Textures Folder Name",
                default="Textures",
        )     
        option_ic_templates_path = bpy.props.StringProperty(
                name="iClone Templates Path",
                subtype='DIR_PATH',
                default="",
        )     
        option_show_zbc = bpy.props.BoolProperty(
                name="Show ZBrushCore Buttons",
                default=True,
        )
        option_show_iclone_toggle = bpy.props.BoolProperty(
                name="iClone Toggle",
                default=True,
        )
        option_show_iclone_toggle_state = bpy.props.BoolProperty(
                name="iClone Toggle Button State",
                default=False,
        )                          
        option_save_before_export = bpy.props.BoolProperty(
                name="Save Before Export",
                default=True,
        )     
        options_display_types = [('Buttons', "Buttons", "Buttons"),('Menu', "Menu", "Menu"),('Hide', "Hide", "Hide"),]        
        option_display_type = bpy.props.EnumProperty(
                items=options_display_types,
                name="Display Type",
                default='Buttons',
        )
        def draw(self, context):

                layout = self.layout

                box=layout.box()
                box.prop(self, 'option_display_type')
                box.prop(self, 'option_ic_exe')
                box.prop(self, 'option_ic_3dx_exe')
                box.prop(self, 'option_ic_cc_exe')
                box.prop(self, 'option_ic_templates_path')
                box=layout.box()
                box.prop(self, 'option_export_folder')
                box.prop(self, 'option_textures_folder')
                box.label('Automatically created as a sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')
                box.prop(self, 'option_save_before_export')

class ds_ic_prefs_open(bpy.types.Operator):

    bl_idname = "ds_ic.prefs_open"
    bl_label = "Open Preferences"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
 
    def execute(self, context):
        
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')

        return {'FINISHED'}

class ds_ic_menu(bpy.types.Menu):

    bl_label = " " + bl_info['name']
    bl_idname = "ds_ic.menu"

    def draw(self, context):
            
        layout = self.layout

        layout.operator('ds_ic.import_base',icon="IMPORT")
        layout.operator('ds_ic.import_female',icon="IMPORT")
        layout.operator('ds_ic.import_male',icon="IMPORT")
        self.layout.separator()

        layout.operator('ds_ic.export_cc',icon="LINK_BLEND")
        layout.operator('ds_ic.export_3dx',icon="EXPORT")
        layout.operator('ds_ic.export_ic',icon="LINK_BLEND")

def draw_ds_ic_menu(self, context):

        layout = self.layout
        layout.menu(ds_ic_menu.bl_idname,icon="COLLAPSEMENU")



def register():

        from bpy.utils import register_class

        register_class(ds_ic_addon_prefs)
        register_class(ds_ic_prefs_open)

        ds_ic.register()

        if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Menu':

                register_class(ds_ic_menu)
                bpy.types.INFO_HT_header.append(draw_ds_ic_menu)

def unregister():

        from bpy.utils import unregister_class

        if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Menu':

                unregister_class(ds_ic_menu)
                bpy.types.INFO_HT_header.remove(draw_ds_ic_menu)

        ds_ic.unregister()

        unregister_class(ds_ic_addon_prefs)
        unregister_class(ds_ic_prefs_open)

if __name__ == "__main__":

	register()