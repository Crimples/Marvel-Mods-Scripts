##Version 2.0

import subprocess,os,sys,re,time,shutil

###############
## Pre-Setup ##
###############

# Define the log file name
log_file = "SkinSwap_Run.txt"

# Delete the log file if it exists
if os.path.exists(log_file):
    os.remove(log_file)

# Function to log messages to both console and a file
def log_message(message, log_file="SkinSwap_Run.txt"):
    try:
        # Open the log file in append mode (it will be created if it doesn't exist)
        with open(log_file, "a") as log:
            log.write(message + "\n")
        print(message)  # Also output the message to the console
    except Exception as e:
        print(f"Failed to write to log file. Error: {str(e)}")


#Function for Check Python Version
def check_python_version():
    if sys.version_info[0] < 3:
        raise Exception("Python 3 or a more recent version is required.")
    print("Python version is 3 or higher. Continuing with the program...")

#Function for setting up progress bar
def progress_bar(current, total, bar_length=50):
    percent = current / total
    arrow = '=' * int(round(percent * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    print(f'\rProgress: [{arrow + spaces}] {current}/{total}', end='', flush=True)

total_tasks = 9

#Run Python Function
check_python_version()

######################################
## Step 1 - Gather Inputs/Variables ##
######################################
#Define function to gather inputs
def gather_inputs():
    def get_valid_skin_slot(prompt, forbidden_slots={0, 1, 2}):
        while True:
            slot = input(prompt).zfill(2)
            if slot.isdigit() and int(slot) not in forbidden_slots:
                return slot
            print("Invalid input. Skin slots '00', '01', and '02' are not allowed.")

    CharacterName = input("Enter Character Name: ")
    CurrentSlotNumber = get_valid_skin_slot("Enter current skin slot (e.g., 03, 04, 05, ...): ")
    RequestedSlotNumber = get_valid_skin_slot("Enter requested skin slot (e.g., 03, 04, 05, ...): ")
    
    CurrentSlotNumber_PlusOne = str(int(CurrentSlotNumber) + 1).zfill(2)
    RequestedSlotNumber_PlusOne = str(int(RequestedSlotNumber) + 1).zfill(2)
    
    return CharacterName, CurrentSlotNumber, CurrentSlotNumber_PlusOne, RequestedSlotNumber, RequestedSlotNumber_PlusOne

CharacterName, CurrentSlotNumber, CurrentSlotNumber_PlusOne, RequestedSlotNumber, RequestedSlotNumber_PlusOne = gather_inputs()

#Gather sanitized inputs for specific use later
RequestedSlotNumberClean = str(int(RequestedSlotNumber))
CurrentSlotNumberClean = str(int(CurrentSlotNumber))
RequestedSlotNumber_PlusOneClean = str(int(RequestedSlotNumber_PlusOne))
CurrentSlotNumber_PlusOneClean = str(int(CurrentSlotNumber_PlusOne))
#Define current working directory
current_directory = os.getcwd()

# Update the progress bar
progress_bar(1, total_tasks)

#############################################
## Step 2 - Running .arc against .bat file ##
#############################################

# Construct the file path with delay for error possibility
file_path = os.path.join(current_directory, f"{CharacterName}_{CurrentSlotNumber}.arc")
time.sleep(1.5)
# Construct the batch file path
batch_file_path = os.path.join(current_directory, "pc-dmc4se.bat")

# Define function to attempt to find the file_path with retries
def run_batch_file(batch_file_path, file_path, retries=3, delay=2):
    for attempt in range(retries):
        if os.path.exists(file_path):
            if os.path.exists(batch_file_path):
                subprocess.run([batch_file_path, file_path], check=True)
                print(f"Opened '{file_path}' with '{batch_file_path}'.")
                return
            else:
                raise FileNotFoundError(f"Batch file '{batch_file_path}' not found.")
        elif attempt < retries - 1:
            print(f"File '{file_path}' not found. Retrying in {delay} second(s)...")
            time.sleep(delay)
        else:
            raise FileNotFoundError(f"File '{file_path}' not found after {retries} attempts.")

#Run function
run_batch_file(batch_file_path, file_path)

# Update the progress bar
progress_bar(2, total_tasks)

############################
## Step 3 - Rename Folder ##
############################
#Define function to rename folders
def rename_folders(current_directory, CurrentSlotNumber_PlusOneClean, RequestedSlotNumber_PlusOneClean, log_file="SkinSwap_Run.txt"):
    try:
        for root, dirs, files in os.walk(current_directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if not filename.endswith('.exe') and filename.startswith(CurrentSlotNumber_PlusOneClean):
                    new_filename = RequestedSlotNumber_PlusOneClean + filename[len(CurrentSlotNumber_PlusOneClean):]
                    new_file_path = os.path.join(root, new_filename)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {file_path} to {new_file_path}")
    except Exception as e:
        error_message = f"Error in folder renaming process. Error: {str(e)}"
        log_message(error_message, log_file)
#Run function to rename folders
rename_folders(current_directory, CurrentSlotNumber_PlusOneClean, RequestedSlotNumber_PlusOneClean)

# Update the progress bar
progress_bar(3, total_tasks)

###########################
## Step 4 - Rename Files ##
###########################

# Iterate over all directories and subdirectories
try:
    for root, dirs, files in os.walk(current_directory):
        # Iterate over each file in the current directory
        for filename in files:
            # Split the file name and extension
            file_name, file_extension = os.path.splitext(filename)
            print("File name:", file_name)
            # Print file name and relevant variables for debugging
            # Check if the file name is cmn.cst and RequestedSlotNumberClean is "7"
            if file_name == "cmn" and RequestedSlotNumberClean == "7":
                # Construct the new file path
                new_file_path = os.path.join(root, "sp.326F732E")
                # Rename the file
                os.rename(os.path.join(root, filename), new_file_path)
                print(f"Renamed: {os.path.join(root, filename)} to {new_file_path}")
                continue  # Skip further processing for this file
            # Check if the file name contains the substring "eftpathlist" followed by CurrentSlotNumber_PlusOne
            if "eftpathlist" + CurrentSlotNumber_PlusOne in file_name:
                # Construct the new file name by replacing CurrentSlotNumber_PlusOne with RequestedSlotNumber_PlusOne
                new_file_name = file_name.replace(CurrentSlotNumber_PlusOne, RequestedSlotNumber_PlusOne)
                # Construct the new file path
                new_file_path = os.path.join(root, new_file_name + file_extension)
                # Rename the file
                os.rename(os.path.join(root, filename), new_file_path)
                print(f"Renamed: {os.path.join(root, filename)} to {new_file_path}")
            # Check if the file name contains the substring for CurrentSlotNumber_PlusOneClean condition
            elif CurrentSlotNumber_PlusOneClean in file_name and file_name.endswith("p"):
                # Construct the new file name by replacing CurrentSlotNumber_PlusOneClean with RequestedSlotNumber_PlusOneClean
                new_file_name = file_name.replace(CurrentSlotNumber_PlusOneClean, RequestedSlotNumber_PlusOneClean)
                # Construct the new file path
                new_file_path = os.path.join(root, new_file_name + file_extension)
                # Rename the file
                os.rename(os.path.join(root, filename), new_file_path)
                print(f"Renamed: {os.path.join(root, filename)} to {new_file_path}")
except FileNotFoundError as e:
    log_message(f"File not found: {e}", log_file="SkinSwap_Run.txt")
except OSError as e:
    log_message(f"OS error during renaming: {e}", log_file="SkinSwap_Run.txt")
except Exception as e:
    log_message(f"Unexpected error during file renaming: {e}", log_file="SkinSwap_Run.txt")

# Iterate over all directories and subdirectories
for root, dirs, files in os.walk(current_directory):
    # Check if the current directory is the top-level directory
    if root == current_directory:
        # Remove the current directory from the list of directories to avoid modifying it
        dirs[:] = [d for d in dirs if d != os.path.basename(root)]
        continue  # Skip further processing for the top-level directory
    
    # Iterate over each directory in the current directory
    for dirname in dirs:
        # Check if the directory name contains CurrentSlotNumber_PlusOneClean
        if CurrentSlotNumber_PlusOneClean in dirname:
            # Construct the new directory name by replacing CurrentSlotNumber_PlusOneClean with RequestedSlotNumber_PlusOneClean
            new_dirname = dirname.replace(CurrentSlotNumber_PlusOneClean, RequestedSlotNumber_PlusOneClean)
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

#Function for modyfing UI files
def modify_ui_files(current_directory, CurrentSlotNumber, RequestedSlotNumber, log_file="SkinSwap_Run.txt"):
    try:
        time.sleep(1.5)
        UIPath = None

        for root, dirs, files in os.walk(current_directory):
            if 'ui' in dirs:
                UIPath = os.path.join(root, 'ui')
                break

        if UIPath:
            for root, dirs, files in os.walk(UIPath):
                for filename in files:
                    if CurrentSlotNumber in filename:
                        if "Thing1" + CurrentSlotNumber in filename:
                            new_filename = filename.replace("Thing1" + CurrentSlotNumber, "Thing1" + RequestedSlotNumber)
                        else:
                            new_filename = filename.replace(CurrentSlotNumber, RequestedSlotNumber)
                        old_file_path = os.path.join(root, filename)
                        new_file_path = os.path.join(root, new_filename)
                        os.rename(old_file_path, new_file_path)
                        print(f"Renamed: {old_file_path} to {new_file_path}")
        else:
            raise FileNotFoundError("No 'ui' folder found in the current directory.")
    except Exception as e:
        error_message = f"Error in UI file modification process. Error: {str(e)}"
        log_message(error_message, log_file)

#Running function for modifying UI files
modify_ui_files(current_directory, CurrentSlotNumber, RequestedSlotNumber)
    
# Update the progress bar
progress_bar(5, total_tasks)

#####################################################################
## Step 6 - Modify .txt to include changes to CurrentSlotNumber_PlusOne  ##
#####################################################################

#Define replacment variable and update

def update_file_content(file_path, old_value, new_value, log_file="SkinSwap_Run.txt"):
    # Read the contents of the text file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Replace occurrences of old_value in each line
    updated_lines = []
    try:
        for line in lines:
            if 'eftpathlist' in line:  # Check if 'eftpathlist' occurs in the line
                # Use regular expression to replace only the first occurrence of old_value before a period
                updated_line = re.sub(r'(?<!\d)' + re.escape(old_value) + r'(?=\.\w)', new_value, line, count=1)
                updated_lines.append(updated_line)
                # Other elif blocks and conditions...
            elif line.strip().startswith('ui'):  # Check if the line starts with 'UI'
                updated_line = line.replace(old_value, new_value, 1)  # Replace only the first occurrence
                updated_lines.append(updated_line)
            elif line.strip().endswith(('.ean', '.0026E7FF', '.3E363245', '.326F732E','.lmt', '.5A7E5D8A')) and '\\' + old_value not in line:
                # If the line ends with above extensions and does not contain a backslash before the variable, keep it unchanged
                updated_lines.append(line)
            elif re.search(r'\b(000[1-9])\b', line) and not re.search(r'\.(lmt|5A7E5D8A)', line):
                # If the line contains 0001-0009 and ends not with .lmt or .5A7E5D8A, keep it unchanged
                updated_lines.append(line)
            elif "weapon" in line:
            # If the word "weapon" occurs in the line, replace the first instance of old_value with new_value
                updated_lines.append(line.replace(old_value, new_value, 1))    
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
    except Exception as e:
        log_message(f"Error processing lines in '{file_path}': {e}", log_file)
        return
    
    try:    
        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(updated_lines)
    except IOError as e:
        log_message("Error processing lines in '{file_path}': {e}", log_file)
        return
    print(f"File '{file_path}' has been modified.")

# File path setup and updating content
file_path = f"{CharacterName}_{CurrentSlotNumber}.arc.txt"
update_file_content(file_path, CurrentSlotNumber_PlusOne, RequestedSlotNumber_PlusOne)
update_file_content(file_path, CurrentSlotNumber_PlusOneClean, RequestedSlotNumber_PlusOneClean)
# Update content related to CurrentSlotNumber (MUST BE DONE SECOND)
update_file_content(file_path, CurrentSlotNumber, RequestedSlotNumber)

# Additional modification based on RequestedSlotNumberClean
if RequestedSlotNumberClean == "7":
    with open(file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        if "cmn.326F732E" in line:
            updated_line = line.replace("cmn.326F732E", "sp.326F732E")
            updated_lines.append(updated_line)
        else:
            updated_lines.append(line)

    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

    print(f"Specific modification for RequestedSlotNumberClean='7' applied to '{file_path}'.")

# Update the progress bar
progress_bar(6, total_tasks)

########################################################################################
## Step 7 - Modify files that contain mentions to efl's/mod's based on conditions ##
########################################################################################

# Define file extensions to search for
FileExtensions = ['.357EF6D4', '.448BBDD4']
EffectExtensions = ['.mrl', '.efl']

try:
    if (CurrentSlotNumber_PlusOneClean) == str(10): 

        # Iterate over all files in the current directory and its subdirectories
        for root, dirs, files in os.walk(current_directory):
            for filename in files:
                if filename.endswith(tuple(FileExtensions)):
                    file_path = os.path.join(root, filename)
                    print(f"Processing file: {file_path}")

                    # Read the content of the file in binary mode
                    with open(file_path, 'r+b') as file:
                        content = bytearray(file.read())

                        # Find all instances of CurrentSlotNumber_PlusOne followed by 3 numbers
                        index = content.find(bytes(CurrentSlotNumber_PlusOne, 'ascii'))
                        while index != -1:
                            # Check if the index is followed by 3 digits
                            if index + len(CurrentSlotNumber_PlusOne) + 3 <= len(content) and content[index + len(CurrentSlotNumber_PlusOne):index + len(CurrentSlotNumber_PlusOne) + 3].isdigit():
                                # Replace CurrentSlotNumber_PlusOne with RequestedSlotNumber_PlusOne
                                content[index:index + len(RequestedSlotNumber_PlusOne)] = bytes(RequestedSlotNumber_PlusOne, 'ascii')
                            # Find the next occurrence of CurrentSlotNumber_PlusOne
                            index = content.find(bytes(CurrentSlotNumber_PlusOne, 'ascii'), index + 1)

                        # Write the modified content back to the file
                        file.seek(0)
                        file.write(content)

                    print(f"Modified: {file_path}")

                elif filename.endswith(tuple(EffectExtensions)):
                    file_path = os.path.join(root, filename)
                    print(f"Processing file: {file_path}")
                    # Read the content of the file in binary mode
                    with open(file_path, 'rb') as file:
                        content = file.read()
        
                    # Find all occurrences of the bytes b'\x63\x6D\x6E\x5C' in the content
                    cmn_indices = [i for i, x in enumerate(content) if content[i:i+4] == b'\x63\x6D\x6E\x5C']
                    # Find all occurrences of the bytes b'\x74\x65\x78\x5C' in the content
                    tex_indices = [i for i, x in enumerate(content) if content[i:i+4] == b'\x74\x65\x78\x5C']
                    # Identify all instances of CurrentSlotNumber_PlusOneClean followed by "p" or by 3 numbers
                    second_current_indices_clean = [i for i in range(len(content) - len(CurrentSlotNumber_PlusOneClean)) if content[i:i+len(CurrentSlotNumber_PlusOneClean)] == bytes(CurrentSlotNumber_PlusOneClean, 'ascii') and (content[i+len(CurrentSlotNumber_PlusOneClean)] == ord('p') or all(chr(content[i+len(CurrentSlotNumber_PlusOneClean)+j]).isdigit() for j in range(3)))]
        
                    # Replace CurrentSlotNumber_PlusOneClean with RequestedSlotNumber_PlusOne as needed
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
                            content = content[:adjusted_index] + bytes(RequestedSlotNumber_PlusOneClean, 'ascii') + content[adjusted_index+len(CurrentSlotNumber_PlusOneClean):]
                            # Adjust the index offset after replacement
                            index_offset += len(RequestedSlotNumber_PlusOneClean) - len(CurrentSlotNumber_PlusOneClean)
        
                    # Write the modified content back to the file
                    with open(file_path, 'wb') as file:
                        file.write(content)
                    print(f"Modified: {file_path}")

    ################################################################################
    ## Step 7a - Modify files that contain mentions to efl's\mod's if same length ##
    ################################################################################

    elif len(CurrentSlotNumberClean) == len(RequestedSlotNumberClean) and (RequestedSlotNumber_PlusOneClean) != str(10):
        
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

                    # Define the regular expression pattern to match CurrentSlotNumber_PlusOneClean not followed by a null byte
                    pattern = re.compile(re.escape(bytes(CurrentSlotNumber_PlusOneClean, 'ascii')) + rb'(?!' + re.escape(b'\x00') + rb'|_StaJ)')

                    # Replace CurrentSlotNumber_PlusOneClean with RequestedSlotNumber_PlusOneClean only if it doesn't occur before a null byte
                    content = pattern.sub(bytes(RequestedSlotNumber_PlusOneClean, 'ascii'), content)

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
                    # Identify all instances of CurrentSlotNumber_PlusOneClean followed by "p" or by 3 numbers
                    second_current_indices_clean = [i for i in range(len(content) - len(CurrentSlotNumber_PlusOneClean)) if content[i:i+len(CurrentSlotNumber_PlusOneClean)] == bytes(CurrentSlotNumber_PlusOneClean, 'ascii') and (content[i+len(CurrentSlotNumber_PlusOneClean)] == ord('p') or all(chr(content[i+len(CurrentSlotNumber_PlusOneClean)+j]).isdigit() for j in range(3)))]
        
                    # Replace CurrentSlotNumber_PlusOneClean with RequestedSlotNumber_PlusOne as needed
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
                            content = content[:adjusted_index] + bytes(RequestedSlotNumber_PlusOneClean, 'ascii') + content[adjusted_index+len(CurrentSlotNumber_PlusOneClean):]
                            # Adjust the index offset after replacement
                            index_offset += len(RequestedSlotNumber_PlusOneClean) - len(CurrentSlotNumber_PlusOneClean)
        
                    # Write the modified content back to the file
                    with open(file_path, 'wb') as file:
                        file.write(content)
                    print(f"Modified: {file_path}")

    ######################################################################################
    ## Step 7b - Modify files that contain mentions to efl's\mod's if different lengths ##
    ######################################################################################

    elif len(CurrentSlotNumberClean) != len(RequestedSlotNumberClean) or (RequestedSlotNumber_PlusOneClean) == str(10):

        # Define file extensions to search for
        extensions = ['.mrl', '.448BBDD4', '.efl', '.357EF6D4', '.448BBDD4']

        # Iterate over all files in the current directory and its subdirectories
        for root, dirs, files in os.walk(current_directory):
            for filename in files:
                file_path = os.path.join(root, filename)
                if filename.endswith(tuple(extensions)):
                    print(f"Processing file: {file_path}")

                    # Read the content of the file in binary mode
                    with open(file_path, 'r+b') as file:
                        content = bytearray(file.read())

                        # Find all instances of CurrentSlotNumber_PlusOneClean
                        index = content.find(bytes(CurrentSlotNumber_PlusOneClean, 'ascii'))
                        while index != -1:
                            if index > 0 and content[index-1] == 92:  # Check if "\" occurs in ASCII before CurrentSlotNumber_PlusOneClean
                                # Calculate the length difference between RequestedSlotNumber_PlusOneClean and CurrentSlotNumber_PlusOneClean
                                length_difference = len(RequestedSlotNumber_PlusOneClean) - len(CurrentSlotNumber_PlusOneClean)
                                # Determine the position of the null byte at the end of the ASCII string
                                null_byte_index = content.find(b'\x00', index)
                                # Move the remaining ASCII string one byte to the right to accommodate the length difference
                                content[index+len(RequestedSlotNumber_PlusOneClean):null_byte_index+1] = content[index+len(CurrentSlotNumber_PlusOneClean):null_byte_index]
                                # Replace the ASCII string with RequestedSlotNumber_PlusOneClean
                                content[index:index+len(RequestedSlotNumber_PlusOneClean)] = bytes(RequestedSlotNumber_PlusOneClean, 'ascii')
                                # Move to the next occurrence of CurrentSlotNumber_PlusOneClean
                                index = content.find(bytes(CurrentSlotNumber_PlusOneClean, 'ascii'), index + len(RequestedSlotNumber_PlusOneClean) + length_difference)
                            else:
                                # Move to the next occurrence without replacing
                                index = content.find(bytes(CurrentSlotNumber_PlusOneClean, 'ascii'), index + 1)  

                        # Write the modified content back to the file
                        file.seek(0)
                        file.write(content)

                    print(f"Modified: {file_path}")
except Exception as e:
    log_message(f"Error: {str(e)}", log_file="SkinSwap_Run.txt")
# Update the progress bar
progress_bar(7, total_tasks)

#######################################################
## Step 8 - Run .bat against folder to apply changes ##
#######################################################

# Construct the current and new folder paths
current_file = f"{CharacterName}_{CurrentSlotNumber}.arc"
new_file = f"{CharacterName}_{RequestedSlotNumber}.arc"
folder_path = f"{CharacterName}_{CurrentSlotNumber}"

# Check if the folder exists
if not os.path.exists(folder_path):
    print(f"Folder '{folder_path}' not found.")
    sys.exit()

# Execute the .bat file with the folder path as an argument
def run_batch_file(folder_path):
    batch_file = 'pc-dmc4se.bat'
    try:
        subprocess.run(f'start {batch_file} "{folder_path}"', check=True, shell=True)
        print(f"Opened folder '{folder_path}' with '{batch_file}'")
    except FileNotFoundError:
        print(f"Batch file '{batch_file}' not found.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the batch file: {str(e)}")

# Run function to execute .bat file
run_batch_file(folder_path)

# Rename the file
print ("Waiting for script to finish running and cleanup")
time.sleep (2) 
try:
    os.rename(current_file, new_file)
    print(f"Renamed file: '{current_file}' to '{new_file}'")
except FileNotFoundError:
    print(f"File '{current_file}' not found.")
    exit()

# Update the progress bar
progress_bar(8, total_tasks)

###########################################################
## Step 9 - Cleanup by removing old folder and .txt file ##
###########################################################

# Define function for cleaning up remaining files    
def cleanup_directory_and_file(CharacterName, CurrentSlotNumber):
    directory_to_delete = os.path.join(current_directory, f"{CharacterName}_{CurrentSlotNumber}")
    txt_file_to_delete = os.path.join(current_directory, f"{CharacterName}_{CurrentSlotNumber}.arc.txt")
    
    if os.path.exists(directory_to_delete) or os.path.exists(txt_file_to_delete):
        confirmation = input(f"Do you want to delete '{directory_to_delete}' and '{txt_file_to_delete}'? (y/n): ").strip().lower()
        if confirmation == 'y':
            try:
                if os.path.exists(directory_to_delete):
                    shutil.rmtree(directory_to_delete)
                if os.path.exists(txt_file_to_delete):
                    os.remove(txt_file_to_delete)
            except OSError as e:
                print(f"Error: {e.strerror}")
        elif confirmation == 'n':
            print("Deletion canceled.")

# Run function to cleanup remaining files
cleanup_directory_and_file(CharacterName, CurrentSlotNumber)

# Update the progress bar
progress_bar(9, total_tasks)

print("\nScript completed!")
