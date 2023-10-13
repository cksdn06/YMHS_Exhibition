from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

gauth = GoogleAuth()
gauth.LocalWebserverAuth()  # Creates local webserver and automatically handles authentication.
drive = GoogleDrive(gauth)

folder_name = "tf"
zip_file_name = folder_name + ".zip"

# Compress the folder into a zip file
import shutil
shutil.make_archive(zip_file_name, 'zip', folder_name)

# Create a GoogleDriveFile instance with the name ozf the zip file
file = drive.CreateFile({'title': zip_file_name})

# Upload the zip file to Google Drive
file.Upload()

# Delete the local zip file after uploading
os.remove(zip_file_name)

# Find the uploaded folder
folder = drive.ListFile({'q': f'title="{zip_file_name}"'}).GetList()[0]

# Get the folder ID
folder_id = folder['1_s8lHeuMD6gCLllJwUP3deEWZSZOUApK']

# Specify the destination folder ID where you want to move the folder
destination_folder_id = "your_destination_folder_id"

# Move the folder to the destination
folder['parents'] = [{'id': destination_folder_id}]
folder.Upload()