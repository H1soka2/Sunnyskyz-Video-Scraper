# Sunnyskyz TikTok Scraper

This repository contains a Python script for scraping TikTok videos from sunnyskyz.com. The scraped videos are then edited using [CanvaBot.py](https://github.com/H1soka2/CanvaAutomationSuite/blob/main/CanvaBot.py) and uploaded to Google Drive with [DriveUpload.py](https://github.com/H1soka2/CanvaAutomationSuite/blob/main/DriveUpload.py).

## Overview

This script is designed for exhibition purposes and showcases the process of scraping TikTok videos, performing edits, and uploading to Google Drive. The code is reusable, making it suitable for long-term usage.


## How it Works

1. **Scraping TikTok Videos:**
   - The script navigates to sunnyskyz.com to extract TikTok videos.

2. **Editing with CanvaBot.py:**
   - CanvaBot.py is a separate Python script for video editing. It is used to modify the text and content of the scraped TikTok videos.

3. **Uploading to Google Drive with DriveUpload.py:**
   - DriveUpload.py is another separate script designed for uploading videos to Google Drive. The edited videos are stored in Google Drive.

4. **Logging Information:**
   - The script generates a [log.json](https://github.com/H1soka2/Sunnyskyz-Video-Scraper/blob/main/log.json) file that stores information about the scraping and editing process.

5. **Saving File Logs:**
   - The script creates a [savingfilelog.txt](https://github.com/H1soka2/Sunnyskyz-Video-Scraper/blob/main/savingfilelog.txt) file to log details about the saving process.

6. **CSV Output:**
   - The script generates a CSV file with information about the scraped and edited videos.

[View CSV File](https://github.com/H1soka2/Sunnyskyz-Video-Scraper/blob/main/csv/Excelfile2.csv)

## References

- [CanvaBot Repository](https://github.com/H1soka2/CanvaAutomationSuite)

Feel free to explore the code and adapt it according to your needs. If you encounter any issues or have questions, please create an issue in this repository.

---

**Note:** This repository is intended for exhibition purposes and may require adjustments for practical use. Ensure compliance with sunnyskyz.com terms of service when using the scraping script.
