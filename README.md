# m_Scripts_1.0 C4D

A collection of Python scripts for Cinema 4D. These scripts provide various functionalities to enhance and speedup your workflow. Some are mostly shorcuts to simple tasks.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
  - [Animation](#animation)
  - [Modeling](#modeling)
  - [Object Manager](#object-manager)
  - [Render](#render)
  - [Utility](#utility)

# Installation

Download or clone this repository to your local machine.

#### Windows
`C:\Users\<USER>\AppData\Roaming\MAXON\Maxon Cinema 4D 2025\library\scripts`

#### Mac OS
`/Applications/MAXON/CINEMA 4D 2025/library/scripts`

### Using scripts
After you have installed m_Scripts you have to reboot Cinema 4D if it is already running. Scripts are located under Extensions -> User Scripts -> M_Scripts_#.##. Scripts can be used with the commander (Shift+C) too.

Some of the scripts have multiple functions and you can use those with key modifiers (Alt / Ctrl / Shift) and different combinations. Some of the scripts requires a certain item selection or mode to be active. If you don't know what the script does you can either open the script in the script editor and read the description or search the info of the specific script on this page.

# Scripts Overview

## Animation

#### <img src="img/m_AnimCurve_Constant.png" alt="AnimCurve Constant" class="icon"> AnimCurve Constant

*-* Makes the animation curve constant before and after.

#### <img src="img/m_AnimCurve_RepeatAfter.png" alt="AnimCurve Repeat After" class="icon"> AnimCurve Repeat After

*-* Repeats the animation curve before and after.

## Modeling

#### <img src="img/m_AlignSelected_X.png" alt="Align Selected X" class="icon"> Align Selected X

*-* Aligns selected vertices on the X axis.

#### <img src="img/m_AlignSelected_Y.png" alt="Align Selected Y" class="icon"> Align Selected Y

*-* Aligns selected vertices on the Y axis.

#### <img src="img/m_AlignSelected_Z.png" alt="Align Selected Z" class="icon"> Align Selected Z

*-* Aligns selected vertices on the Z axis.

#### <img src="img/m_AlignZeroSelected_X.png" alt="Align Zero Selected X" class="icon"> Align Zero Selected X

*-* Aligns selected vertices to the origin on the X axis.

#### <img src="img/m_AlignZeroSelected_Y.png" alt="Align Zero Selected Y" class="icon"> Align Zero Selected Y

*-* Aligns selected vertices to the origin on the Y axis.

#### <img src="img/m_AlignZeroSelected_Z.png" alt="Align Zero Selected Z" class="icon"> Align Zero Selected Z

*-* Aligns selected vertices to the origin on the Z axis.


## Object Manager

#### <img src="img/m_AlignToSelected.png" alt="Align To Selected" class="icon"> Align To Selected

*-* Aligns the first selected object to the second selected object.

#### <img src="img/m_CopyDisplayColor.png" alt="Copy Display Color" class="icon"> Copy Display Color

*-* Copies the display color from the first selected object to the second selected object.

#### <img src="img/m_CopyColortoChild.png" alt="Copy Color to Child" class="icon"> Copy Color to Child

*-* Copies the display color from the parent to the children of selected objects.

#### <img src="img/m_RandomColor_Group.png" alt="Random Color Group" class="icon"> Random Color Group

*-* Sets a random display color to the current object or tag selection.

#### <img src="img/m_CopyMaterialTags_Hierarchy.png" alt="Copy Material Tags Hierarchy" class="icon"> Copy Material Tags Hierarchy

*-* Copies material tags from one hierarchy to another with the same objects.

#### <img src="img/m_PasteNexto.png" alt="Paste Next to" class="icon"> Paste Next to

*-* Pastes objects next to the selected object in the object manager. *Recommended to use with shortcut*

#### <img src="img/m_Pasteaschild.png" alt="Paste as Child" class="icon"> Paste as Child

*-* Pastes objects as children of the current selection. *Recommended to use with shortcut*

#### <img src="img/m_SelectChildren.png" alt="Select Children" class="icon"> Select Children

*-* Selects the children of the selected objects.

#### <img src="img/m_HierarchyMoveDN.png" alt="Hierarchy Move Down" class="icon"> Hierarchy Move Down

*-* Moves selected objects down in the hierarchy.

#### <img src="img/m_HierarchyMoveUP.png" alt="Hierarchy Move Up" class="icon"> Hierarchy Move Up

*-* Moves selected objects up in the hierarchy.

#### <img src="img/m_SceneArrange.png" alt="Scene Arrange" class="icon"> Scene Arrange

*-* Groups objects in the scene into categories under new null objects. *Still needs some improvement*

#### <img src="img/m_SceneArrangeCloners.png" alt="Scene Arrange Cloners" class="icon"> Scene Arrange Cloners

*-* Groups each selected cloner and its effectors under a new null object.

## Render Setup

#### <img src="img/m_RenderSetup_1-1.png" alt="Render Set 1-1" class="icon"> Render Set 1-1

*-* Sets the render resolution to 1920x1920.

#### <img src="img/m_RenderSetup_16-9.png" alt="Render Set 16-9" class="icon"> Render Set 16-9

*-* Sets the render resolution to 1920x1080.

#### <img src="img/m_RenderSetup_9-16.png" alt="Render Set 9-16" class="icon"> Render Set 9-16

*-* Sets the render resolution to 1080x1920.

#### <img src="img/m_RenderSetup_CurrentFrame.png" alt="Render Set Current Frame" class="icon"> Render Set Current Frame

*-* Sets the frame range to "Current Frame".

#### <img src="img/m_RenderSet_PreviewRange.png" alt="Render Set Preview Range" class="icon"> Render Set Preview Range

*-* Sets the frame range to "Preview Range".

#### <img src="img/m_rsSet_BaseSetting.png" alt="Sampling CTRL" class="icon"> Quick Redshift Render Setting Preset

*-* Configures the Redshift renderer to a Basic quick render setting:

1. Disables automatic sampling.
2. Sets cutoff thresholds to 0.01.
3. Sets the adaptive error threshold to 0.1.
4. Sets the maximum samples for unified sampling and other related parameters to 32.
5. Configures the secondary Global Illumination (GI) engine to Brute Force and sets the number of rays.
6. Sets the block size to 512.

*Make sure to set Render Mode to **Advanced***

#### <img src="img/m_rsSet_SamplingCTRL.png" alt="Sampling CTRL" class="icon"> Sampling CTRL

*-* Multiplies by x2 the "Unified Max Samples" Sampling overrides and Brute Force Rays. <br> *If "Sampling Overrides" are higher than Unified Max Samples it will multiply this value by x2, otherwise it will take Max Samples value* <br> *-* If ALT is pressed, the sampling values are halved; instead of doubled. 

#### <img src="img/m_rsSet_Bucket64.png" alt="Bucket 64" class="icon"> Bucket 64

*-* Sets the Redshift bucket size to 64.

#### <img src="img/m_rsSet_Bucket512.png" alt="Bucket 512" class="icon"> Bucket 512

*-* Sets the Redshift bucket size to 512.

#### <img src="img/m_rsSet_CutoffThresholds_Q.png" alt="Cutoff Thresholds Q" class="icon"> Cutoff Thresholds Q

*-* Sets the cutoff thresholds for Redshift renderer to 0.01 to speedup rendering. <br>
*Use with Caution may introduce fireflyes in certain scenarios*

#### <img src="img/m_rsSet_SamplingThresh_0x005.png" alt="Sampling Thresh 0x005" class="icon"> Sampling Threshold 0.005

*-* Sets the Redshift sampling threshold to 0.005.

#### <img src="img/m_rsSet_SamplingThresh_0x01_1.png" alt="Sampling Threshold 0x1" class="icon"> Sampling Threshold 0.01

*-* Sets the Redshift sampling threshold to 0.01.

#### <img src="img/m_rsSet_SamplingThresh_0x01.png" alt="Sampling Thresh 0x01" class="icon"> Sampling Threshold 0.1

*-* Sets the Redshift sampling threshold to 0.1.

#### <img src="img/m_rsSet_SamplingThresh_1.png" alt="Sampling Threshold 1" class="icon"> Sampling Threshold 1

*-* Sets the Redshift sampling threshold to 1.

## Utility

#### <img src="img/m_CameraGridToggle.png" alt="Camera Grid Toggle" class="icon"> Camera Grid Toggle

*-* Toggles the camera grid on and off. *Recommended to use with shortcut*

#### <img src="img/m_BoundingBox_SelectedObjects.png" alt="Bounding Box Selected Objects" class="icon"> Bounding Box Selected Objects

*-* Creates a bounding box around selected objects.

#### <img src="img/m_FFD_SelectedObjs.png" alt="FFD Selected Objects" class="icon"> FFD Selected Objects

*-* Adds an FFD object to selected objects.

#### <img src="img/m_FFDtoNulls.png" alt="FFD to Nulls" class="icon"> FFD to Nulls

*-* Converts FFD points to nulls.

#### <img src="img/m_FFD_SelectedVerts.png" alt="FFD Selected Verts" class="icon"> FFD Selected Verts

*-* Adds an FFD object to selected vertices.

#### <img src="img/m_FFDtoNulls.png" alt="FFD to Nulls" class="icon"> FFD to Nulls

*-* Converts FFD vertices into Null objects.

#### <img src="img/m_FFD_SelectedObjs.png" alt="FFD Selected Objs" class="icon"> FFD Selected Objs

*-* Adds FFD object to selected objects.

#### <img src="img/m_VisibilityToggle.png" alt="Visibility Toggle" class="icon"> Visibility Toggle

*-* Toggles the visibility of selected objects. *Recommended to use with shortcut Shift+V*

#### <img src="img/m_ViewportClean.png" alt="Viewport Clean" class="icon"> Viewport Clean

*-* Cleans up the viewport by toggling various display options. *Recommended to use with shortcut*

#### <img src="img/m_Reset Visibility.png" alt="Reset Visibility" class="icon"> Reset Visibility

*-* Resets the visibility of selected objects.

#### <img src="img/m_ResetRotation.png" alt="Reset Rotation" class="icon"> Reset Rotation

*-* Resets the rotation of selected objects.

#### <img src="img/m_RemoveEmptyNulls.png" alt="Remove Empty Nulls" class="icon"> Remove Empty Nulls

*-* Removes empty null objects from the scene.

#### <img src="img/m_BatchExportObjects.png" alt="Batch Export Objects" class="icon"> Batch Export Objects

Batch exports selected objects to file root as selected format.

#### <img src="img/m_ViewportClean.png" alt="Viewport Clean" class="icon"> Viewport Clean

*-* Cleans up the viewport by toggling various display options.

# License

This project is licensed under the Creative Commons Legal Code CC0 1.0 Universal. See the [LICENSE](LICENSE) file for details.
