import pandas as pd
import pymysql
from sqlalchemy import create_engine

connectionString = "server=reza.mysql.database.azure.com;port=3306;user=reza;password=GoonCentral123;database=CoastalErosion"
engine = create_engine(connectionString)

filePath = "/Users/colegauerkemacbook/Desktop/fall2025Notes/CSC4330/CoastalErosionProject/DataManagement/RawData/VerifiedWaterLevelsGrandIsle.csv"
df = pd.read_csv(filePath)
df.to_sql('VerifiedWaterLevels', engine, if_exists='append', index=False, 
          method='multi', chunksize=5000)