# 🚀 Blender to After Effects (AE) Instant Camera Transfer

![Blender Version](https://img.shields.io/badge/Blender-3.0%2B-orange?style=flat-square&logo=blender)
![After Effects Version](https://img.shields.io/badge/After_Effects-CC_2018%2B-blue?style=flat-square&logo=adobeaftereffects)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows)

**The fastest, 1-click solution to export and transfer your 3D Camera from Blender directly to Adobe After Effects.** 

Stop wasting time exporting `.jsx` or `.fbx` files manually. This add-on acts as a direct bridge, perfectly translating your Blender camera tracking, animation, and focal length into an After Effects composition in milliseconds.

<p align="center">
  <video src="Readme video.mp4" controls="controls" style="max-width: 100%;"></video>
  <br/>
  <i>(If the video above doesn't load, <a href="https://github.com/musahabibulloh/blender-ae-instant-transfer/raw/main/Readme%20video.mp4">click here to view it</a>)</i>
</p>

## 📑 Table of Contents
- [Why Use This Add-on?](#-why-use-this-add-on)
- [How It Works (Under the Hood)](#-how-it-works-technical-details)
- [Key Features](#-key-features)
- [Installation Guide](#-installation-guide)
- [How to Use](#-how-to-use)
- [Troubleshooting](#-troubleshooting)
- [Author & License](#-author--license)

---

## ⚡ Why Use This Add-on?

Traditionally, sending a camera from Blender to After Effects involves a tedious workflow:
1. Selecting the camera.
2. Going to `File > Export > After Effects (.jsx)`.
3. Finding a place to save the file.
4. Opening After Effects.
5. Going to `File > Scripts > Run Script File...`
6. Finding and importing the `.jsx` file.

**With this add-on:**
1. Select the camera.
2. Click **Transfer Camera to AE**.

*(Done. After Effects opens automatically and places the animated camera directly in your timeline).*

---

## 🛠️ How It Works (Technical Details)

This add-on handles complex coordinate math and system communication automatically:

- **Coordinate Matrix Translation**: Translates Blender's Right-Handed system (Z-Up, Y-Forward) into After Effects' Left-Handed pixel space (Y-Down, Z-Forward) by decomposing the camera's `matrix_world` on every frame.
- **Focal Length & Sensor Conversion**: Automatically calculates the exact After Effects **Zoom (in pixels)** dynamically based on your render resolution and Blender's FOV/Focal Length.
- **Background Execution (IPC)**: The add-on safely queries the Windows Registry (`HKEY_LOCAL_MACHINE`) to dynamically locate `AfterFX.exe`. It generates an ExtendScript (`.jsx`) payload and pushes it to the After Effects process headless.

---

## ✨ Key Features

- 🎯 **Selection-Aware**: It only exports your *Active Selected Camera*. Perfect for complex scenes with multiple cameras.
- ⏱️ **True 1-Click Execution**: No exporting menus, no importing dialogs. 
- 🎬 **Smart Comp Creation**: Automatically injects into your active composition, or creates a new one perfectly matching your Blender render resolution and framerate.
- 🔄 **Dynamic Frame Mapping**: Retains your exact `frame_start` and `frame_end` timing perfectly.

---

## 📥 Installation Guide

1. Download the `blender_to_ae.py` file from this repository.
2. Open Blender.
3. Navigate to **Edit > Preferences > Add-ons**.
4. Click **Install...** and select the downloaded `blender_to_ae.py` file.
5. Check the box next to **Import-Export: Instant AE Camera Transfer** to enable it.

> **Requirements:** Blender 3.0+, Adobe After Effects CC 2018+, and Windows OS.

---

## 🎮 How to Use

1. Open your 3D scene in Blender.
2. Click on the **Camera** you wish to transfer in the 3D Viewport.
3. Press **`N`** on your keyboard to open the Sidebar menu.
4. Click on the **AE Transfer** tab.
5. *(Optional)* Adjust the **Scale** (default `100` means 1 Blender unit = 100 pixels in AE).
6. Click **Transfer Camera to AE**.

---

## 🐛 Troubleshooting

* **Button is greyed out?** Make sure you actually clicked on a Camera object in the 3D viewport.
* **Error: Could not find After Effects?** Ensure After Effects is installed properly on Windows. The script looks for it in standard Adobe directories and the Registry.

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/musahabibulloh/blender-ae-instant-transfer/issues) if you have any ideas to improve this workflow.

## 👤 Author & License

**Musa Habibulloh Al Faruq**  
Distributed under the **MIT License**.

<br>

<div align="center">
  <sub><i>Keywords for searchability: export blender camera to after effects, blender to ae script, b3d to ae, blender camera tracking export, after effects live link, blender to after effects bridge, jsx export alternative, automatic camera transfer.</i></sub>
</div>
