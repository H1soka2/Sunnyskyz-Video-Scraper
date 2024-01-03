def savevideofile(videolink, id):
    from urllib.request import urlopen
    try:
        downloadfile = urlopen(videolink)
        full_path = 'C:\\Users\\lukag\\OneDrive\\Desktop\\Python\\Instagram\\canvabot\\Tiktokvideos\\{}.mp4'.format(id)
        with open('savingfilelog.txt', 'r') as savefilelog:
            try:
                lines_in_savingfilelog = sum(1 for lines in savefilelog)
            except:
                lines_in_savingfilelog = 1
        with open('savingfilelog.txt', 'a') as savefile:
            savefile.write(f"{lines_in_savingfilelog}: Saving File: '{id}.mp4'\n")
        with open(full_path, 'wb') as f:
            while True:
                data = downloadfile.read(4096)
                if data:
                    f.write(data)
                else:
                    break
        return {"status": "Downloaded", "path": full_path}
    except Exception as e:
        with open('savingfilelog.txt', 'a') as savefile:
            savefile.write(f"An error occurred: {e}")
        return {"status": f"An error occurred: {e}", "path": None}

