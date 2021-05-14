Infrastructure support system for symptom-related corona tests at ETH. The project aims in testing a cohort of ETH members for SARS-Cov-2. 


To run the server, activate your virtual environment and run the following command in the root directory of the repository:
python3 manage.py runserver

To have the scrapers at a specific daily time (e.g. 16:00), run the command:
python3 manage.py scrape 16 00

In production (VM), the server is run at the port 8080 using the two following commands:
nohup python3 manage.py runserver 8080 &
nohup python3 manage.py scrape 16 00 &
