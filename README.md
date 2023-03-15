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
python ./search.py
```
command to start the search

## Parameters
If you don't specify any parameters, the program will create 10 threads for searching, and search from videos from aid 0-1000000

| Parameter | Explaination |Required|
|:---|:----:|---:|
|   -s   |  specify the aid where the search will start|no |
