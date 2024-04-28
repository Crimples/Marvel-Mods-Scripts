##Version 1.2

import subprocess
import os
import sys
import re
import binascii
import time
import struct
import shutil

###############
## Pre-Setup ##
###############
# Check Python versioning
if sys.version_info[0] < 3:
    raise Exception("Python 3 or a more recent version is required.")
try:

    print("Python version is 3 or higher. Continuing with the program...")
except Exception as e:
    print("Error:", e)

# Define a function to display the progress bar
def progress_bar(current, total, bar_length=50):
    percent = current / total
    arrow = '=' * int(round(percent * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    print('\rProgress: [{0}] {1}/{2}'.format(arrow + spaces, current, total), end='', flush=True)
total_tasks = 9
for i in range(1, total_tasks + 1):
    time.sleep(0.1)


######################################
## Step 1 - Gather Inputs/Variables ##
######################################

def get_valid_skin_slot(prompt):
    while True:
        slot = input(prompt)
        if slot.isdigit() and int(slot) not in [0, 1, 2]:
            return slot
        else:
            print("Invalid input. Skin slots '00', '01', and '02' are not allowed.")

# Prompt the user to input CharacterName
CharacterName = input("Enter Character Name: ")
# Prompt the user to input CurrentNumber
CurrentNumber = get_valid_skin_slot("Enter current skin slot (e.g., 03, 04, 05, ...): ")
# Convert CurrentNumber to an integer and add 1 to it
SecondCurrentNumber = int(CurrentNumber) + 1
# Add leading zero if the number is a single digit
CurrentNumber = str(CurrentNumber).zfill(2)
# Add leading zero if the number is a single digit
SecondCurrentNumber = str(SecondCurrentNumber).zfill(2)
# Prompt the user to input FirstNumber
FirstNumber = get_valid_skin_slot("Enter requested skin slot (e.g., 03, 04, 05, ...): ")
# Convert FirstNumber to an integer and add 1 to it
SecondNumber = int(FirstNumber) + 1
# Add leading zero if the number is a single digit
FirstNumber = str(FirstNumber).zfill(2)
# Add leading zero if the number is a single digit
SecondNumber = str(SecondNumber).zfill(2)
#Declared Variables for First/Current Numbers under 10p
FirstNumberClean = str(int(FirstNumber))
CurrentNumberClean = str(int(CurrentNumber))
#Declared Variables for Second/Current Numbers under 10p
SecondNumberClean = str(int(SecondNumber))
SecondCurrentNumberClean = str(int(SecondCurrentNumber))

# Define variables to check    
def prompt_and_check_numbers():
    while True:
        global CharacterName
        global CurrentNumber
        global SecondCurrentNumber
        global FirstNumber

# Update the progress bar
progress_bar(1, total_tasks)

#############################################
## Step 2 - Running .arc against .bat file ##
#############################################

# Construct the file path with delay for error possibility
file_path = os.path.join(os.getcwd(), f"{CharacterName}_{CurrentNumber}.arc")
time.sleep(1.5)

# Construct the batch file path
batch_file_path = os.path.join(os.getcwd(), "pc-dmc4se.bat")

# Check if the file exists
if os.path.exists(file_path):
    # Check if the batch file exists
    if os.path.exists(batch_file_path):
        # Run the batch file with the file path as an argument
        subprocess.run([batch_file_path, file_path], shell=True)
        print(f"Opened '{file_path}' with '{batch_file_path}'.")
    else:
        print(f"Batch file '{batch_file_path}' not found.")
        sys.exit()
else:
    print(f"File '{file_path}' not found.")
    sys.exit()

# Update the progress bar
progress_bar(2, total_tasks)

############################
## Step 3 - Rename Folder ##
############################

# Get the current directory
current_directory = os.getcwd()

# Iterate over all directories and subdirectories
for root, dirs, files in os.walk(current_directory):
    # Iterate over each file in the current directory
    for filename in files:
        # Get the full path of the file
        file_path = os.path.join(root, filename)
        # Check if the file is not an executable and if its name contains SecondCurrentNumber at the beginning
        if not filename.endswith(('.exe', '.lmt', '.5A7E5D8A')) and filename.startswith(SecondCurrentNumberClean):
            # Construct the new filename by replacing SecondCurrentNumber with SecondNumber
            new_filename = SecondNumberClean + filename[len(SecondCurrentNumberClean):]
            # Construct the new file path
            new_file_path = os.path.join(root, new_filename)
            # Rename the file
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_path} to {new_file_path}")

# Update the progress bar
progress_bar(3, total_tasks)

###########################
## Step 4 - Rename Files ##
###########################

# Get the current directory
current_directory = os.getcwd()

# Iterate over all directories and subdirectories
for root, dirs, files in os.walk(current_directory):
    # Iterate over each file in the current directory
    for filename in files:
        # Split the file name and extension
        file_name, file_extension = os.path.splitext(filename)
        print("File name:", file_name)
        # Print file name and relevant variables for debugging
        # Check if the file name contains the substring "eftpathlist" followed by SecondCurrentNumber
        # Check if the filename contains ".lmt" or ".5A7E5D8A"
        if ".lmt" in file_name or ".5A7E5D8A" in file_name:
            continue  # Ignore files with ".lmt" or ".5A7E5D8A" in the filename
        if "eftpathlist" + SecondCurrentNumber in file_name:
            # Construct the new file name by replacing SecondCurrentNumber with SecondNumber
            new_file_name = file_name.replace(SecondCurrentNumber, SecondNumber)
            # Construct the new file path
            new_file_path = os.path.join(root, new_file_name + file_extension)
            # Rename the file
            os.rename(os.path.join(root, filename), new_file_path)
            print(f"Renamed: {os.path.join(root, filename)} to {new_file_path}")
        # Check if the file name contains the substring for SecondCurrentNumberClean condition
        elif SecondCurrentNumberClean in file_name and file_name.endswith("p"):
            # Construct the new file name by replacing SecondCurrentNumberClean with SecondNumberClean
            new_file_name = file_name.replace(SecondCurrentNumberClean, SecondNumberClean)
            # Construct the new file path
            new_file_path = os.path.join(root, new_file_name + file_extension)
            # Rename the file
            os.rename(os.path.join(root, filename), new_file_path)
            print(f"Renamed: {os.path.join(root, filename)} to {new_file_path}")

# Iterate over all directories and subdirectories
for root, dirs, files in os.walk(current_directory):
    # Iterate over each directory in the current directory
    for dirname in dirs:
        # Check if the directory name contains SecondCurrentNumber
        if SecondCurrentNumberClean in dirname:
            # Construct the new directory name by replacing SecondCurrentNumber with SecondNumber
            new_dirname = dirname.replace(SecondCurrentNumberClean, SecondNumberClean)
            # Construct the new directory path
            new_dir_path = os.path.join(root, new_dirname)
            # Rename the directory
            os.rename(os.path.join(root, dirname), new_dir_path)
            print(f"Renamed: {os.path.join(root, dirname)} to {new_dir_path}")

# Update the progress bar
progress_bar(4, total_tasks)

##########################################
## Step 5 - Modify UI files speficially ##
##########################################

#Delay for issue
time.sleep (1.5) 

# Get the current directory
current_directory = os.getcwd()

# Initialize the UI path variable
UIPath = None

# Iterate over all directories and subdirectories
for root, dirs, files in os.walk(current_directory):
    # Check if 'ui' folder is found
    if 'ui' in dirs:
        UIPath = os.path.join(root, 'ui')
        break

if UIPath:
    # Iterate over files in the 'ui' folder and its subdirectories
    for root, dirs, files in os.walk(UIPath):
        for filename in files:
            # Check if the file name contains CurrentNumber
            if CurrentNumber in filename:
                # Construct the new filename by replacing CurrentNumber with FirstNumber
                new_filename = filename.replace(CurrentNumber, FirstNumber)
                # Construct the new file path
                old_file_path = os.path.join(root, filename)
                new_file_path = os.path.join(root, new_filename)
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed: {old_file_path} to {new_file_path}")
else:
    print("No 'ui' folder found in the current directory.")
    sys.exit()
    
# Update the progress bar
progress_bar(5, total_tasks)

#####################################################################
## Step 6 - Modify .txt to include changes to SecondCurrentNumber  ##
#####################################################################

#Define replacment variable and update

def update_file_content(file_path, old_value, new_value):
    # Read the contents of the text file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Replace occurrences of old_value in each line
    updated_lines = []
    for line in lines:
        if 'eftpathlist' in line:  # Check if 'eftpathlist' occurs in the line
            # Use regular expression to replace only the first occurrence of old_value before a period
            updated_line = re.sub(r'(?<!\d)' + re.escape(old_value) + r'(?=\.\w)', new_value, line, count=1)
            updated_lines.append(updated_line)
            # Other elif blocks and conditions...
        elif line.strip().startswith('ui'):  # Check if the line starts with 'UI'
            updated_line = line.replace(old_value, new_value, 1)  # Replace only the first occurrence
            updated_lines.append(updated_line)
        elif line.strip().endswith(('.ean', '.0026E7FF', '.3E363245', '.326F732E')) and '\\' + old_value not in line:
            # If the line ends with above extensions and does not contain a backslash before the variable, keep it unchanged
            updated_lines.append(line)
        elif re.search(r'\b(000[1-9])\b', line) and not re.search(r'\.(lmt|5A7E5D8A)', line):
            # If the line contains 0001-0009 and ends not with .lmt or .5A7E5D8A, keep it unchanged
            updated_lines.append(line)
        elif line.strip().endswith(('.lmt', '.5A7E5D8A')):
            updated_lines.append(line)
        elif line.strip().endswith('.tex'):
            # If the line ends with the specified extension, replace all instances of "old_value"p
            updated_line = re.sub(re.escape(old_value) + r'(?=p)', new_value, line)
            updated_lines.append(updated_line)
        else:
            # Find the index of the first occurrence of old_value
            index = line.find(old_value)
            if index != -1:  # If old_value is found in the line
                # Check if old_value is followed by "p" or another number
                if index + len(old_value) < len(line) and (line[index + len(old_value)].isdigit() or line[index + len(old_value)] == 'p'):
                    # Replace only the first occurrence of old_value with new_value
                    updated_line = line[:index] + new_value + line[index + len(old_value):]
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line)  # Append the original line if old_value is not followed by "p" or a number
            else:
                updated_lines.append(line)  # Append the original line if old_value is not found in the line

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

    print(f"File '{file_path}' has been modified.")

# Specify the file path
file_path = f"{CharacterName}_{CurrentNumber}.arc.txt"

# Update content related to SecondCurrentNumber
update_file_content(file_path, SecondCurrentNumber, SecondNumber)
update_file_content(file_path, SecondCurrentNumberClean, SecondNumberClean)
# Update content related to CurrentNumber
update_file_content(file_path, CurrentNumber, FirstNumber)
    
# Update the progress bar
progress_bar(6, total_tasks)

########################################################################################
## Step 7 - Modify files that contain mentions to efl's\mod's if specifically .arc 09 ##
########################################################################################

# Get the current directory
current_directory = os.getcwd()

# Define file extensions to search for
extensions = ['.357EF6D4', '.448BBDD4']
extensions2 = ['.mrl', '.efl']

if (SecondCurrentNumberClean) == str(10):

    # Iterate over all files in the current directory and its subdirectories
    for root, dirs, files in os.walk(current_directory):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")

                # Read the content of the file in binary mode
                with open(file_path, 'r+b') as file:
                    content = bytearray(file.read())

                    # Find all instances of SecondCurrentNumber followed by 3 numbers
                    index = content.find(bytes(SecondCurrentNumber, 'ascii'))
                    while index != -1:
                        # Check if the index is followed by 3 digits
                        if index + len(SecondCurrentNumber) + 3 <= len(content) and content[index + len(SecondCurrentNumber):index + len(SecondCurrentNumber) + 3].isdigit():
                            # Replace SecondCurrentNumber with SecondNumber
                            content[index:index + len(SecondNumber)] = bytes(SecondNumber, 'ascii')
                        # Find the next occurrence of SecondCurrentNumber
                        index = content.find(bytes(SecondCurrentNumber, 'ascii'), index + 1)

                    # Write the modified content back to the file
                    file.seek(0)
                    file.write(content)

                print(f"Modified: {file_path}")

            elif filename.endswith(tuple(extensions2)):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")
                # Read the content of the file in binary mode
                with open(file_path, 'rb') as file:
                    content = file.read()
    
                # Find all occurrences of the bytes b'\x63\x6D\x6E\x5C' in the content
                cmn_indices = [i for i, x in enumerate(content) if content[i:i+4] == b'\x63\x6D\x6E\x5C']
                # Find all occurrences of the bytes b'\x74\x65\x78\x5C' in the content
                tex_indices = [i for i, x in enumerate(content) if content[i:i+4] == b'\x74\x65\x78\x5C']
                # Identify all instances of SecondCurrentNumberClean followed by "p" or by 3 numbers
                second_current_indices_clean = [i for i in range(len(content) - len(SecondCurrentNumberClean)) if content[i:i+len(SecondCurrentNumberClean)] == bytes(SecondCurrentNumberClean, 'ascii') and (content[i+len(SecondCurrentNumberClean)] == ord('p') or all(chr(content[i+len(SecondCurrentNumberClean)+j]).isdigit() for j in range(3)))]
    
                # Replace SecondCurrentNumberClean with SecondNumber as needed
                index_offset = 0
                for index in second_current_indices_clean:
                    adjusted_index = index + index_offset
                    should_replace = True
                    for cmn_index in cmn_indices:
                        if abs(cmn_index - adjusted_index) < 20:
                            should_replace = False
                            break
                    # Check if the current index is within 20 bytes of b'\x74\x65\x78\x5C'
                    for tex_index in tex_indices:
                        if abs(tex_index - adjusted_index) < 20:
                            should_replace = False
                            break
                    if should_replace and (adjusted_index == 0 or not content[adjusted_index - 1:adjusted_index].isdigit()):
                        content = content[:adjusted_index] + bytes(SecondNumberClean, 'ascii') + content[adjusted_index+len(SecondCurrentNumberClean):]
                        # Adjust the index offset after replacement
                        index_offset += len(SecondNumberClean) - len(SecondCurrentNumberClean)
    
                # Write the modified content back to the file
                with open(file_path, 'wb') as file:
                    file.write(content)
                print(f"Modified: {file_path}")

################################################################################
## Step 7a - Modify files that contain mentions to efl's\mod's if same length ##
################################################################################

elif len(CurrentNumberClean) == len(FirstNumberClean):

    # Get the current directory
    current_directory = os.getcwd()
    
    # Define file extensions to search for
    extensions = ['.mrl', '.448BBDD4', '.efl']
    
    # Iterate over all files in the current directory and its subdirectories
    for root, dirs, files in os.walk(current_directory):
        for filename in files:
            # Check if the file has one of the specified extensions
            if filename.endswith(('.357EF6D4', '.448BBDD4')):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")
                # Read the content of the file in binary mode
                with open(file_path, 'rb') as file:
                    content = file.read()

                # Define the regular expression pattern to match SecondCurrentNumberClean not followed by a null byte
                pattern = re.compile(re.escape(bytes(SecondCurrentNumberClean, 'ascii')) + rb'(?!' + re.escape(b'\x00') + rb'|_StaJ)')

                # Replace SecondCurrentNumberClean with SecondNumberClean only if it doesn't occur before a null byte
                content = pattern.sub(bytes(SecondNumberClean, 'ascii'), content)

                # Write the modified content back to the file
                with open(file_path, 'wb') as file:
                    file.write(content)
                print(f"Modified: {file_path}")
            elif filename.endswith(tuple(extensions)):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")
                # Read the content of the file in binary mode
                with open(file_path, 'rb') as file:
                    content = file.read()
    
                # Find all occurrences of the bytes b'\x63\x6D\x6E\x5C' in the content
                cmn_indices = [i for i, x in enumerate(content) if content[i:i+4] == b'\x63\x6D\x6E\x5C']
                # Find all occurrences of the bytes b'\x74\x65\x78\x5C' in the content
                tex_indices = [i for i, x in enumerate(content) if content[i:i+4] == b'\x74\x65\x78\x5C']
                # Identify all instances of SecondCurrentNumberClean followed by "p" or by 3 numbers
                second_current_indices_clean = [i for i in range(len(content) - len(SecondCurrentNumberClean)) if content[i:i+len(SecondCurrentNumberClean)] == bytes(SecondCurrentNumberClean, 'ascii') and (content[i+len(SecondCurrentNumberClean)] == ord('p') or all(chr(content[i+len(SecondCurrentNumberClean)+j]).isdigit() for j in range(3)))]
    
                # Replace SecondCurrentNumberClean with SecondNumber as needed
                index_offset = 0
                for index in second_current_indices_clean:
                    adjusted_index = index + index_offset
                    should_replace = True
                    for cmn_index in cmn_indices:
                        if abs(cmn_index - adjusted_index) < 20:
                            should_replace = False
                            break
                    # Check if the current index is within 20 bytes of b'\x74\x65\x78\x5C'
                    for tex_index in tex_indices:
                        if abs(tex_index - adjusted_index) < 20:
                            should_replace = False
                            break
                    if should_replace and (adjusted_index == 0 or not content[adjusted_index - 1:adjusted_index].isdigit()):
                        content = content[:adjusted_index] + bytes(SecondNumberClean, 'ascii') + content[adjusted_index+len(SecondCurrentNumberClean):]
                        # Adjust the index offset after replacement
                        index_offset += len(SecondNumberClean) - len(SecondCurrentNumberClean)
    
                # Write the modified content back to the file
                with open(file_path, 'wb') as file:
                    file.write(content)
                print(f"Modified: {file_path}")

######################################################################################
## Step 7b - Modify files that contain mentions to efl's\mod's if different lengths ##
######################################################################################

elif len(CurrentNumberClean) != len(FirstNumberClean):

    # Get the current directory
    current_directory = os.getcwd()

    # Define file extensions to search for
    extensions = ['.mrl', '.448BBDD4', '.efl', '.357EF6D4', '.448BBDD4']

    # Iterate over all files in the current directory and its subdirectories
    for root, dirs, files in os.walk(current_directory):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")

                # Read the content of the file in binary mode
                with open(file_path, 'r+b') as file:
                    content = bytearray(file.read())

                    # Find all instances of SecondCurrentNumberClean
                    index = content.find(bytes(SecondCurrentNumberClean, 'ascii'))
                    while index != -1:
                        if index > 0 and content[index-1] == 92:  # Check if "\" occurs in ASCII before SecondCurrentNumberClean
                            # Calculate the length difference between SecondNumberClean and SecondCurrentNumberClean
                            length_difference = len(SecondNumberClean) - len(SecondCurrentNumberClean)
                            # Determine the position of the null byte at the end of the ASCII string
                            null_byte_index = content.find(b'\x00', index)
                            # Move the remaining ASCII string one byte to the right to accommodate the length difference
                            content[index+len(SecondNumberClean):null_byte_index+1] = content[index+len(SecondCurrentNumberClean):null_byte_index]
                            # Replace the ASCII string with SecondNumberClean
                            content[index:index+len(SecondNumberClean)] = bytes(SecondNumberClean, 'ascii')
                            # Move to the next occurrence of SecondCurrentNumberClean
                            index = content.find(bytes(SecondCurrentNumberClean, 'ascii'), index + len(SecondNumberClean) + length_difference)
                        else:
                            # Move to the next occurrence without replacing
                            index = content.find(bytes(SecondCurrentNumberClean, 'ascii'), index + 1)  

                    # Write the modified content back to the file
                    file.seek(0)
                    file.write(content)
                    file.truncate()

                print(f"Modified: {file_path}")

# Update the progress bar
progress_bar(7, total_tasks)

#######################################################
## Step 8 - Run .bat against folder to apply changes ##
#######################################################

# Construct the current and new folder paths
current_file = f"{CharacterName}_{CurrentNumber}.arc"
new_file = f"{CharacterName}_{FirstNumber}.arc"
folder_path = f"{CharacterName}_{CurrentNumber}"

# Check if the folder exists
if not os.path.exists(folder_path):
    print(f"Folder '{folder_path}' not found.")
    sys.exit()

# Execute the .bat file with the folder path as an argument
try:
    os.system(f'start pc-dmc4se.bat "{folder_path}"')
    print(f"Opened folder '{folder_path}' with 'pc-dmc4se.bat'")
except FileNotFoundError:
    print("Batch file 'pc-dmc4se.bat' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")


# Rename the file
print ("Waiting for script to finish running and cleanup")
time.sleep (3) 
try:
    os.rename(current_file, new_file)
    print(f"Renamed file: '{current_file}' to '{new_file}'")
except FileNotFoundError:
    print(f"File '{current_file}' not found.")
    exit()

# Update the progress bar
progress_bar(8, total_tasks)

#############################################
## Step 9 - Cleanup by removing old folder ## ##Commented out for extended testing
#############################################
    
# Construct the folder name
#folder_name = f"{CharacterName}_{CurrentNumber}"

# Specify the path to the directory to delete
#directory_to_delete = os.path.join(os.getcwd(), folder_name)

# Check if the directory exists
#if os.path.exists(directory_to_delete):
    # Try to remove the directory
    #try:
        #shutil.rmtree(directory_to_delete)
        #print(f"Successfully deleted the directory: {directory_to_delete}")
    #except OSError as e:
        #print(f"Error: {directory_to_delete} : {e.strerror}")
#else:
    #print(f"Directory does not exist: {directory_to_delete}")

# Update the progress bar
progress_bar(9, total_tasks)

print("\nScript completed!")
