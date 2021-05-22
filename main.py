import dropbox
import os
from threading import Timer

def getItem():

    # connecting dropbox with api key
    dbx = dropbox.Dropbox('KEY_SHOULD_BE_HERE')
    dropbox_folder_content = dbx.files_list_folder('/Uploads')

    # sorting the contents of Uploads folder, sorting key is the uploaded date to the server,
    # we want to take the newest files first
    dropbox_folder_content.entries.sort(key=lambda x: x.server_modified)

    # running on the sorted list of files in the folder, from the newest to the oldest
    # this is done in order to keep consistency and checking that all files from the server
    # are in our system, for example to solve a case where we accidentally delete a file in our system,
    # and we need to download it again from the server.
    for i in range(len(dropbox_folder_content.entries)):
        file_to_download = dropbox_folder_content.entries[i]

        # splitting the file name to different variables according to the agreed format
        device, day, month, year, time = file_to_download.name.split('_')
        device_path = device
        year_path = os.path.join(device_path,year)
        month_path = os.path.join(year_path,month)
        file_path = os.path.join(month_path,day + '_' + time)

        # If the file already exists in our system, we continue to the next file
        if os.path.exists(file_path):
            continue
        # creating a folder for the device name
        if not os.path.exists(device_path):
            os.mkdir(device)
        # creating a folder for a year for each device
        if not os.path.exists(year_path):
            os.mkdir(year_path)
        # creating a folder for a month of the year for each device
        if not os.path.exists(month_path):
            os.mkdir(month_path)
        # downloading the file and saving it in the folder.
        # we can be sure that the file doesn't exist in our system.
        dbx.files_download_to_file(file_path, file_to_download.path_display)
    # running this script every 10 minutes. We can run it every few hours to check for new items
    Timer(600,getItem).start()

# starting the script immediately
Timer(1,getItem).start()

