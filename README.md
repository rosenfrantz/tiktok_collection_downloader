Made with Claude 3.5 Sonnet in about 10 minutes, please excuse any bugs. Feel free to submit a PR if you find any.

## Disclaimer

This script is merely for research purposes. Anything you do with the code is your own responsibility.

## Python setup

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Download HTML file for each TikTok collection

Go to your profile, ie: [https://www.tiktok.com/@your_username](https://www.tiktok.com/@your_username)

Go to `Favorites > Collections`. And for each collection, you'll click into it. For example, your "funny" collection might be at the URL: [https://www.tiktok.com/@your_username/collection/funny-23462378436368476](https://www.tiktok.com/@your_username/collection/funny-23462378436368476)

Then, SCROLL ALL THE WAY DOWN to load all the videos, then right click and save the page as HTML into the `collection_htmls` folder.

Inside the `collection_htmls` folder, you should have a file for each collection. There will also be a folder with the same name, you can delete those. We just need the HTML files.

## Extract the URLs from the HTML files

```bash
cd tiktok_collection_downloader/
python collect_urls.py
```

This will create a CSV file in the root directory called `tiktok_video_info.csv`.

## Download the videos

```bash
python download_all.py
```

This will download all the videos into the `videos` folder.

Note: the `download_all.py` script will wait 3 seconds between each video download to avoid rate limiting. If you'd like to download faster, you can remove the `time.sleep(WAIT_SECS)` line in the `download_all.py` script, or set the `WAIT_SECS` variable to any number of seconds you'd like. I'd suggest starting with 3 seconds to make sure you're not rate limited.

Your folder structure should look something like this:

```
$ tree -L 3
.
├── LICENSE.md
├── README.md
├── collect_urls.py
├── collection_htmls
│   ├── acapellas.html
│   ├── funny.html
│   └── other.html
├── download_all.py
├── requirements.txt
├── tiktok_video_info.csv
└── videos
    ├── acapellas
    │   ├── 67694855112687464246_Untitled_722158053954769438469.mp4
    │   ├── yebbahq_Jacob_Collier_and_Yebba_need_to_collab_NOW._7311829283289255199.mp4
    |   ...
    │   └── yebbahq_Untitled_7311829283289255199.mp4
    ├── funny
    │   ├── 67694855112268746246_Untitled_72215805954245958469.mp4
    │   ├── cosmicacademy_Untitled_74518197923678741294.mp4
    │   ├── hardacademysound_Lurker_bass_patch_in_serum_____74430635850444066091.mp4
    │   ...
    │   └── productionmusiclive____Beautiful_vocal_chords_74442188634492861216.mp4
    └── other
        ├── 6769482551148746246_Untitled_7221580423476958469.mp4
        ├── 6784805723451112390_Untitled_7134276438226914603.mp4
        ...
        └── zhannapiano_my_job_is_teacher_7302532742752161056.mp4
```
