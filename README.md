# Blender Addon Reallusion

Pipeline/Workflow import/export for Character Creator (CC) and export to 3DXchange for iClone.

\* Updated to Blender 2.80.0 Beta

# Features

- One click CC Base FBX Template Import (Copies "Base.fbxkey" to export folder and renames it to the Blender "filename.fbxkey")
- One click CC Female FBX Template Import (Copies "Base Female.fbxkey" to export folder and renames it to the Blender "filename.fbxkey")
- One click CC Male FBX Template Import (Copies "Base Male.fbxkey" to export folder and renames it to the Blender "filename.fbxkey")
- Sets eyelash material to Blend Mode 'MULTIPLY' (* See screenshot below)

## 3DXchange

- One click 3DXchange FBX Export (Exports scene to export folder and opens file in 3DXchange)

## Character Creator

- Application Link to Open CC (Exports scene to export folder before opening CC for manual import)
- Export option to create "//{Textures}/Reallusion/" folder and copy/rename texture files to Reallusion''s naming Conventions for import (* See CC screenshot below)
- Import CC character (fbx) and setup PBR materials using the Principled BSDF shader.

# Required Blender Version

Blender 2.80.0+

blender_addon_reallusion 1.2.0+

2.80.0

Prior to blender_addon_reallusion 1.2.0

2.79.0

# IMPORTANT USAGE NOTES 

\* Make sure you have a saved .blend file before using the auto import/export features, then saving before import/export is then not required. The addon needs the file location to know where to create the export and textures folder used for import/export of the files.

- File Naming Convention

    File names are derived from the selected object name or your blender file name.

# Installation

CC3 Templates [https://www.reallusion.com/character-creator/custom-outfit.html]

\* In preferences set the "iClone Templates Path" to the base folder of CC3_Body_Templates, e.g. C:\CC3_Body_Templates\

Download either the tar.gz or zip from [https://github.com/DigiKrafting/blender_addon_reallusion/releases/latest](https://github.com/DigiKrafting/blender_addon_reallusion/releases/latest)

Installing an Addon in Blender

- [File]->[User Preferences]
- Select [Add-ons] Tab
- Click [Install Add-on from File..]

# Character Creator

## Outfits_Male Avatar (* No changes/conforming)

![alt](/screenshots/cc_male.png)

## Export Configuration

![alt](/screenshots/cc_export.png)

## Default Blender FBX Import (* Default Scene Setup/Lighting)

![alt](/screenshots/cc_import_default.png)

## FBX Import via this Addon (* Default Scene Setup/Lighting)

![alt](/screenshots/cc_import_pbr.png)

# Screenshots

## CC Template Eyelash Opacity

![alt](/screenshots/rl_eyelash.png)

## CC Textures Import

![alt](/screenshots/rl_textures.png)

## Preferences

![alt](/screenshots/ic_prefs.png)

## Blender 2.79 

![alt](/screenshots/ic.png)

# 3DXchange

## Blender to 3DXchange

![alt](/screenshots/3dx_cc_blender.png)

## 3DXchange to iClone

![alt](/screenshots/3dx_cc_3dx.png)

## iClone

![alt](/screenshots/3dx_cc_iclone.png)

