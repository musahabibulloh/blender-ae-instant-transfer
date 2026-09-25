# Blender-to-AE Instant Camera Transfer

**A highly efficient, single-click bridge between Blender 3D and Adobe After Effects for seamless camera animation transfer.**

<p align="center">
  <video src="Readme video.mp4" controls="controls" style="max-width: 100%;"></video>
  <br/>
  <i>(If the video above doesn't load, <a href="https://github.com/musahabibulloh/blender-ae-instant-transfer/raw/main/Readme%20video.mp4">click here to view it</a>)</i>
</p>

## 📖 Overview

When working on motion graphics and 3D animation, seamlessly integrating 3D camera data from Blender into a 2.5D compositing environment like Adobe After Effects has always been tedious. Traditional workflows require exporting `.jsx` or `.fbx` files, manually importing them into AE, and linking scripts. 

**Blender-to-AE Instant Transfer** eliminates this friction. It acts as an automated pipeline that directly extracts the exact animation data from your selected Blender camera, translates the 3D coordinate space, and instantly injects a native Camera Layer into your active After Effects composition via a background command execution.

## 🛠️ How It Works (Under the Hood)

This add-on handles complex coordinate math and system communication automatically:

1. **Mathematical Coordinate Translation**: Blender uses a right-handed system (Z-Up, Y-Forward), whereas After Effects uses a modified left-handed pixel-based system (Y-Down, Z-Forward). The script performs matrix decomposition on the camera's `matrix_world` for every single frame and calculates the exact Euler rotation offsets and positional inversion required to match AE's 3D space.
2. **Focal Length to Zoom Conversion**: After Effects cameras operate on a "Zoom" parameter (in pixels) rather than traditional Focal Length/Field of View. The script calculates the exact zoom value dynamically based on your render resolution and the camera's FOV.
3. **Automated Inter-Process Communication (IPC)**: The add-on safely queries the Windows Registry (`HKEY_LOCAL_MACHINE`) to dynamically locate your specific Adobe After Effects installation path (`AfterFX.exe`). It then generates a temporary ExtendScript (`.jsx`) payload and pushes it to the After Effects process, ensuring your data is transferred whether AE is currently closed, or already running in the background.

## ✨ Core Features

* **True 1-Click Execution**: No exporting, no importing, no browsing for files. One click in Blender, and the camera appears in After Effects.
* **Selection-Aware**: It specifically targets your *Active Object* (if it's a camera). You can have 10 different cameras in a scene and easily transfer only the one you need.
* **Smart Composition Handling**: If an After Effects project/composition is open, the camera will be injected seamlessly into your active composition. If none is open, it generates a new comp matching your Blender render resolution and framerate.
* **Dynamic Frame Mapping**: Accurately maps the `frame_start` and `frame_end` of your scene, ensuring the animation timing remains 1:1.

## 📋 Requirements

* **Blender**: 3.0 or higher.
* **Adobe After Effects**: CC 2018 or newer.
* **Operating System**: Windows (The automated executable location feature relies on the Windows Registry).

## 🚀 Installation

1. Download the `blender_to_ae.py` file from this repository.
2. Open Blender.
3. Navigate to **Edit > Preferences > Add-ons**.
4. Click **Install...** and select the downloaded `blender_to_ae.py` file.
5. Check the box next to **Import-Export: Instant AE Camera Transfer** to enable it.

## 🕹️ Usage

1. Open your scene in Blender.
2. Click on the **Camera** you wish to transfer in the 3D Viewport (ensure it is the active selection).
3. Press the **`N`** key to open the Sidebar menu.
4. Open the **AE Transfer** tab.
5. *(Optional)* Adjust the **Scale** (default `100` means 1 Blender unit translates to 100 pixels in AE).
6. Click the **Transfer Camera to AE** button.

After Effects will immediately process the data and present your animated camera layer.

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

## 👤 Author

**Musa Habibulloh Al Faruq**
