# Blender AE Instant Transfer

Instantly transfer your Blender camera animation to Adobe After Effects without manually exporting and importing `.jsx` files! 

## Demo Video
<video src="Readme video.mp4" controls="controls" style="max-width: 100%;"></video>

*(If the video above doesn't load on some devices, [click here to view it](https://github.com/musahabibulloh/blender-ae-instant-transfer/raw/main/Readme%20video.mp4))*

## ✨ Features
- **1-Click Transfer**: Select your camera, click "Transfer Camera to AE", and After Effects will instantly open with your animated camera ready to go!
- **Selection-Based**: Transfers the exact camera you select, perfect for scenes with multiple cameras.
- **Perfect Accuracy**: Translates Blender's (Z-up, Y-forward) coordinate system to After Effects' (Y-down, Z-forward) system flawlessly.
- **Automated**: Automatically locates `AfterFX.exe` on your Windows system and handles all the `.jsx` generation in the background.

## ⚙️ Installation
1. Download `blender_to_ae.py` from this repository.
2. Open Blender.
3. Go to **Edit > Preferences** and select the **Add-ons** tab.
4. Click **Install...** and select the `blender_to_ae.py` file.
5. Check the box next to **Import-Export: Instant AE Camera Transfer** to enable the add-on.

## 🚀 How to Use
1. Select the Camera you want to transfer in the 3D Viewport.
2. Press the `N` key to open the Sidebar.
3. Navigate to the new **AE Transfer** tab on the right side.
4. (Optional) Adjust the Scale. The default is `100` (1 Blender unit = 100 pixels in AE).
5. Click **Transfer Camera to AE**.

That's it! If After Effects is already open, it will instantly add the camera to your active composition (or create a new one). If it isn't open, it will automatically launch and do the setup for you.

## 👤 Author
**Musa Habibulloh Al Faruq**
