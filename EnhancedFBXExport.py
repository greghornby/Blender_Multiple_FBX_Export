import bpy
import os

bl_info = {
 "name": "Enhanced FBX Exporter",
 "description": "Export individual fbx files",
 "author": "Greg Hornby",
 "blender": (2, 7, 8),
 "version": (1, 0, 0),
 "category": "FBX",
 "location": "",
 "warning": "",
 "wiki_url": "",
 "tracker_url": "",
}

def SelectChildren(parentObj):
    for obj in bpy.data.objects:
        if obj.type == "MESH" and obj.parent == parentObj:
            obj.select = True
            SelectChildren(obj)


class FBXBatchExportPanel(bpy.types.Panel):

    bl_idname = "Enhanced_FBX"
    bl_label = "FBX"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        layout = self.layout

        # batch export
        col = layout.column(align=True)
        col.label(text="Batch export:")
        col.prop(context.scene, 'gh_batch_export_path')
        row = col.row(align=True)
        row.operator("gh.batch_export", text="Batch Export", icon='EXPORT')

        #Options
        col = layout.column(align=True)
        col.label(text="Options")
        col.prop(context.scene, 'gh_group_children')
        row = col.row(align=True)


class GHBatchExport(bpy.types.Operator):
    bl_idname = "gh.batch_export"
    bl_label = "Choose Directory"

    def execute(self, context):
        print ("execute GH_batch_export")

        basedir = os.path.dirname(bpy.data.filepath)
        if not basedir:
            raise Exception("Blend file is not saved")

        if context.scene.gh_batch_export_path == "":
            raise Exception("Export path not set")

        # Select all visible meshes
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.select_by_type(type='MESH')
        col = bpy.context.selected_objects

        # Get directory path
        dirname = os.path.dirname(bpy.path.abspath(context.scene.gh_batch_export_path))
        # cursor to origin
        bpy.context.scene.cursor_location = (0.0, 0.0, 0.0)

        for obj in col:

            # Skip if custom property "exportFBX" set to 0 (False)
            if "exportFBX" in obj and obj["exportFBX"] == 0:
                continue
            
            if context.scene.gh_group_children == True and obj.parent is not None:
                continue
            
            # Select only current object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select = True

            if context.scene.gh_group_children == True:
                 SelectChildren(obj)

            # freeze rotation and scale
            # bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            name = bpy.path.clean_name(obj.name)
            filename = os.path.join(dirname, name)
            print("Exporting: " + filename)

            # Export .fbx
            bpy.ops.export_scene.fbx(filepath=filename + ".fbx", use_selection=True, axis_forward='-Z', axis_up='Y')

        return {'FINISHED'}



def register():
    bpy.types.Scene.gh_batch_export_path = bpy.props.StringProperty (
        name="Export Path",
        default="",
        description="Define the path where to export",
        subtype='DIR_PATH'
    )
    bpy.types.Scene.gh_group_children = bpy.props.BoolProperty (
        name="Group Children",
        default=True,
        description="Group parent/children objects into the same exported file"
    )
    bpy.utils.register_class(FBXBatchExportPanel)
    bpy.utils.register_class(GHBatchExport)


def unregister():
    del bpy.types.Scene.gh_batch_export_path
    del bpy.types.Scene.gh_group_children
    bpy.utils.unregister_class(FBXBatchExportPanel)
    bpy.utils.unregister_class(GHBatchExport)

if __name__ == "__main__":
    register()
