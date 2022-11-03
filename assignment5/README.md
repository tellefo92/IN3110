# Assignment5
### Setup
To install requirements, do
```python
pip install -r requirements.txt
```
### Usage
All programs are ran simply by going to command line, navigating to folder containing scripts and running
```python
python script_name.py
```
All outputs are generated and saved to their respective folders

### Wikiracer
Specifically for wikiracer, the user will answer a few questions regarding links used in the program.
```python
python wiki_race_challenge.py
```
When running, the program displays which article it is currently searching through, and how many articles it has searched through in total.

Example running the task with links from the assignment, and excluding wikipedia main page from path:
```
Would you like to
(1) Run the links from the assignment, or
(2) Supply your own links?
Please select 1 or 2: 1
Include wikipedia main page as part of path?
y/n: n
Fetching links from https://en.wikipedia.org/wiki/Array_data_structure
Filtering articles found on https://en.wikipedia.org/wiki/Array_data_structure
Checked 538 of articles in total
Fetching articles from https://en.wikipedia.org/wiki/Nobel_Prize
Filtering articles found on https://en.wikipedia.org/wiki/Nobel_Prize
Checked 997 of articles in total
Fetching articles from https://en.wikipedia.org/wiki/Nobel_Prize_in_Physics
Filtering articles found on https://en.wikipedia.org/wiki/Nobel_Prize_in_Physics
Checked 1255 of articles in total
Fetching articles from https://en.wikipedia.org/wiki/Nobel_Prize_in_Chemistry
Filtering articles found on https://en.wikipedia.org/wiki/Nobel_Prize_in_Chemistry
Checked 1594 of articles in total
Fetching articles from https://en.wikipedia.org/wiki/Nobel_Prize_in_Physiology_or_Medicine
Filtering articles found on https://en.wikipedia.org/wiki/Nobel_Prize_in_Physiology_or_Medicine
```
And so on, until the path is found, when the following message is displayed:
```
Found path in 0.99565 seconds!
Path from article https://en.wikipedia.org/wiki/Nobel_Prize to https://en.wikipedia.org/wiki/Array_data_structure has 3 degrees of separation.
['https://en.wikipedia.org/wiki/Nobel_Prize', 'https://en.wikipedia.org/wiki/Nobel_Prize_in_Physiology_or_Medicine', 'https://en.wikipedia.org/wiki/Mathematical_and_theoretical_biology', 'https://en.wikipedia.org/wiki/Array_data_structure']
Links in the shortest path saved to wiki_race_challenge/assignment_links.txt
```
The program has a built in timer, and will print the time it took to find a path between two links, using time.perf_counter().