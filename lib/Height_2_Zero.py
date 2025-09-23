from xml.dom import minidom


def modify_kml(input_file, output_file):
    # Parse the KML file
    kml_doc = minidom.parse(input_file)

    # Get all <coordinates> elements
    coordinates_elements = kml_doc.getElementsByTagName("coordinates")

    for elem in coordinates_elements:
        # Get the text content of the <coordinates> element
        coords_text = elem.firstChild.nodeValue.strip()

        # Split the coordinates into individual points
        points = coords_text.split()

        # Process each point
        modified_points = []
        for point in points:
            # Split the point into lon, lat, and (optionally) alt
            values = point.split(",")

            # Modify every third value (altitude, if present)
            if len(values) == 3:  # Only modify if altitude is present
                values[2] = "0"

            # Join the modified values and add them to the list
            modified_points.append(",".join(values))

        # Join the modified points and update the <coordinates> element
        elem.firstChild.nodeValue = " ".join(modified_points)

    # Write the modified KML to the output file
    with open(output_file, "w") as f:
        kml_doc.writexml(f, indent="  ", addindent="  ", newl="\n")


# Example usage
input_kml = "TMF_2_PORT_Final_WGS84.kml"  # Replace with your input KML file path
output_kml = "TMF_2_PORT_Final_WGS84_Zero_H.kml"  # Replace with your desired output KML file path
modify_kml(input_kml, output_kml)