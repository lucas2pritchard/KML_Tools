import xml.etree.ElementTree as ET

# Input and output file paths
input_kml_file = "Heading_Corrected_2_1_height.kml"
output_kml_file = "Heading_Corrected_2_1_height_reduced.kml"

def remove_points(input_file, output_file, num_to_remove):
    # Parse the KML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Define the KML namespace
    namespace = {"kml": "http://www.opengis.net/kml/2.2"}
    ET.register_namespace("", namespace["kml"])

    # Find all <coordinates> tags in the KML
    coordinates_elements = root.findall(".//kml:coordinates", namespace)

    for coordinates_element in coordinates_elements:
        # Get the text content of the <coordinates> tag
        coordinates_text = coordinates_element.text.strip()

        # Split the coordinates into a list of points
        coordinates = coordinates_text.split()

        # Remove specified number of points from each set of 10
        reduced_coordinates = []
        for i in range(0, len(coordinates), 10):
            # Get the current block of 10 points
            block = coordinates[i:i+10]
            # Remove the specified number of points
            reduced_block = [point for j, point in enumerate(block) if j >= num_to_remove]
            reduced_coordinates.extend(reduced_block)

        # Update the <coordinates> tag with the reduced list
        coordinates_element.text = "\n".join(reduced_coordinates)

    # Write the updated KML to the output file
    tree.write(output_file, encoding="utf-8", xml_declaration=True)
    print(f"Updated KML saved to {output_file}")

# Ask user for the number of points to remove
num_to_remove = int(input("Enter the number of points to remove from each set of 10: "))

# Run the function
remove_points(input_kml_file, output_kml_file, num_to_remove)