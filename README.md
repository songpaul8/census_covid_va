<a name="readme-top"></a>

#### [Datapane Dashboard Link](https://cloud.datapane.com/apps/mA26ZjA/va-covid-19-and-census-db/)

<h3 align="center">US Census + COVID-19 Analysis</h3>

  <p align="center">
    Transformed webscraped COVID-19 tracking and US 2020 Census data into a SQL database, and used Datapane to dashboard/visualize/report notable correlations.
    <br />
  </p>
</div>


<!-- ABOUT THE PROJECT -->
## About The Project

project description

<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

[![Python](https://img.shields.io/badge/python-000000?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Plotly-logo.png/220px-Plotly-logo.png" width="200" height='60'/>](https://plotly.com/)

[<img src=https://user-images.githubusercontent.com/94925327/209491518-513d879c-506f-4a5c-af37-cfe9aba34604.png width="150" height='200'/>](https://docs.python.org/3/library/sqlite3.html)

[<img src="https://miro.medium.com/max/481/1*n_ms1q5YoHAQXXUIfeADKQ.png" width="200" height='80'/>](https://pandas.pydata.org/)

[<img src="https://camo.githubusercontent.com/f7b85b8a2b1619032bfd370c9501ff87a18b08316d1ebb587fd0119f29317866/68747470733a2f2f636c6f75642e6461746170616e652e636f6d2f7374617469632f6461746170616e652d6c6f676f2d6461726b2e706e67" width="200" height='60'/>](https://docs.datapane.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

A description of repo files are below:

* sqlite_db_generator.ipynb
  -  Jupyter notebook containing code to scrape JHU COVID-19 and US 2020 Census data for the state of VA.
  -  Load data into pandas dataframes
  -  Convert dataframes into 3 separate relations into a DBMS using sqlite3

* dashboard.py
  -  Utilize sqlite3 (for querying) and datapane to generate a dashboard app to summarize and visualize notable correlations.

* db_csv.zip
  - covid-19.db : contains census (population metrics), locations (geographic details for each FIPS code) and covid_cases (daily COVID infections) tables.
  - Virginia_VA.csv : 2020 Census results for the state of VA

### Prerequisites

Outside of standard popular DS libraries (pandas, plotly), this notebook also utilizes sqlite3 for generating SQL relations and querying, as well as datapane for generating an interactive dashboard app.
The dashboard.py file can be used to create the app, but requires a login tokin that datapane authenticates. If you do not have a datapane account, a link to the generated dashboard is provided at the top of the read me and at the bottom of the dashboard.py file.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->
## Contact

Paul Song - songpaul8@gmail.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/songpaul8/census_covid_va)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
