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
        "version": (1, 2, 5),
        "blender": (2, 80, 0),
        "location": "Info Toolbar, File -> Import, File -> Export",
        "wiki_url":    "https://github.com/Digiography/blender_addon_iclone/wiki",
        "tracker_url": "https://github.com/Digiography/blender_addon_iclone/issues",
        "category": "Import-Export",
}

import bpy
from . import ds_ic

class ds_ic_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_ic_exe : bpy.props.StringProperty(
                name="iClone Executable",
                subtype='FILE_PATH',
                default="C:\Program Files\Reallusion\iClone 7\Bin64\iClone.exe",
        )    
        option_ic_cc_exe : bpy.props.StringProperty(
                name="Character Creator Executable",
                subtype='FILE_PATH',
                default="C:\Program Files\Reallusion\Character Creator 3\Bin64\CharacterCreator.exe",
        )    
        option_ic_3dx_exe : bpy.props.StringProperty(
                name="3DXchange Executable",
                subtype='FILE_PATH',
                default="C:\Program Files (x86)\Reallusion\iClone 3DXchange 7\Bin\iClone3DXchange.exe",
        )      
        option_export_folder : bpy.props.StringProperty(
                name="Export Folder Name",
                default="eXport",
        )     
        option_textures_folder : bpy.props.StringProperty(
                name="Textures Folder Name",
                default="Textures",
        )     
        option_ic_templates_path : bpy.props.StringProperty(
                name="iClone Templates Path",
                subtype='DIR_PATH',
                default="",
        )     
        option_show_zbc : bpy.props.BoolProperty(
                name="Show ZBrushCore Buttons",
                default=True,
        )
        option_show_iclone_toggle : bpy.props.BoolProperty(
                name="iClone Buttons Toggle",
                default=True,
        )
        option_show_iclone_toggle_state : bpy.props.BoolProperty(
                name="iClone Toggle Button State",
                default=False,
        )                          
        option_save_before_export : bpy.props.BoolProperty(
                name="Save Before Export",
                default=True,
        )     
        option_display_type : bpy.props.EnumProperty(
                items=[('Buttons', "Buttons", "Use Buttons"),('Menu', "Menu", "Append a Menu to Main Menu"),('Hide', "Import/Export", "Use only Import/Export Menu's"),],
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
                box.label(text='Automatically created as a sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')
                box=layout.box()
                box.prop(self, 'option_show_iclone_toggle')
                box.prop(self, 'option_save_before_export')

class ds_ic_menu(bpy.types.Menu):

    bl_label = " " + bl_info['name']
    bl_idname = "ds_ic.menu"

    def draw(self, context):
            
        layout = self.layout

        layout.operator('ds_ic.import_base',icon="IMPORT")
        layout.operator('ds_ic.import_female',icon="IMPORT")
        layout.operator('ds_ic.import_male',icon="IMPORT")
        layout.separator()
        layout.operator('ds_ic.export_cc',icon="LINK_BLEND")
        layout.operator('ds_ic.export_3dx',icon="EXPORT")
        layout.operator('ds_ic.export_ic',icon="LINK_BLEND")

def draw_ds_ic_menu(self, context):

        layout = self.layout
        layout.menu(ds_ic_menu.bl_idname,icon="COLLAPSEMENU")

def ds_ic_menu_func_import_base(self, context):
    self.layout.operator("ds_ic.import_base")
def ds_ic_menu_func_import_female(self, context):
    self.layout.operator("ds_ic.import_female")
def ds_ic_menu_func_import_male(self, context):
    self.layout.operator("ds_ic.import_male")
def ds_ic_menu_func_export_cc(self, context):
    self.layout.operator("ds_ic.export_cc")
def ds_ic_menu_func_export_3dx(self, context):
    self.layout.operator("ds_ic.export_3dx")

def ds_ic_draw_btns(self, context):
    
    if context.region.alignment != 'RIGHT':

        layout = self.layout
        row = layout.row(align=True)
        
        if bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle:

                if bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle_state:
                        row.operator(ds_ic_toggle.bl_idname,text="iClone",icon="TRIA_LEFT")
                else:
                        row.operator(ds_ic_toggle.bl_idname,text="iClone",icon="TRIA_RIGHT")

        if bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle_state or not bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle:

                row.operator("ds_ic.import_base",text="Base",icon="IMPORT")
                row.operator("ds_ic.import_female",text="Female",icon="IMPORT")
                row.operator("ds_ic.import_male",text="Male",icon="IMPORT")
                row.operator("ds_ic.export_cc",text="CC",icon="LINK_BLEND")
                row.operator("ds_ic.export_3dx",text="3DX",icon="EXPORT")

class ds_ic_toggle(bpy.types.Operator):

    bl_idname = "ds_ic.toggle"
    bl_label = "iClone"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):

        if not bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle_state:
            bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle_state=True
        else:
            bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle_state=False
        return {'FINISHED'}

classes = (
    ds_ic_addon_prefs,
    ds_ic_toggle,
)

def register():

        from bpy.utils import register_class
        for cls in classes:
                register_class(cls)

        ds_ic.register()

        bpy.types.TOPBAR_MT_file_import.append(ds_ic_menu_func_import_base)
        bpy.types.TOPBAR_MT_file_import.append(ds_ic_menu_func_import_female)
        bpy.types.TOPBAR_MT_file_import.append(ds_ic_menu_func_import_male)
        bpy.types.TOPBAR_MT_file_export.append(ds_ic_menu_func_export_cc)
        bpy.types.TOPBAR_MT_file_export.append(ds_ic_menu_func_export_3dx)

        bpy.context.preferences.addons[__package__].preferences.option_show_iclone_toggle_state=False

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.append(ds_ic_draw_btns)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                register_class(ds_ic_menu)
                bpy.types.INFO_HT_header.append(draw_ds_ic_menu)

def unregister():

        bpy.types.TOPBAR_MT_file_import.remove(ds_ic_menu_func_import_base)
        bpy.types.TOPBAR_MT_file_import.remove(ds_ic_menu_func_import_female)
        bpy.types.TOPBAR_MT_file_import.remove(ds_ic_menu_func_import_male)
        bpy.types.TOPBAR_MT_file_export.remove(ds_ic_menu_func_export_cc)
        bpy.types.TOPBAR_MT_file_export.remove(ds_ic_menu_func_export_3dx)

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.remove(ds_ic_draw_btns)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                unregister_class(ds_ic_menu)
                bpy.types.INFO_HT_header.remove(draw_ds_ic_menu)

        ds_ic.unregister()

        from bpy.utils import unregister_class
        for cls in reversed(classes):
                unregister_class(cls)

if __name__ == "__main__":

	register()