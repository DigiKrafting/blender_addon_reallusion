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
from bpy.props import StringProperty

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

                    system('copy /Y "' + _filepath + '" "' + _filepath_copy + '"')

def dks_rl_material_adjustments():

    _objects = bpy.context.scene.objects

    for _obj in _objects:

        if _obj.type=='MESH':

            _obj_name = _obj.name

            if "CC_Base_Body" in _obj_name:

                _materials = _obj.data.materials

                for _material in _materials:

                    if "Std_Eyelash" in _material.name:

                        _material.blend_method = 'MULTIPLY'

def dks_rl_get_texture_file(texture_file):

    if path.exists(texture_file):
        return texture_file
    else:
        return ""

def dks_rl_pbr_nodes(fbx_file):

    _texture_ext="png"
    
    _fbx_folder = path.dirname(fbx_file)
    _fbx_file = path.basename(fbx_file).replace('.Fbx','')

    _objects=bpy.context.selected_objects

    for _obj in _objects:

        if _obj.type=='MESH':

            _obj_name = _obj.name.split(".")[0]

            _materials = _obj.data.materials

            for _material in _materials:

                _material_name = _material.name.split(".")[0]

                _textures_path = _fbx_folder + "\\" + _fbx_file + ".fbm\\"
                
                print(_textures_path+_material_name+'_Diffuse.png')

                _file_Diffuse = dks_rl_get_texture_file(_textures_path+_material_name+'_Diffuse.png')

                if not _file_Diffuse:
                    _file_Diffuse = dks_rl_get_texture_file(_textures_path+_material_name+'_Diffuse.jpg')

                _file_Normal = dks_rl_get_texture_file(_textures_path+_material_name+'_Normal.png')
                _file_Opacity = dks_rl_get_texture_file(_textures_path+_material_name+'_Opacity.png')

                if not _file_Opacity:
                    _file_Opacity = dks_rl_get_texture_file(_textures_path+_material_name+'_Opacity.jpg')
                
                if _obj_name=="CC_Base_Body" or _obj_name=="CC_Base_Tongue":

                    _textures_path = _fbx_folder + "\\textures\\"+_fbx_file+"\\"+_fbx_file+"\\"+_obj_name+"\\"

                    if "Std_Eyelash" in _material_name:

                        _material.blend_method = 'MULTIPLY'

                else:

                    _textures_path = _fbx_folder + "\\textures\\"+_fbx_file+"\\"+_obj_name+"\\"+_obj_name+"\\"

                    if _file_Opacity and _obj_name=="Hair" or "_Hair" in _obj_name or "Hair_" in _obj_name:

                        _material.blend_method = 'BLEND'

                print(_textures_path+_material_name+"\\"+_material_name+'_metallic.png')

                _file_AO = dks_rl_get_texture_file(_textures_path+_material_name+"\\"+_material_name+'_ao.png')
                _file_Metallic = dks_rl_get_texture_file(_textures_path+_material_name+"\\"+_material_name+'_metallic.png')
                _file_Roughness = dks_rl_get_texture_file(_textures_path+_material_name+"\\"+_material_name+'_roughness.png')

                _file_Emissive = "" #dks_rl_get_texture_file(_textures_path,_obj_name,_material_name,'Emissive',_texture_ext)

                if _file_Diffuse:
                    
                    if _material:
                        
                        _material.use_nodes = True

                    # Clear Nodes

                    if _material and _material.node_tree:

                        _nodes = _material.node_tree.nodes

                        for node in _nodes:
                            _nodes.remove(node)

                    _material_links = _material.node_tree.links
                    
                    _nodes = _material.node_tree.nodes

                    # Output Material

                    _material_output = _nodes.new('ShaderNodeOutputMaterial')

                    if not _file_Emissive:
                        _material_output.location = 600,0
                    else:
                        _material_output.location = 1600,0

                    _material_output.name='dks_pbr_output'

                    if _file_Emissive:

                        # Add Shader

                        _node_add_shader=_nodes.new('ShaderNodeAddShader')
                        _node_add_shader.location = 1400,0
                        _node_add_shader.name = 'dks_pbr_add_shader'
                        _material_links.new(_node_add_shader.outputs['Shader'], _material_output.inputs['Surface'])
                        
                        # Shader Emission
                        
                        _node_emission=_nodes.new('ShaderNodeEmission')
                        _node_emission.location = 1200,-100
                        _node_emission.name = 'dks_pbr_emission'
                        _material_links.new(_node_emission.outputs['Emission'], _node_add_shader.inputs[1])

                        # Emissive
                        
                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 800,-100
                        node.name='dks_pbr_texture_emissive'
                        _material_links.new(node.outputs['Color'], _node_emission.inputs['Color'])
                        node.image = bpy.data.images.load(_file_Emissive)

                    # Shader

                    node_shader = _nodes.new('ShaderNodeBsdfPrincipled')
                    node_shader.location = 400,0
                    node_shader.name='dks_pbr_shader'

                    if not _file_Emissive:
                        _material_links.new(node_shader.outputs['BSDF'], _material_output.inputs['Surface'])
                    else:
                        _material_links.new(node_shader.outputs['BSDF'], _node_add_shader.inputs[0])
                    
                    if _file_AO:

                        # Mix RGB

                        node_mix=_nodes.new('ShaderNodeMixRGB')
                        node_mix.location = 200,100
                        node_mix.blend_type = 'MULTIPLY'
                        node_mix.name='dks_pbr_mix_rgb'
                        _material_links.new(node_mix.outputs['Color'], node_shader.inputs['Base Color'])

                        # Base Color

                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 0,250
                        node.name='dks_pbr_texture_base_color'
                        _material_links.new(node.outputs['Color'], node_mix.inputs['Color1'])
                        
                        node.image = bpy.data.images.load(_file_Diffuse)
                        
                        node.image.colorspace_settings.name = 'sRGB'

                        # Ambient Occlusion
                        
                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 0,0
                        node.name='dks_pbr_texture_ao'
                        _material_links.new(node.outputs['Color'], node_mix.inputs['Color2'])
                        node.image = bpy.data.images.load(_file_AO)
                        node.image.colorspace_settings.name = 'Non-Color'
                    
                    else:

                        # Base Color

                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 0,250
                        node.name='dks_pbr_texture_base_color'
                        _material_links.new(node.outputs['Color'], node_shader.inputs['Base Color'])

                        node.image = bpy.data.images.load(_file_Diffuse)
                        
                        node.image.colorspace_settings.name = 'sRGB'

                    # Metallic

                    if _file_Metallic:

                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 0,-250
                        node.name='dks_pbr_texture_metallic'
                        _material_links.new(node.outputs['Color'], node_shader.inputs['Metallic'])   
                        node.image = bpy.data.images.load(_file_Metallic)
                        node.image.colorspace_settings.name = 'Non-Color'

                    # Roughness

                    if _file_Roughness:

                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 0,-500
                        node.name='dks_pbr_texture_roughness'
                        _material_links.new(node.outputs['Color'], node_shader.inputs['Roughness'])   
                        node.image = bpy.data.images.load(_file_Roughness)
                        node.image.colorspace_settings.name = 'Non-Color'

                    # Opacity

                    if _file_Opacity:

                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = 0,-600
                        node.name='dks_pbr_texture_opacity'
                        _material_links.new(node.outputs['Color'], node_shader.inputs['Alpha'])   
                        node.image = bpy.data.images.load(_file_Opacity)
                        node.image.colorspace_settings.name = 'Non-Color'

                    # Normal

                    if _file_Normal:

                        node_map=_nodes.new('ShaderNodeNormalMap')
                        node_map.location = 200,-700
                        node_map.name='dks_pbr_normal_map'
                        _material_links.new(node_map.outputs['Normal'], node_shader.inputs['Normal'])
                        
                        node=_nodes.new('ShaderNodeTexImage')
                        node.location = -100,-750
                        node.name='dks_pbr_texture_normal'
                        _material_links.new(node.outputs['Color'], node_map.inputs['Color'])
                        node.image = bpy.data.images.load(_file_Normal)
                        node.image.colorspace_settings.name = 'Non-Color'

class dks_rl_import_cc(bpy.types.Operator):
    bl_idname = "dks_rl.import_cc"
    bl_label = "Import CC"
    filepath : bpy.props.StringProperty(subtype="FILE_PATH")
    #option_relative : bpy.props.BoolProperty(name="Relative")
    filter_glob : StringProperty(default="*.fbx")
    
    def execute(self, context):

        bpy.ops.import_scene.fbx(filepath = self.filepath, axis_forward='-Z', axis_up='Y')
        
        dks_rl_pbr_nodes(self.filepath)

        return {'FINISHED'}

    def invoke(self, context, event):
        #self.option_relative=context.material.dks_pbr_material_options.option_relative
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

class dks_rl_import_base(bpy.types.Operator):

    bl_idname = "dks_rl.import_base"
    bl_label = "CC Base Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = dks_rl_get_export_path()

        system('copy /Y "' + bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Neutral_Maya_fbx\CC3_Neutral_Maya_fbx.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')

        bpy.ops.import_scene.fbx(filepath = bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Neutral_Maya_fbx\CC3_Neutral_Maya_fbx.Fbx", axis_forward='-Z', axis_up='Y')

        dks_rl_material_adjustments()

        return {'FINISHED'}

class dks_rl_import_female(bpy.types.Operator):

    bl_idname = "dks_rl.import_female"
    bl_label = "CC Female Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = dks_rl_get_export_path()

        system('copy /Y "' + bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Female_Maya_fbx\CC3_Base Female_Maya_fbx.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')
        
        bpy.ops.import_scene.fbx(filepath = bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Female_Maya_fbx\CC3_Base Female_Maya_fbx.Fbx", axis_forward='-Z', axis_up='Y')

        dks_rl_material_adjustments()

        return {'FINISHED'}

class dks_rl_import_male(bpy.types.Operator):

    bl_idname = "dks_rl.import_male"
    bl_label = "CC Male Template (FBX)"

    def execute(self, context):

        _export_name = bpy.path.basename(bpy.context.blend_data.filepath).replace('.blend','')
        _export_path = dks_rl_get_export_path()

        system('copy /Y "' + bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Male_Maya_fbx\CC3_Base Male_Maya_fbx.fbxkey" + '" "' + _export_path + _export_name + '.fbxkey"')

        bpy.ops.import_scene.fbx(filepath = bpy.context.preferences.addons[__package__].preferences.option_rl_templates_path + "Maya\FBX\CC3_Base Male_Maya_fbx\CC3_Base Male_Maya_fbx.Fbx", axis_forward='-Z', axis_up='Y')

        dks_rl_material_adjustments()

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
    dks_rl_import_cc,
)

def register():

    for cls in classes:
        register_class(cls)

def unregister():

    for cls in reversed(classes):
        unregister_class(cls)
  