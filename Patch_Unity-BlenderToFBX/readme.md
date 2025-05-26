Replace this file:
C:\Program Files\Unity\Hub\Editor\{EditorVersion}\Editor\Data\Tools\Unity-BlenderToFBX.py
with the file of the same name found in this directory

then copy the file `BlenderToUnityExportsOnly.cs` from this directory into your Unity Assets folder under a folder called `Editor`, this Editor folder can go anywhere under Assets.
Example location: `Assets/Editor/BlenderToUnityExportsOnly.cs`

this will patch Unity's fbx export script to look for a collection named Export, if this collection is found, everytihng not in the Export collection will be renamed to be prefixed with the string `UnityDestroy__` on FBX export into Unity, and then the Editor script `BlenderToUnityExportsOnly.cs` checks for GameObjects in this import that begin with that prefix and removes them from the import.
This was the only solution I found that works without messing up the Transforms of the objects you wish to keep.

Other solutions I tried:
- Selecting the Export collections as active and then setting `use_active_collection=True` in the fbx script. This messes up the axises.
- - Even using `use_space_transform=true` or `bake_space_transform=true` wouldn't work
- Having the FBX script delete all objects not in the collection before export. This also messes up the axises.

Therefore, removing the non-export objects when Unity imports it is the only way it seems.
