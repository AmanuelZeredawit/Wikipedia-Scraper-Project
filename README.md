# Wikipedia-Scraper-Project

This project first queries an API for a list of countries and their past leaders. Then it scraps Wikipedia to get the content 
of their first paragraph. It then filters and cleans their short bio.

## Detailed Description

The program first checks the status of the connection to the API which has a list of countries with leaders' detail. Then it creates cookies
to get access to query info about the countries and a list of leaders. with the list of leaders and their Wikipedia URL the get_first_paragraph()
function get the bio of the leaders from the Wikipedia website. It also filters out the HTML tags to get only the content of their first paragraph.
And finally, the output of the query is saved  to a JSON file(leaders.json)

In this program 

## Usage
create a virtual environment and install python 3 and  you can run go to the directory of the file 
using cmd you can run it with this command: python leaders_scrappey.py

## Installation
This version of the project does not come with the installation file. we will come with full package in the next version.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature
5. Submit a pull request :D



