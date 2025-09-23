from xml.dom import minidom
from tkinter import messagebox

def edit_kml(input_file):
    output_file = input_file[:-4] + "_DP_RM.kml"
    # Parse the KML file
    kml_doc = minidom.parse(input_file)

    # Get all <coordinates> elements
    coordinates_elements = kml_doc.getElementsByTagName("coordinates")

    for elem in coordinates_elements:
        # Get the text content of the <coordinates> element
        coords_text = elem.firstChild.nodeValue.strip()

        # Split the coordinates into individual points
        points = coords_text.split()

        # Use a set to track unique points
        unique_points = set()
        cleaned_points = []

        for point in points:
            # Check if the point is a duplicate
            if point in unique_points:
                # Log a message to the console about the duplicate
                print(f"Duplicate found and removed: {point}")
            else:
                # Add the point to the set and the cleaned list
                unique_points.add(point)
                cleaned_points.append(point)

        # Join the cleaned points and update the <coordinates> element
        elem.firstChild.nodeValue = " ".join(cleaned_points)

    # Write the modified KML to the output file
    with open(output_file, "w") as f:
        kml_doc.writexml(f, indent="  ", addindent="  ", newl="\n")
    messagebox.showinfo("Status", f"Updated KML saved to {output_file}")