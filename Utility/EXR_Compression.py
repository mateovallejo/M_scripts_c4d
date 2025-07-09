import OpenImageIO as oiio

# Input and output file paths
input_file = "input.exr"
output_file = "output_compressed.exr"

# Open the input image
in_image = oiio.ImageInput.open(input_file)
if not in_image:
    raise RuntimeError(f"Could not open input file: {input_file}")

# Read image spec and pixels
spec = in_image.spec()
pixels = in_image.read_image()
in_image.close()

# Modify the spec to change compression
spec.attribute("compression", "dwaa")  # Changed to DWAA compression

# Create output image
out_image = oiio.ImageOutput.create(output_file)
if not out_image:
    raise RuntimeError(f"Could not create output file: {output_file}")

# Write the image with the new compression
success = out_image.open(output_file, spec)
if success:
    out_image.write_image(pixels)
    out_image.close()
    print(f"Written to {output_file} with DWAA compression.")
else:
    raise RuntimeError("Failed to write image.")
