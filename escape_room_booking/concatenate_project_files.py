import os

def concat_files(directory, output_file):
    with open(output_file, 'w') as outfile:
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                filepath = subdir + os.sep + file

                # Check for Python and HTML files
                if filepath.endswith(".py") or filepath.endswith(".html"):
                    with open(filepath, 'r') as infile:
                        outfile.write(f"---- {filepath} ----\n")
                        outfile.write(infile.read())
                        outfile.write("\n\n")

# Set the directory of your project here
project_directory = r'F:\COLLEGE\SEMESTER 5\PYTHON II\FINAL PROJECT\Python-EscapeRoomAppointmentSystem\escape_room_booking'

# The output file where all the contents will be concatenated
output_file = r'F:\COLLEGE\SEMESTER 5\PYTHON II\FINAL PROJECT\Python-EscapeRoomAppointmentSystem\project_files_concatenated.txt'

# Call the function
concat_files(project_directory, output_file)
