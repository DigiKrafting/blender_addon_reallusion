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
from bpy.utils import register_class, unregister_class
from subprocess import Popen
from os import system, path, makedirs, listdir

texture_names={
    '_Base_Color':'__Diffuse',
    '_Normal_OpenGL':'__Normal',
    '_Ambient_occlusion':'__AO',
    '_Metallic':'__Metallic',    
    '_Roughness':'__Roughness',
    '_Displacement':'__Displacement',
    '_Opacity':'__Opacity',
    '_Emissive':'__Glow',
}

def dks_rl_fbx_export(self, context):

    _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
    _export_path = dks_rl_get_export_path()

    _export_file = _export_path + _export_name + '.fbx'

    if bpy.context.preferences.addons[__package__].preferences.option_save_before_export:
        bpy.ops.wm.save_mainfile()

    bpy.ops.export_scene.fbx(filepath=_export_file, check_existing=False, axis_forward='-Z', axis_up='Y', use_selection=False, object_types={'ARMATURE', 'MESH'}, add_leaf_bones=False, path_mode='COPY', embed_textures=True)
    
    return _export_file

class dks_rl_fbx_export_execute(bpy.types.Operator):

    bl_idname = "dks_rl.fbx_export"
    bl_label = "Export FBX."

    def execute(self, context):

        _export_file = dks_rl_fbx_export(self, context)

        return {'FINISHED'}

def dks_rl_get_export_path():

    _export_path = bpy.path.abspath('//') + bpy.context.preferences.addons[__package__].preferences.option_export_folder + '\\'

    if not path.exists(_export_path):
        makedirs(_export_path)

    return _export_path

def dks_rl_get_textures_path():

    _textures_path = bpy.path.abspath('//') + bpy.context.preferences.addons[__package__].preferences.option_textures_folder + '\\'

    if not path.exists(_textures_path):
        makedirs(_textures_path)

    return _textures_path

def dks_rl_sp_textures_rename():    
    
    _textures_path = dks_rl_get_textures_path()

    if (_textures_path):
        
        _reallusion_path = _textures_path + '\\Reallusion\\'

        if not path.exists(_reallusion_path):
            makedirs(_reallusion_path)

        for filename in listdir(_textures_path):

            for _match in texture_names:

                if _match in filename:

                    _filepath=path.join(_textures_path,filename)
                    _filename = filename.replace(_match,texture_names[_match])
                    _filepath_copy=path.join(_reallusion_path,_filename)

                    system('copy "' + _filepath + '" "' + _filepath_copy + '"')

#texture_names

class dks_rl_import_base(bpy.types.Operator):

    bl_idname = "dks_rl.import_base"
    bl_label = "CC Base Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = dks_rl_get_export_path()

        system('copy "' + bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Neutral_Maya_fbx\CC3_Neutral_Maya_fbx.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')

        bpy.ops.import_scene.fbx(filepath = bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Neutral_Maya_fbx\CC3_Neutral_Maya_fbx.Fbx", axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}

class dks_rl_import_female(bpy.types.Operator):

    bl_idname = "dks_rl.import_female"
    bl_label = "CC Female Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = dks_rl_get_export_path()

        system('copy "' + bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Female_Maya_fbx\CC3_Base Female_Maya_fbx.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')
        
        bpy.ops.import_scene.fbx(filepath = bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Female_Maya_fbx\CC3_Base Female_Maya_fbx.Fbx", axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}

class dks_rl_import_male(bpy.types.Operator):

    bl_idname = "dks_rl.import_male"
    bl_label = "CC Male Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = dks_rl_get_export_path()

        system('copy "' + bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Male_Maya_fbx\CC3_Base Male_Maya_fbx.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')

        bpy.ops.import_scene.fbx(filepath = bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Male_Maya_fbx\CC3_Base Male_Maya_fbx.Fbx", axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}

class dks_rl_export_3dx(bpy.types.Operator):

    bl_idname = "dks_rl.export_3dx"
    bl_label = "3DXchange (FBX)"

    def execute(self, context):

        if bpy.context.preferences.addons[__package__].preferences.option_sp_rename:

            dks_rl_sp_textures_rename()

        export_file = dks_rl_fbx_export(self, context)

        Popen([bpy.context.preferences.addons[__package__].preferences.option_rl_3dx_exe, export_file])

        return {'FINISHED'}

class dks_rl_export_cc(bpy.types.Operator):

    bl_idname = "dks_rl.export_cc"
    bl_label = "Character Creator (FBX)"

    def execute(self, context):

        if bpy.context.preferences.addons[__package__].preferences.option_sp_rename:

            dks_rl_sp_textures_rename()

        export_file = dks_rl_fbx_export(self, context)

        Popen([bpy.context.preferences.addons[__package__].preferences.option_rl_cc_exe, export_file])
        
        return {'FINISHED'}

classes = (
    dks_rl_fbx_export_execute,
    dks_rl_import_base,
    dks_rl_import_female,
    dks_rl_import_male,
    dks_rl_export_cc,
    dks_rl_export_3dx,
)

def register():

    for cls in classes:
        register_class(cls)

def unregister():

    for cls in reversed(classes):
        unregister_class(cls)
  