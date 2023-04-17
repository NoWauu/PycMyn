import csv

with open('ressources/niveaux.csv','r') as file:
    TABLE = list(csv.DictReader(file, delimiter=';'))
    print(TABLE)