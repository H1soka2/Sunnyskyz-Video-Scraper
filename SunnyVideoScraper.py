from bs4 import BeautifulSoup
from urllib.request import urlopen
from CanvaBot_copy import CanvaVideo
import tiktokdownloader, checkjson, DriveUpload, requests, json, time, re
import pandas as pd

class FetchVideo:
    def __init__(self, amount: int) -> None:
        """
        Initializes a new instance of the FetchVideo class.

        Args:
            amount (int): The number of videos to fetch.
        """
        self.amount = amount
        self.canva_bot = CanvaVideo()
        self.fetch_video()

    def editvideo(self, video: str, text: str, videoid: str) -> bool:
        # Method to edit video using CanvaBot, returns True if successful, False otherwise
        if not self.canva_bot.change_video_text(text=text):
            return False
        if not self.canva_bot.change_video(video_path=video, foldername=videoid):
            return False

    def fetch_video(self) -> bool:
        # Method to fetch videos
        how_many_video = self.amount
        reserved_characters_pattern = r'[\\/:*?"<>|]'
        pattern = r'\d{5}'
        
        # Finds newest video id
        sunnyskitz_happy_videos = 'https://www.sunnyskyz.com/happy-videos/{}'
        main_page = requests.get("https://www.sunnyskyz.com/happy-videos")
        main_html = main_page.text
        main_soup = BeautifulSoup(main_html, "lxml")
        new = main_soup.find('a', class_="newslist")
        newest_video = re.findall(pattern, str(new))[0]

        master_list = []
        indexes = []
        counter = 1
        jsondata_index = -1

        # Loop through videoids
        for videoid in range(int(newest_video), -1 , -1):
            # Check if the videoid is to be skipped
            check_skips = checkjson.errjs(videoid)
            if check_skips['skip']:
                continue
            else:
                errlist1 = check_skips['errlist']
            
            # Check the status of the video
            data = checkjson.checkid(videoid)
            parsed_data = data["existing_data"]

            if data["downloaded"]:
                print(f"Video already exists: {videoid}")
                continue
            elif data["jsondata"]:
                failed_to_download = data["jsondata"]
                jsondata_index = data["index"]
                
                # Download the video
                redownload = tiktokdownloader.download_tiktok_video(data["jsondata"]["DownloadManually"], data["jsondata"]["StoryTitle"])

                if redownload[0] == "Downloaded":
                    # Update the json data with the download status
                    failed_to_download["Status"].update(redownload[0])
                    parsed_data[jsondata_index] = failed_to_download
                    checkjson.updatejson(parsed_data)

                    # Get file download link and update json data
                    Drivevideo = DriveUpload.get_file_download_link(json_hp["StoryTitle"].replace(' ', '_'))
                    failed_to_download["DownloadManuallyDrive"] = Drivevideo["downloadUrl"]
                    failed_to_download["PreviewVideo"] = Drivevideo["previewUrl"]
                    failed_to_download["VideoId"] = Drivevideo["driveId"]
                    parsed_data[jsondata_index] = failed_to_download

                    # Edit the video using CanvaBot
                    if not self.editvideo(
                        video    = redownload[2],
                        text     = failed_to_download['StoryTitle'],
                        videoid = str(videoid)):
                        return False

                    # Check if the process should stop
                    if counter != how_many_video:
                        indexes.append(videoid)
                        counter += 1
                    else:
                        print(f"{how_many_video} Videos Have Successfully Downloaded")
                        self.canva_bot.Close()
                    continue

            # Get video link and proceed if it is a TikTok video
            video_link = sunnyskitz_happy_videos.format(videoid)
            response = requests.get(video_link)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')
            json_hp = {}

            try:
                # Check if the page has a TikTok video link
                tiktok_link = soup.find('blockquote')['cite']
                print(f"                                    Scraping in progress: {round((((counter-1) / int(how_many_video))*100), 2)}% complete")
            except:
                # Skip if there is no TikTok video link
                errlist1.append(str(videoid))
                with open('err.json', 'w') as errw:
                    skip_list = json.dumps(errlist1, indent=2)
                    errw.write(skip_list)
                continue

            # Get upload date, story title, video URL, description, and download the TikTok video
            json_hp["UploadDate"] = soup.p.text
            story_title = soup.find('h2', class_="storytitle").text
            filtered_story_title = re.sub(reserved_characters_pattern, '', story_title)
            json_hp["StoryTitle"] = filtered_story_title
            json_hp["VideoURL"] = video_link
            div = soup.find('div', class_='storytext onlynews')
            json_hp["Description"] = div.find_all('p')[2].text.strip()
            tiktok_video_status = tiktokdownloader.download_tiktok_video(tiktok_link, filtered_story_title)
            json_hp["Status"] = tiktok_video_status[0]
            json_hp["DownloadManually"] = tiktok_video_status[1]

            # If the video is downloaded, edit and upload it using CanvaBot
            if json_hp['Status'] == "Downloaded":
                if not self.editvideo(
                    video    = tiktok_video_status[2], 
                    text     = json_hp['StoryTitle'], 
                    videoid = str(videoid)):
                    return False

            # Get file download link and update json data
            json_hp["DownloadManuallyDrive"] = None
            if json_hp["Status"] == "Downloaded":
                Drivevideo = DriveUpload.get_file_download_link(json_hp["StoryTitle"].replace(' ', '_'))
                json_hp["DownloadManuallyDrive"] = Drivevideo["downloadUrl"]
                json_hp["PreviewVideo"] = Drivevideo["previewUrl"]
                json_hp["VideoId"] = Drivevideo["driveId"]

            json_hp["SunnySkyzId"] = videoid

            # Append the dictionary to existing data
            if jsondata_index == -1:
                parsed_data.append(json_hp)
            else:
                parsed_data[jsondata_index] = json_hp

            checkjson.updatejson(parsed_data)

            json_hp.pop("SunnySkyzId")
            master_list.append(json_hp)
            indexes.append(videoid)

            # Check if the process should stop
            if counter != how_many_video:
                if tiktok_video_status[0] == "Downloaded":
                    counter += 1
            elif tiktok_video_status[0] != "Downloaded":
                continue
            else:
                print(f"{how_many_video} Videos Have Successfully Downloaded")
                self.canva_bot.Close()
                break

        # Create a DataFrame from the master list and save it to a CSV file
        df = pd.DataFrame(master_list, index=indexes)
        csv_file_path = fr'csv\Excelfile {time.ctime()[:10]}.csv'
        df.to_csv(csv_file_path)

        return True

# Entry point of the script
if __name__ == "__main__":
    amount = int(input("How Many Video You Want to Scrape: "))
    FetchVideo(amount)
