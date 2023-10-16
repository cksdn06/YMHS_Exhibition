from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'output.jpg', 'parents': [{'id': '1CBFFj7OqV9jC8htkotR6ytYYgnmPvmPw'}]})
file1.SetContentFile('C:\\tf\\output.jpg')
file1.Upload()
