import xml.etree.ElementTree as ET

# Input KML file path
input_kml_file = "Heading_Corrected_2_1_height_reduced.kml"

def count_data_points_in_kml(input_file):
    # Parse the KML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Define the KML namespace
    namespace = {"kml": "http://www.opengis.net/kml/2.2"}
    ET.register_namespace("", namespace["kml"])

    # Find all <coordinates> tags in the KML
    coordinates_elements = root.findall(".//kml:coordinates", namespace)

    # Initialize a counter for the data points
    total_points = 0

    for coordinates_element in coordinates_elements:
        # Get the text content of the <coordinates> tag
        coordinates_text = coordinates_element.text.strip()

        # Split the coordinates into a list of points
        coordinates = coordinates_text.split()

        # Add the number of points in this <coordinates> tag to the total
        total_points += len(coordinates)

    print(f"Total number of data points in the KML file: {total_points}")
    return total_points

# Run the function
count_data_points_in_kml(input_kml_file)