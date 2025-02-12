# Cinema 4D Python Scripts

This repository contains a collection of Python scripts for use with Cinema 4D. These scripts provide various functionalities to enhance your workflow in Cinema 4D.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
  - [Animation](#animation)
    - [AnimCurve Constant](#animationm_animcurve_constantpy)
    - [AnimCurve Repeat After](#animationm_animcurve_repeatafterpy)
  - [Modeling](#modeling)
    - [Align Selected X](#modelingm_align-selected-xpy)
    - [Align Selected Y](#modelingm_align-selected-ypy)
    - [Align Selected Z](#modelingm_align-selected-zpy)
    - [Align To Selected](#modelingm_aligntoselectedpy)
    - [Align Zero Selected X](#modelingm_alignzero-selected-xpy)
    - [Align Zero Selected Y](#modelingm_alignzero-selected-ypy)
    - [Align Zero Selected Z](#modelingm_alignzero-selected-zpy)
  - [Object Manager](#object-manager)
    - [Copy Display Color](#object-managerm_copydisplaycolorpy)
    - [Copy Color to Child](#object-managerm_copycolortochildpy)
    - [Copy Material Tags Hierarchy](#object-managerm_copymaterialtags_hierarchypy)
    - [Paste Next to](#object-managerm_pastenextopy)
    - [Select Children](#object-managerm_select-childrenpy)
    - [Scene Arrange](#object-managerm_scenearrangepy)
    - [Scene Arrange Cloners](#object-managerm_scenearrangeclonerspy)
    - [Reset Visibility](#object-managerm_reset-visibilitypy)
    - [Reset Rotation](#object-managerm_resetrotationpy)
    - [Visibility Toggle](#object-managerm_visibilitytogglepy)
  - [Render](#render)
    - [Render Set 1-1](#renderm_renderset-1-1py)
    - [Render Set 16-9](#renderm_renderset-16-9py)
    - [Render Set 9-16](#renderm_renderset-9-16py)
    - [Render Set Current Frame](#renderm_renderset_currentframepy)
    - [Render Set Preview Range](#renderm_renderset_previewrangepy)
    - [Render Set Save ON OFF](#renderm_renderset_save-on-offpy)
    - [Render Set Save ON OFF v02](#renderm_renderset_save-on-off_v02py)
    - [Sampling Lower](#renderm_rset_samplinglowerpy)
    - [Sampling CTRL](#renderm_rset_samplingctrlpy)
    - [Bucket 64](#renderm_rsset_bucket64py)
    - [Cutoff Thresholds Q](#renderm_rsset_cutoffthresholds_qpy)
    - [Bucket 512](#renderm_rsset_bucket512py)
    - [Sampling Thresh 0x01](#renderm_rsset_samplingthresh_0x01py)
    - [Sampling Thresh 0x005](#renderm_rsset_samplingthresh_0x005py)
    - [Sampling Thresh 0x1](#renderm_rsset_samplingthresh_0x1py)
    - [Sampling Thresh 1](#renderm_rsset_samplingthresh_1py)
  - [Utility](#utility)
    - [Convert Hair to Spline](#utilityconvert-hair-to-splinepy)
    - [Bounding Box Selected Objects](#utilitym_boundingbox_selectedobjectspy)
    - [Camera Grid Toggle](#utilitym_cameragridtoggle_01py)
    - [FFD Selected Objects](#utilitym_ffd_selectedobjspy)
    - [FFD to Nulls](#utilitym_ffd-to-nulls_01py)
    - [Paste as Child](#utilitym_paste-as-childpy)
    - [Hierarchy Move Down](#utilitym_hierarchymovednpy)
    - [Hierarchy Move Up](#utilitym_hierarchymoveuppy)
    - [Viewport Clean](#utilitym_viewportclean_01py)
    - [Swap Index Number](#utilitym_swapindexnumberpy)
    - [Points to Circle](#utilitypoints2circlepy)
    - [Point Auto Rig](#utilitypoint_autorigpy)
    - [Remove Empty Nulls](#utilityremove-empty-nullspy)
    - [Random Color Group](#utilitym_randomcolor_grouppy)
    - [Batch Export Objects](#utilitym_batchexportobjectspy)
    - [FFD Selected Verts](#utilitym_ffd_selectedvertspy)
    - [Car Generator](#utilitym_cargeneratorpy)
    - [FFD to Nulls](#utilitym_ffd_to_nullspy)
    - [FFD Selected Objs](#utilitym_ffd_selectedobjspy)
    - [Hierarchy Move DN](#utilitym_hierarchymovednpy)
    - [Hierarchy Move UP](#utilitym_hierarchymoveuppy)
    - [Paste as Child](#utilitym_paste_as_childpy)
    - [Viewport Clean](#utilitym_viewportclean_01py)

## Installation

Download or clone this repository to your local machine.

#### Windows
`C:\Users\<USER>\AppData\Roaming\MAXON\Maxon Cinema 4D 2024\library\scripts`

#### Mac OS
`/Applications/MAXON/CINEMA 4D 2024/library/scripts`

### Using scripts
After you have installed m_Scripts you have to reboot Cinema 4D if it is already running. Scripts are located under Extensions -> User Scripts -> M_Scripts_#.##. Scripts can be used with the commander (Shift+C) too.

Some of the scripts have multiple functions and you can use those with key modifiers (Alt / Ctrl / Shift) and different combinations. Some of the scripts requires a certain item selection or mode to be active. If you don't know what the script does you can either open the script in the script editor and read the description or search the info of the specific script on this page.

## Scripts

### Animation

#### AnimCurve Constant

Repeats the animation curve after and before.

#### AnimCurve Repeat After

Repeats the animation curve after and before.

### Modeling

#### Align Selected X

Aligns selected vertices on the X axis.

#### Align Selected Y

Aligns selected vertices on the Y axis.

#### Align Selected Z

Aligns selected vertices on the Z axis.

#### Align To Selected

Aligns the first selected object to the second selected object.

#### Align Zero Selected X

Aligns selected vertices to the origin on the X axis.

#### Align Zero Selected Y

Aligns selected vertices to the origin on the Y axis.

#### Align Zero Selected Z

Aligns selected vertices to the origin on the Z axis.

### Object Manager

#### Copy Display Color

Copies the display color from the first selected object to the second selected object.

#### Copy Color to Child

Copies the display color from the parent to the children of selected objects.

#### Copy Material Tags Hierarchy

Copies material tags from one hierarchy to another with the same objects.

#### Paste Next to

Pastes objects next to the selected object in the object manager.

#### Select Children

Selects the children of the selected objects.

#### Scene Arrange

Arranges the scene objects.

#### Scene Arrange Cloners

Arranges the scene cloners.

#### Reset Visibility

Resets the visibility of selected objects.

#### Reset Rotation

Resets the rotation of selected objects.

#### Visibility Toggle

Toggles the visibility of selected objects.

### Render

#### Render Set 1-1

Sets the render resolution to 1920x1920.

#### Render Set 16-9

Sets the render resolution to 1920x1080.

#### Render Set 9-16

Sets the render resolution to 1080x1920.

#### Render Set Current Frame

Sets the frame range to "Current Frame".

#### Render Set Preview Range

Sets the frame range to "Preview Range".

#### Render Set Save ON OFF

Toggles the save output on and off.

#### Render Set Save ON OFF v02

Toggles the save output on and off with a command plugin.

#### Sampling Lower

Lowers the sampling threshold for Redshift renderer.

#### Sampling CTRL

Controls the sampling threshold for Redshift renderer with keyboard modifiers.

#### Bucket 64

Sets the Redshift bucket size to 64.

#### Cutoff Thresholds Q

Sets the cutoff thresholds for Redshift renderer.

#### Bucket 512

Sets the Redshift bucket size to 512.

#### Sampling Thresh 0x01

Sets the Redshift sampling threshold to 0.01.

#### Sampling Thresh 0x005

Sets the Redshift sampling threshold to 0.005.

#### Sampling Thresh 0x1

Sets the Redshift sampling threshold to 0.1.

#### Sampling Thresh 1

Sets the Redshift sampling threshold to 1.

### Utility

#### Convert Hair to Spline

Converts a selected Hair object to a spline.

#### Bounding Box Selected Objects

Creates a bounding box around selected objects.

#### Camera Grid Toggle

Toggles the camera grid on and off.

#### FFD Selected Objects

Adds an FFD object to selected objects.

#### FFD to Nulls

Converts FFD points to nulls.

#### Paste as Child

Pastes objects as children of the current selection.

#### Hierarchy Move Down

Moves selected objects down in the hierarchy.

#### Hierarchy Move Up

Moves selected objects up in the hierarchy.

#### Viewport Clean

Cleans up the viewport by toggling various display options.

#### Swap Index Number

Swaps the index number of points.

#### Points to Circle

Converts selected points to a circle.

#### Point Auto Rig

Automatically rigs points with nulls.

#### Remove Empty Nulls

Removes empty null objects from the scene.

#### Random Color Group

Sets a random display color to the current object or tag selection.

#### Batch Export Objects

Batch exports selected objects to file root as selected format.

#### FFD Selected Verts

Adds an FFD object to selected vertices.

#### Car Generator

Generates a random car model.

#### FFD to Nulls

Converts FFD vertices into Null objects.

#### FFD Selected Objs

Adds FFD object to selected objects.

#### Hierarchy Move DN

Moves selected objects down in the hierarchy.

#### Hierarchy Move UP

Moves selected objects up in the hierarchy.

#### Paste as Child

Pastes objects as children of the current selection.

#### Viewport Clean

Cleans up the viewport by toggling various display options.

## License

This project is licensed under the Creative Commons Legal Code CC0 1.0 Universal. See the [LICENSE](LICENSE) file for details.