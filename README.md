I have (unfortunately) invested considerable time into collecting some wonderful videos from TikTok over the years, mostly incredible found sounds, acapellas, or sound design tutorials. 

I'd hate to lose them, so I've written a script to download them all.

Made with Claude 3.5 Sonnet in about 10 minutes, please excuse any bugs. Feel free to submit a PR if you find any.

# Python setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# Download HTML file for each TikTok collection

Go to your profile, ie: [https://www.tiktok.com/@your_username](https://www.tiktok.com/@your_username)

Go to `Favorites > Collections`. And for each collection, you'll click into it. For example, your "funny" collection might be at the URL: [https://www.tiktok.com/@your_username/collection/funny-23462378436368476](https://www.tiktok.com/@your_username/collection/funny-23462378436368476)

Then, SCROLL ALL THE WAY DOWN to load all the videos, then right click and save the page as HTML into the `collection_htmls` folder.

Inside the `collection_htmls` folder, you should have a file for each collection. There will also be a folder with the same name, you can delete those. We just need the HTML files.

# Extract the URLs from the HTML files

```bash
cd tiktok_collection_downloader/
python collect_urls.py
```

This will create a CSV file in the root directory called `tiktok_video_info.csv`.

# Download the videos

```bash
python download_all.py
```

This will download all the videos into the `videos` folder.

Note: the `download_all.py` script will wait 3 seconds between each video download to avoid rate limiting. If you'd like to download faster, you can remove the `time.sleep(WAIT_SECS)` line in the `download_all.py` script, or set the `WAIT_SECS` variable to any number of seconds you'd like. I'd suggest starting with 3 seconds to make sure you're not rate limited.
