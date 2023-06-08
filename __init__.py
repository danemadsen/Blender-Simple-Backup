bl_info = {
    "name": "Simple Backup",
    "author": "Dane Madsen",
    "version": (1, 0),
    "blender": (3, 4, 0),
    "location": "File > Save Backup",
    "description": "Saves a backup of the current project",
    "category": "System",
}

import bpy
import os
import re

class SimpleBackupOperator(bpy.types.Operator):
    bl_idname = "object.simple_backup"
    bl_label = "Save Backup"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        filepath = bpy.data.filepath
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        project_name = os.path.splitext(filename)[0]

        backup_dir = os.path.join(directory, "bak")
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)

        regex = re.compile(rf"^{project_name}Bak(\d+)\.blend$")
        backup_number = max(
            (
                int(m.group(1))
                for m in map(regex.match, os.listdir(backup_dir))
                if m is not None
            ),
            default=0,
        ) + 1

        backup_filename = f"{project_name}Bak{backup_number}.blend"
        backup_path = os.path.join(backup_dir, backup_filename)
        bpy.ops.wm.save_as_mainfile(filepath=backup_path, copy=True)
        self.report({'INFO'}, f'Saved backup to {backup_path}')

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleBackupOperator.bl_idname)

def register():
    bpy.utils.register_class(SimpleBackupOperator)
    bpy.types.TOPBAR_MT_file.append(menu_func)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Window')
    kmi = km.keymap_items.new(SimpleBackupOperator.bl_idname, 'S', 'PRESS', ctrl=True, alt=True)

def unregister():
    bpy.utils.unregister_class(SimpleBackupOperator)
    bpy.types.TOPBAR_MT_file.remove(menu_func)
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps['Window']
    km.keymap_items.remove(km.keymap_items[SimpleBackupOperator.bl_idname])

if __name__ == "__main__":
    register()
