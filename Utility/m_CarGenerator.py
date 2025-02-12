import c4d
from c4d import utils
import random

# ------------------------------------------------
# Utility function to set an object’s custom color.
# ------------------------------------------------
def set_custom_color(obj, color):
    obj[c4d.ID_BASEOBJECT_COLOR] = color
    obj[c4d.ID_BASEOBJECT_USECOLOR] = 2

# ------------------------------------------------
# Trapezoidal Cabin Creation & Deformer Functions
# ------------------------------------------------
def create_trapezoid_cabin(bottom_width, bottom_depth, height, scale_top=0.8):
    """
    Create a trapezoidal cabin as a polygon object.
    The bottom face is defined by bottom_width x bottom_depth,
    while the top face is scaled by scale_top.
    The pivot is at the bottom center.
    """
    top_width = bottom_width * scale_top
    top_depth = bottom_depth * scale_top

    # Define eight vertices (with pivot at bottom center)
    vertices = [
        c4d.Vector(-bottom_width/2, 0, -bottom_depth/2),      # 0: bottom-back-left
        c4d.Vector( bottom_width/2, 0, -bottom_depth/2),       # 1: bottom-back-right
        c4d.Vector( top_width/2, height, -top_depth/2),         # 2: top-back-right
        c4d.Vector(-top_width/2, height, -top_depth/2),         # 3: top-back-left
        c4d.Vector(-bottom_width/2, 0, bottom_depth/2),         # 4: bottom-front-left
        c4d.Vector( bottom_width/2, 0, bottom_depth/2),          # 5: bottom-front-right
        c4d.Vector( top_width/2, height, top_depth/2),           # 6: top-front-right
        c4d.Vector(-top_width/2, height, top_depth/2)            # 7: top-front-left
    ]

    # Define six faces (polygons) for the box
    polygons = [
        c4d.CPolygon(3, 2, 1, 0),  # Back face
        c4d.CPolygon(4, 5, 6, 7),  # Front face
        c4d.CPolygon(0, 1, 5, 4),  # Bottom face
        c4d.CPolygon(2, 3, 7, 6),  # Top face (trapezoidal)
        c4d.CPolygon(1, 2, 6, 5),  # Right face
        c4d.CPolygon(4, 7, 3, 0)   # Left face
    ]

    polyObj = c4d.PolygonObject(len(vertices), len(polygons))
    polyObj.SetAllPoints(vertices)
    for i, poly in enumerate(polygons):
        polyObj.SetPolygon(i, poly)
    polyObj.Message(c4d.MSG_UPDATE)
    polyObj.SetName("Cabin")
    return polyObj

def add_edge_selection_tag(obj):
    """
    Add an edge selection tag to the object and select two edges:
    the top-back edge (between vertices 2 and 3) and the top-front edge (between vertices 6 and 7).
    """
    edgeSelTag = c4d.BaseTag(c4d.Tedgeselection)
    edgeSelTag.SetName("EdgeSelectionTag")
    baseSel = edgeSelTag.GetBaseSelect()
    if baseSel is None:
        raise RuntimeError("Could not retrieve BaseSelect from edge selection tag.")
    baseSel.DeselectAll()
    
    # Build a mapping of unique edges from all polygons.
    polyCount = obj.GetPolygonCount()
    edge_map = {}
    edge_list = []
    for i in range(polyCount):
        poly = obj.GetPolygon(i)
        pts = [poly.a, poly.b, poly.c, poly.d]
        for j in range(4):
            edge = tuple(sorted((pts[j], pts[(j+1) % 4])))
            if edge not in edge_map:
                edge_map[edge] = len(edge_list)
                edge_list.append(edge)
    
    # Select the edges (2,3) and (6,7)
    desired_edges = [tuple(sorted((6, 2))), tuple(sorted((3, 7)))]
    for edge in desired_edges:
        if edge in edge_map:
            baseSel.Select(edge_map[edge])
    
    obj.InsertTag(edgeSelTag)
    return edgeSelTag

def add_bevel_deformer_edges(obj):
    """
    Create a bevel deformer in edge mode with a set bevel radius
    and restrict it to the edges specified in the object's edge selection tag.
    """
    global doc
    # Make the object the active object.
    doc.SetActiveObject(obj, c4d.SELECTION_NEW)
    c4d.EventAdd()
    
    # Call the bevel deformer command (command ID 431000028).
    c4d.CallCommand(431000028)
    
    bevel = doc.GetActiveObject()
    if bevel is None or bevel == obj:
        raise RuntimeError("Bevel deformer was not created correctly.")
    
    # If not already a child, re-parent the bevel deformer under the cabin.
    if bevel.GetUp() != obj:
        bevel.Remove()
        bevel.InsertUnder(obj)
    
    # Retrieve (or add) the edge selection tag.
    edgeSelTag = obj.GetTag(c4d.Tedgeselection)
    if edgeSelTag is None:
        edgeSelTag = add_edge_selection_tag(obj)
    
    # Set the deformer to work in edge mode (typically 1 indicates edge mode).
    bevel[c4d.O_BEVEL_MODE_COMPONENT_TYPE] = 1
    # Set a bevel radius (adjust as desired).
    bevel[c4d.O_BEVEL_RADIUS] = 0
    # Restrict the deformer using the edge selection tag's name.
    bevel[c4d.O_BEVEL_RESTRICTION_START] = edgeSelTag.GetName()
    
    bevel.Message(c4d.MSG_UPDATE)
    c4d.EventAdd()
    return bevel

# ------------------------------------------------
# Main Car Generator
# ------------------------------------------------
def main():
    global doc
    doc = c4d.documents.GetActiveDocument()
    doc.StartUndo()  # Start the Undo block

    random.seed()

    # Define Colors
    body_color      = c4d.Vector(random.random(), random.random(), random.random())
    wheel_color     = c4d.Vector(0.2, 0.2, 0.2)
    headlight_color = c4d.Vector(1.0, 1.0, 0.5)
    taillight_color = c4d.Vector(1.0, 0.0, 0.0)
    detail_color    = c4d.Vector(0.2, 0.2, 0.2)

    # ------------------------------------------------
    # Create Nulls for grouping
    # ------------------------------------------------
    car = c4d.BaseObject(c4d.Onull)
    car.SetName("Car")
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, car)
    doc.InsertObject(car)

    wheelsNull = c4d.BaseObject(c4d.Onull)
    wheelsNull.SetName("Wheels")
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, wheelsNull)
    wheelsNull.InsertUnder(car)

    lightsNull = c4d.BaseObject(c4d.Onull)
    lightsNull.SetName("Lights")
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, lightsNull)
    lightsNull.InsertUnder(car)

    detailsNull = c4d.BaseObject(c4d.Onull)
    detailsNull.SetName("Details")
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, detailsNull)
    detailsNull.InsertUnder(car)

    # ------------------------------------------------
    # Chassis & Basic Dimensions
    # ------------------------------------------------
    chassis_length = random.uniform(150.0, 400.0)
    chassis_height = 30.0
    chassis_width  = random.uniform(80.0, 140.0)

    wheel_radius    = random.uniform(15.0, 35.0)
    wheel_thickness = random.uniform(15.0, 30.0)

    chassis_bottom   = wheel_radius
    chassis_center_y = chassis_bottom + chassis_height / 2.0

    chassis = c4d.BaseObject(c4d.Ocube)
    chassis.SetName("Chassis")
    chassis[c4d.PRIM_CUBE_LEN] = c4d.Vector(chassis_length, chassis_height, chassis_width)
    chassis.SetAbsPos(c4d.Vector(0, chassis_center_y, 0))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, chassis)
    chassis.InsertUnder(car)
    set_custom_color(chassis, body_color)

    # ------------------------------------------------
    # Generate Spoiler Length Early for Cabin sizing
    # ------------------------------------------------
    spoiler_length = random.uniform(30.0, 50.0)

    # ------------------------------------------------
    # Cabin (Trapezoidal version)
    # Instead of a cube, we create a trapezoidal cabin.
    # The cabin’s bottom dimensions are driven by available chassis space.
    # ------------------------------------------------
    cabin_min_length = 60.0
    cabin_max_length_candidate = chassis_length - spoiler_length - 20.0  # available space on chassis minus margin
    cabin_max_length = min(180.0, cabin_max_length_candidate)
    if cabin_max_length < cabin_min_length:
        cabin_max_length = cabin_min_length

    cabin_length = random.uniform(cabin_min_length, cabin_max_length)  # used as the cabin’s bottom width
    cabin_height = random.uniform(18.0, 28.0)
    max_cabin_width = min(120.0, chassis_width)
    cabin_width  = random.uniform(60.0, max_cabin_width)  # used as the cabin’s bottom depth

    # Compute position (pivot is at the bottom center)
    cabin_x = -20.0
    # Place the cabin just above the chassis
    cabin_y = chassis_bottom + chassis_height  
    cabin_z = 0.0

    # Create the trapezoidal cabin using the custom function.
    cabin = create_trapezoid_cabin(cabin_length, cabin_width, cabin_height, scale_top=0.8)
    cabin.SetAbsPos(c4d.Vector(cabin_x, cabin_y, cabin_z))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, cabin)
    cabin.InsertUnder(car)
    set_custom_color(cabin, body_color)

    # Add edge selection tag and bevel deformer to the cabin.
    add_edge_selection_tag(cabin)
    add_bevel_deformer_edges(cabin)

    # ------------------------------------------------
    # Wheels (with fillet), factoring in wheel_thickness for offset
    # ------------------------------------------------
    margin_z = 2.0
    half_chassis = chassis_width / 2.0
    half_thickness = wheel_thickness / 2.0

    wheel_offset_x = chassis_length / 2.0 - 20.0
    wheel_offset_z = half_chassis + half_thickness + margin_z

    wheel_positions = [
        c4d.Vector( wheel_offset_x, wheel_radius,  wheel_offset_z),   # Front Left
        c4d.Vector( wheel_offset_x, wheel_radius, -wheel_offset_z),   # Front Right
        c4d.Vector(-wheel_offset_x, wheel_radius,  wheel_offset_z),   # Rear Left
        c4d.Vector(-wheel_offset_x, wheel_radius, -wheel_offset_z)    # Rear Right
    ]

    fillet_radius = 5.0

    for i, pos in enumerate(wheel_positions):
        wheel = c4d.BaseObject(c4d.Ocylinder)
        wheel.SetName(f"Wheel_{i+1}")
        wheel[c4d.PRIM_CYLINDER_RADIUS] = wheel_radius
        wheel[c4d.PRIM_CYLINDER_HEIGHT] = wheel_thickness
        wheel[c4d.PRIM_CYLINDER_SEG] = 32

        if hasattr(c4d, 'PRIM_CYLINDER_AXIS'):
            wheel[c4d.PRIM_CYLINDER_AXIS] = 2
        else:
            wheel.SetAbsRot(c4d.Vector(0, utils.DegToRad(90), 0))

        wheel[c4d.PRIM_CYLINDER_FILLET] = True
        wheel[c4d.PRIM_CYLINDER_FILLETRADIUS] = fillet_radius

        wheel.SetAbsPos(pos)
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, wheel)
        wheel.InsertUnder(wheelsNull)
        set_custom_color(wheel, wheel_color)

    # ------------------------------------------------
    # Front Lights
    # ------------------------------------------------
    shapes = ["sphere", "cube"]
    chosen_shape = random.choice(shapes)
    
    # Define size ranges (in cm) for the lights.
    light_min_size = 8.0
    light_max_size = 10.0
    random_size = random.uniform(light_min_size, light_max_size)
    
    # For cube lights, add randomness to the Z (depth) size.
    z_min_size = 6.0
    z_max_size = 12.0
    if chosen_shape == "cube":
        random_z_size = random.uniform(z_min_size, z_max_size)
    
    front_light_offset_x = 2.0
    # Align front lights 1/3 of the chassis height from the top.
    # The chassis top is at: chassis_bottom + chassis_height.
    front_light_y = chassis_bottom + chassis_height - (chassis_height / 3.0)
    
    num_sets = random.randint(1, 2)
    if num_sets == 1:
        # Single set: two lights symmetrically placed.
        z_positions = [-(chassis_width / 3.0), (chassis_width / 3.0)]
    else:
        # Double sets: two lights per side.
        # Ensure the lights don't touch by leaving a 1.5 cm gap between them.
        desired_gap = 1.5  # gap in cm
        offset = (random_size + desired_gap) / 2.0
        
        left_center = -chassis_width / 4.0
        right_center = chassis_width / 4.0
        left_positions = [left_center - offset, left_center + offset]
        right_positions = [right_center - offset, right_center + offset]
        z_positions = left_positions + right_positions
    
    idx = 0
    for z_pos in z_positions:
        idx += 1
        if chosen_shape == "sphere":
            light = c4d.BaseObject(c4d.Osphere)
            light.SetName(f"FrontLight_{idx}")
            light[c4d.PRIM_SPHERE_RAD] = random_size / 2.0
        else:
            light = c4d.BaseObject(c4d.Ocube)
            light.SetName(f"FrontLight_{idx}")
            light[c4d.PRIM_CUBE_LEN] = c4d.Vector(random_size, random_size, random_z_size)
    
        px = chassis_length / 2.0 + front_light_offset_x
        py = front_light_y
        pz = z_pos
        light.SetAbsPos(c4d.Vector(px, py, pz))
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, light)
        light.InsertUnder(lightsNull)
        set_custom_color(light, headlight_color)

    # ------------------------------------------------
    # Tail Lights
    # ------------------------------------------------
    tail_light_radius  = 5.0
    tail_light_offset_x= 2.0
    tail_light_y       = chassis_center_y
    tail_light_z       = chassis_width / 4.0

    tail_light_left = c4d.BaseObject(c4d.Osphere)
    tail_light_left.SetName("TailLight_Left")
    tail_light_left[c4d.PRIM_SPHERE_RAD] = tail_light_radius
    tail_light_left.SetAbsPos(c4d.Vector(-chassis_length/2.0 - tail_light_offset_x, tail_light_y,  tail_light_z))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, tail_light_left)
    tail_light_left.InsertUnder(lightsNull)
    set_custom_color(tail_light_left, taillight_color)

    tail_light_right = c4d.BaseObject(c4d.Osphere)
    tail_light_right.SetName("TailLight_Right")
    tail_light_right[c4d.PRIM_SPHERE_RAD] = tail_light_radius
    tail_light_right.SetAbsPos(c4d.Vector(-chassis_length/2.0 - tail_light_offset_x, tail_light_y, -tail_light_z))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, tail_light_right)
    tail_light_right.InsertUnder(lightsNull)
    set_custom_color(tail_light_right, taillight_color)

    # ------------------------------------------------
    # Spoiler
    # ------------------------------------------------
    spoiler_height = random.uniform(5.0, 10.0)
    spoiler_width  = random.uniform(50.0, chassis_width)

    spoiler_x = -chassis_length / 2.0 + spoiler_length / 2.0
    spoiler_y = chassis_bottom + chassis_height + spoiler_height / 2.0
    spoiler_z = 0.0

    spoiler = c4d.BaseObject(c4d.Ocube)
    spoiler.SetName("Spoiler")
    spoiler[c4d.PRIM_CUBE_LEN] = c4d.Vector(spoiler_length, spoiler_height, spoiler_width)
    spoiler.SetAbsPos(c4d.Vector(spoiler_x, spoiler_y, spoiler_z))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, spoiler)
    spoiler.InsertUnder(detailsNull)
    set_custom_color(spoiler, detail_color)

    # ------------------------------------------------
    # Bumper 
    # ------------------------------------------------
    bumper_length = 10.0
    bumper_height = 10.0
    # Match the bumper's width to the chassis width
    bumper_width  = chassis_width

    # Position the bumper at the front of the chassis
    bumper_x = chassis_length / 2.0 + bumper_length / 2.0
    # Align the bumper's bottom with the chassis bottom.
    # Since the bumper's pivot is at its center, add half its height.
    bumper_y = chassis_bottom + bumper_height / 2.0
    bumper_z = 0.0

    bumper = c4d.BaseObject(c4d.Ocube)
    bumper.SetName("Bumper")
    bumper[c4d.PRIM_CUBE_LEN] = c4d.Vector(bumper_length, bumper_height, bumper_width)
    bumper.SetAbsPos(c4d.Vector(bumper_x, bumper_y, bumper_z))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, bumper)
    bumper.InsertUnder(detailsNull)
    set_custom_color(bumper, detail_color)

    # ------------------------------------------------
    # Randomized Exhaust (single/double, left/right/both)
    # ------------------------------------------------
    exhaust_mode = random.randint(1, 4)
    exhaust_radius = 4.0
    exhaust_height = random.uniform(12.0, 20.0)
    margin_exhaust_x = 10.0
    exhaust_x = -chassis_length / 2.0 + margin_exhaust_x - (exhaust_height / 2.0)
    exhaust_y = chassis_bottom - exhaust_radius
    margin_exhaust_z = 20.0
    leftZ = (chassis_width / 2.0) - margin_exhaust_z
    rightZ = -(chassis_width / 2.0) + margin_exhaust_z
    double_gap_z = exhaust_radius * 2.0

    def create_exhaust(pos_x, pos_y, pos_z, name):
        e = c4d.BaseObject(c4d.Ocylinder)
        e.SetName(name)
        e[c4d.PRIM_CYLINDER_RADIUS] = exhaust_radius
        e[c4d.PRIM_CYLINDER_HEIGHT] = exhaust_height
        if hasattr(c4d, 'PRIM_CYLINDER_AXIS'):
            e[c4d.PRIM_CYLINDER_AXIS] = 1  # X axis
        else:
            e.SetAbsRot(c4d.Vector(0, 0, utils.DegToRad(90)))
        e.SetAbsPos(c4d.Vector(pos_x, pos_y, pos_z))
        doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, e)
        e.InsertUnder(detailsNull)
        set_custom_color(e, detail_color)
        return e

    if exhaust_mode == 1:
        create_exhaust(exhaust_x, exhaust_y, leftZ, "Exhaust_Left")
    elif exhaust_mode == 2:
        create_exhaust(exhaust_x, exhaust_y, leftZ,  "Exhaust_Left")
        create_exhaust(exhaust_x, exhaust_y, rightZ, "Exhaust_Right")
    elif exhaust_mode == 3:
        create_exhaust(exhaust_x, exhaust_y, leftZ - double_gap_z/2.0, "Exhaust_LeftA")
        create_exhaust(exhaust_x, exhaust_y, leftZ + double_gap_z/2.0, "Exhaust_LeftB")
    else:
        create_exhaust(exhaust_x, exhaust_y, leftZ - double_gap_z/2.0,  "Exhaust_LeftA")
        create_exhaust(exhaust_x, exhaust_y, leftZ + double_gap_z/2.0,  "Exhaust_LeftB")
        create_exhaust(exhaust_x, exhaust_y, rightZ - double_gap_z/2.0, "Exhaust_RightA")
        create_exhaust(exhaust_x, exhaust_y, rightZ + double_gap_z/2.0, "Exhaust_RightB")

    # ------------------------------------------------
    # Side Mirrors (Left & Right, near front corners)
    # ------------------------------------------------
    mirror_width = 8.0
    mirror_height = 8.0
    mirror_depth = 3.0

    cabin_front_x = cabin_x + (cabin_length * 0.5)
    mirror_base_y = cabin_y + (cabin_height / 4.0)
    mirror_offset_front = -5.0
    mirror_offset_z = (cabin_width / 2.0) + 5.0

    mirror_left = c4d.BaseObject(c4d.Ocube)
    mirror_left.SetName("Mirror_Left")
    mirror_left[c4d.PRIM_CUBE_LEN] = c4d.Vector(mirror_width, mirror_height, mirror_depth)
    mlx = cabin_front_x + mirror_offset_front
    mly = mirror_base_y
    mlz = cabin_z + mirror_offset_z
    mirror_left.SetAbsPos(c4d.Vector(mlx, mly, mlz))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, mirror_left)
    mirror_left.InsertUnder(detailsNull)
    set_custom_color(mirror_left, detail_color)

    mirror_right = c4d.BaseObject(c4d.Ocube)
    mirror_right.SetName("Mirror_Right")
    mirror_right[c4d.PRIM_CUBE_LEN] = c4d.Vector(mirror_width, mirror_height, mirror_depth)
    mrx = cabin_front_x + mirror_offset_front
    mry = mirror_base_y
    mrz = cabin_z - mirror_offset_z
    mirror_right.SetAbsPos(c4d.Vector(mrx, mry, mrz))
    doc.AddUndo(c4d.UNDOTYPE_NEWOBJ, mirror_right)
    mirror_right.InsertUnder(detailsNull)
    set_custom_color(mirror_right, detail_color)

    # End the Undo Block and update Cinema 4D.
    doc.EndUndo()
    # Select the top most parent null ("Car")
    doc.SetActiveObject(car, c4d.SELECTION_NEW)
    c4d.EventAdd()

if __name__=='__main__':
    main()
