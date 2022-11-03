from typing import Optional

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

import webvisualization_plots

# create app variable (FastAPI instance)
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount one or more static directories,
# e.g. your auto-generated Sphinx documentation with html files
app.mount(
    # the URL where these files will be available
    "/static",
    StaticFiles(
        # the directory the files are in
        directory="static/",
        html=True,
    ),
    # an internal name for FastAPI
    name="static",
)


@app.get("/")
def plot_reported_cases_per_million_html(request: Request):
    """
    Root route for the web application.
    Handle requests that go to the path "/".
    """
    return templates.TemplateResponse(
        "plot_reported_cases_per_million.html",
        {
            "request": request,
            # further template inputs here
            "countries": webvisualization_plots.get_countries()
        },
    )


@app.get("/plot_reported_cases_per_million.json")
def plot_reported_cases_per_million_json(countries: Optional[str] = None, 
                                         start: Optional[str] = None, 
                                         end: Optional[str] = None,
                                         typeofCases: Optional[str] = "daily"):
    try:
        countries = countries.split(",")
    except AttributeError:
        countries = webvisualization_plots.get_highest_countries(end)
    countries = tuple(countries)
    """Return json chart from altair"""
    cases = webvisualization_plots.plot_reported_cases_per_million(countries=countries, start=start, end=end, typeofCases=typeofCases).properties(width="container")
    
    return cases.to_dict()

@app.get("/help")
def help(request: Request):
    return templates.TemplateResponse(
        "help.html",
        {
            "request": request
        }
    )


def main():
    """Called when run as a script
    Should launch your web app
    """
    print("Downloading most recent data file..")
    webvisualization_plots.download_csv()
    print("Download complete. Initializing app.")

    import uvicorn

    uvicorn.run(app)


if __name__ == "__main__":
    main()