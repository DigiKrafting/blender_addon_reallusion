# Blender Addon Reallusion

Pipeline/Workflow import/export for Character Creator (CC) and export to 3DXchange for iClone.

\* Updated to Blender 2.80.0 Beta

# Features

- One click CC Base FBX Template Import (Copies "Base.fbxkey" to export folder and renames it to the Blender "filename.fbxkey")
- One click CC Female FBX Template Import (Copies "Base Female.fbxkey" to export folder and renames it to the Blender "filename.fbxkey")
- One click CC Male FBX Template Import (Copies "Base Male.fbxkey" to export folder and renames it to the Blender "filename.fbxkey")
- Option to create "//{Textures}/Reallusion/" folder and copy/rename texture files to Reallusion''s naming Conventions for import (* See CC screenshot below)

## 3DXchange

- One click 3DXchange FBX Export (Exports scene to export folder and opens file in 3DXchange)

## Character Creator

- Application Link to Open CC (Exports scene to export folder before opening CC for manual import)

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

Download either the tar.gz or zip from [https://github.com/DigiKrafting/reallusion/releases/latest](https://github.com/DigiKrafting/reallusion/releases/latest)

Installing an Addon in Blender

- [File]->[User Preferences]
- Select [Add-ons] Tab
- Click [Install Add-on from File..]

# Screenshots

![alt](/screenshots/ic_prefs.png)

![alt](/screenshots/ic.png)

![alt](/screenshots/rl_textures.png)
