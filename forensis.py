import pytsk3

# Open the disk image
image = pytsk3.Img_Info("/path/to/disk.img")

# Open the file system
fs = pytsk3.FS_Info(image)

# Improved file system support: Add support for NTFS file system
if fs.info.ftype == pytsk3.TSK_FS_TYPE_NTFS:
    # Iterate through the root directory
    root_dir = fs.open_dir(path="/")
    for file in root_dir:
        # Print the file name and size
        print(file.info.name.name, file.info.meta.size)

# Enhanced data extraction: Extract deleted files
deleted_files = []
for file in fs.open_dir(path="/").info.fs_file.lookup_inum(0):
    if file.info.meta.flags & pytsk3.TSK_FS_META_FLAG_UNALLOC:
        deleted_files.append(file)

# Cloud integration: Upload disk image to cloud storage
import cloudstorage as gcs

bucket_name = "my-bucket"
file_name = "disk.img"

gcs_file = gcs.open(f"gs://{bucket_name}/{file_name}", "w", content_type="application/octet-stream")
gcs_file.write(image.read())
gcs_file.close()

# Close the file system and the disk image
fs.close()
image.close()
