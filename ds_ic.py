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

import bpy

from subprocess import Popen
from os import system, path, makedirs

def ds_ic_fbx_export(self, context):

    _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
    _export_path = ds_ic_get_export_path()

    _export_file = _export_path + _export_name + '.fbx'

    if not bpy.context.user_preferences.addons[__package__].preferences.option_save_before_export:
        bpy.ops.wm.save_mainfile()

    bpy.ops.export_scene.fbx(filepath=_export_file, check_existing=False, axis_forward='-Z', axis_up='Y', filter_glob="*.fbx", version='BIN7400', ui_tab='MAIN', use_selection=False, global_scale=1.0, apply_unit_scale=True, bake_space_transform=False, object_types={'ARMATURE', 'MESH'}, use_mesh_modifiers=True, mesh_smooth_type='OFF', use_mesh_edges=False, use_tspace=False, use_custom_props=False, add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, bake_anim=False, bake_anim_use_all_bones=False, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=False, bake_anim_force_startend_keying=False, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, use_anim=False, use_anim_action_all=False, use_default_take=False, use_anim_optimize=False, anim_optimize_precision=6.0, path_mode='AUTO', embed_textures=True, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True)
    
    return _export_file

class ds_ic_fbx_export_execute(bpy.types.Operator):

    bl_idname = "ds_ic.fbx_export"
    bl_label = "Export FBX."

    def execute(self, context):

        _export_file = ds_ic_fbx_export(self, context)

        return {'FINISHED'}

def ds_ic_get_export_path():

    _export_path = bpy.path.abspath('//') + bpy.context.user_preferences.addons[__package__].preferences.option_export_folder + '\\'

    if not path.exists(_export_path):
        makedirs(_export_path)

    return _export_path

def ds_ic_get_textures_path():

    _textures_path = bpy.path.abspath('//') + bpy.context.user_preferences.addons[__package__].preferences.option_textures_folder + '\\'

    if not path.exists(_textures_path):
        makedirs(_textures_path)

    return _textures_path

class ds_ic_import_base(bpy.types.Operator):

    bl_idname = "ds_ic.import_base"
    bl_label = "iClone Base Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = ds_ic_get_export_path()

        system('copy "' + bpy.context.user_preferences.addons[__package__].preferences.option_ic_templates_path + "Base.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')

        bpy.ops.import_scene.fbx(filepath = bpy.context.user_preferences.addons[__package__].preferences.option_ic_templates_path + "Base.fbx", axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}

class ds_ic_import_female(bpy.types.Operator):

    bl_idname = "ds_ic.import_female"
    bl_label = "iClone Female Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = ds_ic_get_export_path()

        system('copy "' + bpy.context.user_preferences.addons[__package__].preferences.option_ic_templates_path + "Base Female.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')
        
        bpy.ops.import_scene.fbx(filepath = bpy.context.user_preferences.addons[__package__].preferences.option_ic_templates_path + "Base Female.fbx", axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}

class ds_ic_import_male(bpy.types.Operator):

    bl_idname = "ds_ic.import_male"
    bl_label = "iClone Male Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = ds_ic_get_export_path()

        system('copy "' + bpy.context.user_preferences.addons[__package__].preferences.option_ic_templates_path + "Base Male.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')

        bpy.ops.import_scene.fbx(filepath = bpy.context.user_preferences.addons[__package__].preferences.option_ic_templates_path + "Base Male.fbx", axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}

class ds_ic_export_3dx(bpy.types.Operator):

    bl_idname = "ds_ic.export_3dx"
    bl_label = "3DXchange (FBX)"

    def execute(self, context):

        export_file = ds_ic_fbx_export(self, context)

        Popen([bpy.context.user_preferences.addons[__package__].preferences.option_ic_3dx_exe, export_file])

        return {'FINISHED'}

class ds_ic_export_ic(bpy.types.Operator):

    bl_idname = "ds_ic.export_ic"
    bl_label = "Open iClone"

    def execute(self, context):

        Popen([bpy.context.user_preferences.addons[__package__].preferences.option_ic_exe])

        return {'FINISHED'}

class ds_ic_export_cc(bpy.types.Operator):

    bl_idname = "ds_ic.export_cc"
    bl_label = "Character Creator (FBX)"

    def execute(self, context):

        export_file = ds_ic_fbx_export(self, context)

        Popen([bpy.context.user_preferences.addons[__package__].preferences.option_ic_cc_exe])

        return {'FINISHED'}

class ds_ic_toggle(bpy.types.Operator):

    bl_idname = "ds_ic.toggle"
    bl_label = "iClone"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    def execute(self, context):

        if not bpy.context.user_preferences.addons[__package__].preferences.option_show_iclone_toggle_state:
                bpy.context.user_preferences.addons[__package__].preferences.option_show_iclone_toggle_state=True
        else:
                bpy.context.user_preferences.addons[__package__].preferences.option_show_iclone_toggle_state=False
        return {'FINISHED'}

def ds_ic_menu_func_import_base(self, context):
    self.layout.operator(ds_ic_import_base.bl_idname)
def ds_ic_menu_func_import_female(self, context):
    self.layout.operator(ds_ic_import_female.bl_idname)
def ds_ic_menu_func_import_male(self, context):
    self.layout.operator(ds_ic_import_male.bl_idname)
def ds_ic_menu_func_export_cc(self, context):
    self.layout.operator(ds_ic_export_cc.bl_idname)
def ds_ic_menu_func_export_3dx(self, context):
    self.layout.operator(ds_ic_export_3dx.bl_idname)

def ds_ic_toolbar_btn_base(self, context):
    self.layout.operator('ds_ic.import_base',text="Base",icon="IMPORT")
def ds_ic_toolbar_btn_female(self, context):
    self.layout.operator('ds_ic.import_female',text="Female",icon="IMPORT")
def ds_ic_toolbar_btn_male(self, context):
    self.layout.operator('ds_ic.import_male',text="Male",icon="IMPORT")
def ds_ic_toolbar_btn_cc(self, context):
    self.layout.operator('ds_ic.export_cc',text="CC",icon="LINK_BLEND")
def ds_ic_toolbar_btn_3dx(self, context):
    self.layout.operator('ds_ic.export_3dx',text="3DX",icon="EXPORT")
def ds_ic_toolbar_btn_ic(self, context):
    self.layout.operator('ds_ic.export_ic',text="IC",icon="LINK_BLEND")

def register():

    from bpy.utils import register_class

    register_class(ds_ic_fbx_export_execute)

    register_class(ds_ic_import_base)
    register_class(ds_ic_import_female)
    register_class(ds_ic_import_male)
    register_class(ds_ic_export_cc)
    register_class(ds_ic_export_3dx)
    register_class(ds_ic_export_ic)
    register_class(ds_ic_toggle)

    bpy.types.INFO_MT_file_import.append(ds_ic_menu_func_import_base)
    bpy.types.INFO_MT_file_import.append(ds_ic_menu_func_import_female)
    bpy.types.INFO_MT_file_import.append(ds_ic_menu_func_import_male)
    bpy.types.INFO_MT_file_export.append(ds_ic_menu_func_export_cc)
    bpy.types.INFO_MT_file_export.append(ds_ic_menu_func_export_3dx)

    if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Buttons':

        bpy.types.INFO_HT_header.append(ds_ic_toolbar_btn_base)
        bpy.types.INFO_HT_header.append(ds_ic_toolbar_btn_female)
        bpy.types.INFO_HT_header.append(ds_ic_toolbar_btn_male)
        bpy.types.INFO_HT_header.append(ds_ic_toolbar_btn_cc)
        bpy.types.INFO_HT_header.append(ds_ic_toolbar_btn_3dx)
        bpy.types.INFO_HT_header.append(ds_ic_toolbar_btn_ic)

def unregister():

    from bpy.utils import unregister_class

    bpy.types.INFO_MT_file_import.remove(ds_ic_menu_func_import_base)
    bpy.types.INFO_MT_file_import.remove(ds_ic_menu_func_import_female)
    bpy.types.INFO_MT_file_import.remove(ds_ic_menu_func_import_male)
    bpy.types.INFO_MT_file_export.remove(ds_ic_menu_func_export_cc)
    bpy.types.INFO_MT_file_export.remove(ds_ic_menu_func_export_3dx)

    if bpy.context.user_preferences.addons[__package__].preferences.option_display_type=='Buttons':

        bpy.types.INFO_HT_header.remove(ds_ic_toolbar_btn_base)
        bpy.types.INFO_HT_header.remove(ds_ic_toolbar_btn_female)
        bpy.types.INFO_HT_header.remove(ds_ic_toolbar_btn_male)
        bpy.types.INFO_HT_header.remove(ds_ic_toolbar_btn_cc)
        bpy.types.INFO_HT_header.remove(ds_ic_toolbar_btn_3dx)
        bpy.types.INFO_HT_header.remove(ds_ic_toolbar_btn_ic)  

    unregister_class(ds_ic_toggle)
    unregister_class(ds_ic_fbx_export_execute)
    unregister_class(ds_ic_import_base)
    unregister_class(ds_ic_import_female)
    unregister_class(ds_ic_import_male)
    unregister_class(ds_ic_export_cc)
    unregister_class(ds_ic_export_3dx)
    unregister_class(ds_ic_export_ic)

  