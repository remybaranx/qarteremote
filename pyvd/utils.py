# -*- coding: utf-8 -*-

NO_PREVIEW_THUMBNAIL = "medias/noPreview.png"

#----------------------------------------------
# Some utils
#----------------------------------------------
def fetchPicture(p_url, p_filepath):
    """Get the image file for the thumbnail.

    Args:
    url -- image file URL
    path -- path where the file must be saved
    """
    try:
        with open(p_filepath, 'wb') as objfile:
            f = urllib2.urlopen(p_url)
            objfile.write(f.read())
        return p_filepath

    except:
        return NO_PREVIEW_THUMBNAIL

def getThumbnailPath(p_thumbnailFolder, p_video):
    """Return thumbnail path. If thumbnail is not already into the previews
    folder, he's downloaded.

    Args:
    p_thumbnailFolder -- folder to store the thumbnails
    p_video -- instance of VideoItem

    Returns:
    path of thumbnail
    """
    # Thumbnails are named with date, i.e. '2013 05 16, 13h01.jpg'
    thumbnailFilepath = os.path.join(p_thumbnailFolder, p_video.date.strip() + ".jpg")

    if not os.path.isfile(thumbnailFilepath):
        if p_video.pix is not None:
            return fetchPicture(p_video.pix, thumbnailFilepath)

        else:
            return NO_PREVIEW_THUMBNAIL

    return thumbnailFilepath
