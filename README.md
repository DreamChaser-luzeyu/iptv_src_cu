A collection of Chinese IPTV live sources. Optimized for China Unicom.

All collected from the internet. You could either use my collection or collect on your own.

 ## Working flow
 - Collect `.m3u` files or urls to `.m3u` files
 - Put `.m3u` files into `local_list` folder, and append the urls to the `remote_url_list.txt`
 - Clear the content in the `full.m3u`
 - `[Github Action]` Run `gen_full.py`
 - Run `IPTV Checker` and export channels needed to `filtered_list` folder
 - `[Github Action]` Clear content in `full_filtered.m3u` and run `gen_filtered.py`
 - Either use the `full_filtered.m3u` file or use the github raw link to it
