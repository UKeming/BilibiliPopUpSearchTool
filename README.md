# BilibiliPopUpSearchTool - Bilibili 弹幕搜索工具 0.1

## Usage
After downloading the search.py file, run
```
pip install lxml
pip install requests
```
to install dependencies.

Then, create a *keywords.txt* file and add the keywords you want to search for.

Finally, run
```
python ./search.py --new
```
command to start a new search

## Parameters
If you don't specify any parameters, the program will create 10 threads for searching, and search from videos from aid 0-1000000

| Parameter | Explaination |Required|Default Value|
|:----:|:----:|:----:|:----:|
|   -s   |  the aid where the search will start from|no | 0 |
|   -c   |  the number of videos from aid [-s] to be searched|no |1000000 |
|   -t   |  the number of threads used for search |no|10 |
|  --new | if you specify this parameter, a new search will start, and previous search history will be discarded |no|False|

- Additional Info
  - The program will save all search results to results.json.
  - When a search is interrupted, it can be continued when you run the program again without --new command.
  - If you want to start a new search, you must specify --new command.
  - -c, -t, -s are only valid when you use --new.

