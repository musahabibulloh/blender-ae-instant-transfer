bl_info = {
    "name": "Instant AE Camera Transfer",
    "author": "Musa Habibulloh Al Faruq",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > AE Transfer",
    "description": "Instantly transfers the active camera animation to After Effects.",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
import math
import mathutils
import os
import winreg
import subprocess
import tempfile
import json

def find_after_effects():
    try:
        # Check App Paths
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\AfterFX.exe") as key:
            path = winreg.QueryValue(key, None)
            if path and os.path.exists(path):
                return path
    except Exception:
        pass
    
    # Common paths
    program_files = os.environ.get("ProgramW6432", "C:\\Program Files")
    adobe_path = os.path.join(program_files, "Adobe")
    if os.path.exists(adobe_path):
        for folder in os.listdir(adobe_path):
            if "After Effects" in folder:
                exe_path = os.path.join(adobe_path, folder, "Support Files", "AfterFX.exe")
                if os.path.exists(exe_path):
                    return exe_path
    return None

def blender_cam_to_ae(matrix_world, scale, width, height):
    loc, rot, scale_vec = matrix_world.decompose()
    
    # AE Position
    pos_x = width / 2.0 + (loc.x * scale)
    pos_y = height / 2.0 - (loc.z * scale)
    pos_z = loc.y * scale
    
    # Blender Camera Local axes in World space
    right = matrix_world.col[0].xyz
    up = matrix_world.col[1].xyz
    forward = -matrix_world.col[2].xyz  # Blender camera looks down local -Z
    
    # Map these axes to AE World space
    # AE X = Blender X
    # AE Y = -Blender Z
    # AE Z = Blender Y
    ae_right = mathutils.Vector((right.x, -right.z, right.y))
    ae_up = mathutils.Vector((up.x, -up.z, up.y))
    ae_forward = mathutils.Vector((forward.x, -forward.z, forward.y))
    
    # AE camera local axes: X=Right, Y=Down (-Up), Z=Forward
    ae_matrix = mathutils.Matrix()
    ae_matrix.col[0] = ae_right.to_4d()
    ae_matrix.col[1] = (-ae_up).to_4d()
    ae_matrix.col[2] = ae_forward.to_4d()
    ae_matrix.col[3] = mathutils.Vector((0, 0, 0, 1))
    
    ae_euler = ae_matrix.to_euler('XYZ')
    
    rot_x = math.degrees(ae_euler.x)
    rot_y = math.degrees(ae_euler.y)
    rot_z = math.degrees(ae_euler.z)
    
    return [pos_x, pos_y, pos_z], [rot_x, rot_y, rot_z]


class AETRANSFER_OT_send_camera(bpy.types.Operator):
    bl_idname = "aetransfer.send_camera"
    bl_label = "Transfer Camera to After Effects"
    bl_description = "Exports active camera animation and opens it in After Effects"
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'CAMERA'
    
    def execute(self, context):
        scene = context.scene
        cam = context.active_object
        
        if not cam or cam.type != 'CAMERA':
            self.report({'ERROR'}, "Please select a camera first!")
            return {'CANCELLED'}
        
        ae_path = find_after_effects()
        if not ae_path:
            self.report({'ERROR'}, "Could not find After Effects executable!")
            return {'CANCELLED'}
            
        width = scene.render.resolution_x
        height = scene.render.resolution_y
        fps = scene.render.fps / scene.render.fps_base
        scale = scene.ae_transfer_scale
        
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        
        # Save current frame to restore later
        current_frame = scene.frame_current
        
        frames = []
        positions = []
        xRots = []
        yRots = []
        zRots = []
        zooms = []
        
        for f in range(frame_start, frame_end + 1):
            scene.frame_set(f)
            matrix = cam.matrix_world
            
            pos, rot = blender_cam_to_ae(matrix, scale, width, height)
            
            # Zoom
            angle_x = cam.data.angle_x
            zoom = (width / 2.0) / math.tan(angle_x / 2.0)
            
            frames.append(f)
            positions.append(pos)
            xRots.append(rot[0])
            yRots.append(rot[1])
            zRots.append(rot[2])
            zooms.append(zoom)
            
        # Restore frame
        scene.frame_set(current_frame)
        
        # Generate JSX
        jsx_script = f"""
(function(){{
    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {{
        comp = app.project.items.addComp("Blender Scene", {width}, {height}, 1, {frame_end - frame_start + 1}/{fps}, {fps});
    }}
    
    app.beginUndoGroup("Transfer Blender Camera");
    
    var camLayer = comp.layers.addCamera("{cam.name}", [comp.width/2, comp.height/2]);
    camLayer.autoOrient = AutoOrientType.NO_AUTO_ORIENT;
    
    var posProp = camLayer.property("ADBE Transform Group").property("ADBE Position");
    var xRotProp = camLayer.property("ADBE Transform Group").property("ADBE Rotate X");
    var yRotProp = camLayer.property("ADBE Transform Group").property("ADBE Rotate Y");
    var zRotProp = camLayer.property("ADBE Transform Group").property("ADBE Rotate Z");
    var zoomProp = camLayer.property("ADBE Camera Options Group").property("ADBE Camera Zoom");
    
    var fps = comp.frameRate;
    
    var frames = {json.dumps(frames)};
    var positions = {json.dumps(positions)};
    var xRots = {json.dumps(xRots)};
    var yRots = {json.dumps(yRots)};
    var zRots = {json.dumps(zRots)};
    var zooms = {json.dumps(zooms)};
    var frameStart = {frame_start};
    
    for (var i = 0; i < frames.length; i++) {{
        var time = (frames[i] - frameStart) / fps;
        posProp.setValueAtTime(time, positions[i]);
        xRotProp.setValueAtTime(time, xRots[i]);
        yRotProp.setValueAtTime(time, yRots[i]);
        zRotProp.setValueAtTime(time, zRots[i]);
        zoomProp.setValueAtTime(time, zooms[i]);
    }}
    
    app.endUndoGroup();
}})();
"""
        # Save JSX to temp file
        temp_dir = tempfile.gettempdir()
        jsx_path = os.path.join(temp_dir, 'blender_to_ae_transfer.jsx')
        with open(jsx_path, 'w', encoding='utf-8') as f:
            f.write(jsx_script)
            
        # Run After Effects
        try:
            subprocess.Popen([ae_path, '-r', jsx_path])
            self.report({'INFO'}, "Camera sent to After Effects!")
        except Exception as e:
            self.report({'ERROR'}, f"Failed to launch AE: {str(e)}")
            return {'CANCELLED'}
            
        return {'FINISHED'}


class AETRANSFER_PT_panel(bpy.types.Panel):
    bl_label = "Transfer to After Effects"
    bl_idname = "AETRANSFER_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AE Transfer'
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        layout.prop(scene, "ae_transfer_scale", text="Scale (px/unit)")
        layout.separator()
        layout.operator("aetransfer.send_camera", text="Transfer Camera to AE", icon='CAMERA_DATA')


classes = (
    AETRANSFER_OT_send_camera,
    AETRANSFER_PT_panel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.ae_transfer_scale = bpy.props.FloatProperty(
        name="Scale",
        description="Conversion scale (1 Blender unit = X pixels in AE)",
        default=100.0,
        min=1.0
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.ae_transfer_scale

if __name__ == "__main__":
    register()
