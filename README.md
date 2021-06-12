# SUMMARY

Infrastructure support system for symptom-related corona tests at ETH. The project aims at testing a cohort of ETH members for SARS-Cov-2.
The values are collected from 3 different websites once a day. A button lets the user download the table as a Word document. 

The website is launched at https://covidreport.nexus.ethz.ch/ (requires to be connected to the network of the ETH Zürich)



# RUNNING THE PROGRAM

To run the server, activate your virtual environment and run the following command in the root directory of the repository:
python3 manage.py runserver

To decide at what time should the scrapers be executed (e.g. 16:00), run the command:
python3 manage.py scrape 16 00

In production (VM), the server is run at the port 8080 using the two following commands:
nohup python3 manage.py runserver 8080 &
nohup python3 manage.py scrape 16 00 &
