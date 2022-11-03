# Assignment 6
## Requirements
To run the program, quite a few packages are required. Install them by running the following commands
```bash
pip install pandas
pip install altair
pip install tqdm
pip install fastapi
pip install uvicorn
pip install -U urllib   # Necessary to get the latest version of urllib.request.urlretrieve
```

## Usage
To launch the app, simply run the following command:
```bash
python webvisualization.py
```
This will prompt a download of the latest covid data directly from the owid github.\
A progress bar will show how much of the file is downloaded, and how much time is estimated to be left.\
\
Once the download is complete, the app is launched, and can be viewed at (usually) 127.0.0.1:8000.\
The app has most of the functionality described in assignment 6.

## Missing functionality / anomalies
### Launch issue
Sometimes when launching the app, it will get stuck on the step in the image below
![Stuck](static/startup_issue.jpg)
To resolve this issue, I've found that pressing ctrl+c in the terminal does not shut down the app\
but instead forces it to the next steps
![After pressing ctrl+c](static/startup_complete.jpg)
### Missing documentation / help page
As I had to focus on other exams, and already had enough points to pass the course, \
I focused exclusively on the app, and did not prioritize creating documentation or a help page.\
I know this isn't good practice, but I simply did not have time to prioritize it.
