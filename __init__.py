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
        "name": "DKS Reallusion",
        "description": "Reallusion Pipeline",
        "author": "DigiKrafting.Studio",
        "version": (1, 3, 1),
        "blender": (2, 80, 0),
        "location": "Info Toolbar, File -> Import, File -> Export",
        "wiki_url":    "https://github.com/DigiKrafting/blender_addon_reallusion/wiki",
        "tracker_url": "https://github.com/DigiKrafting/blender_addon_reallusion/issues",
        "category": "Import-Export",
}

import bpy
from . import dks_rl

class dks_rl_addon_prefs(bpy.types.AddonPreferences):

        bl_idname = __package__

        option_rl_cc_exe : bpy.props.StringProperty(
                name="Character Creator Executable",
                subtype='FILE_PATH',
                default="C:\Program Files\Reallusion\Character Creator 3\Bin64\CharacterCreator.exe",
        )    
        option_rl_3dx_exe : bpy.props.StringProperty(
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
        option_rl_templates_path : bpy.props.StringProperty(
                name="CC Templates Path",
                subtype='DIR_PATH',
                default="",
        )     
        option_sp_rename : bpy.props.BoolProperty(
                name="Copy and Rename SP Textures",
                default=False,
        )
        option_show_rl_toggle : bpy.props.BoolProperty(
                name="Buttons Toggle",
                default=True,
        )
        option_show_rl_toggle_state : bpy.props.BoolProperty(
                name="Toggle Button State",
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
                box.prop(self, 'option_rl_3dx_exe')
                box.prop(self, 'option_rl_cc_exe')
                box.prop(self, 'option_rl_templates_path')
                box=layout.box()
                box.prop(self, 'option_export_folder')
                box.prop(self, 'option_textures_folder')
                box.label(text='Automatically created as a sub folder relative to the saved .blend file. * Do NOT include any "\\".',icon='INFO')
                box.prop(self, 'option_sp_rename')
                box.label(text='Create "//{Textures}/Reallusion/" folder and rename texture files to Reallusion''s naming Conventions".',icon='INFO')
                box=layout.box()
                box.prop(self, 'option_show_rl_toggle')
                box.prop(self, 'option_save_before_export')

class dks_rl_menu(bpy.types.Menu):

    bl_label = " " + bl_info['name']
    bl_idname = "dks_rl.menu"

    def draw(self, context):
            
        layout = self.layout

        layout.operator('dks_rl.import_base',icon="IMPORT")
        layout.operator('dks_rl.import_female',icon="IMPORT")
        layout.operator('dks_rl.import_male',icon="IMPORT")
        layout.separator()
        layout.operator('dks_rl.export_cc',icon="LINK_BLEND")
        layout.operator('dks_rl.export_3dx',icon="EXPORT")
        #layout.operator('dks_rl.export_ic',icon="LINK_BLEND")

def draw_dks_rl_menu(self, context):

        layout = self.layout
        layout.menu(dks_rl_menu.bl_idname,icon="COLLAPSEMENU")

def dks_rl_menu_func_import_base(self, context):
    self.layout.operator("dks_rl.import_base")
def dks_rl_menu_func_import_female(self, context):
    self.layout.operator("dks_rl.import_female")
def dks_rl_menu_func_import_male(self, context):
    self.layout.operator("dks_rl.import_male")
def dks_rl_menu_func_export_cc(self, context):
    self.layout.operator("dks_rl.export_cc")
def dks_rl_menu_func_export_3dx(self, context):
    self.layout.operator("dks_rl.export_3dx")

def dks_rl_draw_btns(self, context):
    
    if context.region.alignment != 'RIGHT':

        layout = self.layout
        row = layout.row(align=True)
        
        if bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle:

                if bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle_state:
                        row.operator(dks_rl_toggle.bl_idname,text="IC",icon="TRIA_LEFT")
                else:
                        row.operator(dks_rl_toggle.bl_idname,text="IC",icon="TRIA_RIGHT")

        if bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle_state or not bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle:

                row.operator("dks_rl.export_cc",text="CC",icon="EXPORT")
                row.operator("dks_rl.export_3dx",text="3DX",icon="EXPORT")
                row.operator("dks_rl.import_base",text="Base",icon="IMPORT")
                row.operator("dks_rl.import_female",text="Female",icon="IMPORT")
                row.operator("dks_rl.import_male",text="Male",icon="IMPORT")

class dks_rl_toggle(bpy.types.Operator):

    bl_idname = "dks_rl.toggle"
    bl_label = "RL"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):

        if not bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle_state:
            bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle_state=True
        else:
            bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle_state=False
        return {'FINISHED'}

classes = (
    dks_rl_addon_prefs,
    dks_rl_toggle,
)

def register():

        from bpy.utils import register_class
        for cls in classes:
                register_class(cls)

        dks_rl.register()

        bpy.types.TOPBAR_MT_file_import.append(dks_rl_menu_func_import_base)
        bpy.types.TOPBAR_MT_file_import.append(dks_rl_menu_func_import_female)
        bpy.types.TOPBAR_MT_file_import.append(dks_rl_menu_func_import_male)
        bpy.types.TOPBAR_MT_file_export.append(dks_rl_menu_func_export_cc)
        bpy.types.TOPBAR_MT_file_export.append(dks_rl_menu_func_export_3dx)

        bpy.context.preferences.addons[__package__].preferences.option_show_rl_toggle_state=False

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.append(dks_rl_draw_btns)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                register_class(dks_rl_menu)
                bpy.types.INFO_HT_header.append(draw_dks_rl_menu)

def unregister():

        bpy.types.TOPBAR_MT_file_import.remove(dks_rl_menu_func_import_base)
        bpy.types.TOPBAR_MT_file_import.remove(dks_rl_menu_func_import_female)
        bpy.types.TOPBAR_MT_file_import.remove(dks_rl_menu_func_import_male)
        bpy.types.TOPBAR_MT_file_export.remove(dks_rl_menu_func_export_cc)
        bpy.types.TOPBAR_MT_file_export.remove(dks_rl_menu_func_export_3dx)

        if bpy.context.preferences.addons[__package__].preferences.option_display_type=='Buttons':

                bpy.types.TOPBAR_HT_upper_bar.remove(dks_rl_draw_btns)

        elif bpy.context.preferences.addons[__package__].preferences.option_display_type=='Menu':

                unregister_class(dks_rl_menu)
                bpy.types.INFO_HT_header.remove(draw_dks_rl_menu)

        dks_rl.unregister()

        from bpy.utils import unregister_class
        for cls in reversed(classes):
                unregister_class(cls)

if __name__ == "__main__":

	register()