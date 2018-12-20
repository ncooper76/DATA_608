# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 09:07:20 2018

@author: Nate
"""

#%%
import sys
import os.path
from io import StringIO
import pandas as pd
import numpy as np
#%%

#%%
file = "C:\\Users\\Nate\\Documents\\DataSet\\warcraftlogsarchive\\WoWCombatLog-archive-2018-11-06T14-20-52.865Z.txt"
raw_log = open(file, mode = 'r')
data = raw_log.read()
# Set all delimiters to spaces for consistancy
data = data.replace(',', ' ')
data = StringIO(data)
#%%

#%%
# Since the number of column betweeen rows are inconsistent, 
#I had to set the column count manually to get pandas to read all rows.
#my_cols = list(range(0,35))
#Column titles come after a lot of trial and error: The documentation is out-of-date
#My technique was to record a fight with the combat log showing so I could identify the
#column containing the damage or healing dealt
my_cols = ["Day", "Time", "Event", "sourceGUID", "sourceName", "sourceFlags", 
          "sourceRaidFlags", "destGUID", "destName", "destFlags", "destRaidFlags",
          "spellId", "spellName", "spellSchool", "amount/type", "extraInfo1", 
           "extraInfo2","dsp_resist/heal_crit","blocked", "absorbed", "critical", 
           "glancing", "crushing", "isOffHand", "extraInfo3", "extraInfo4","extraInfo5" ,
           "swing_damage","extraInfo7","extraInfo8","spell_damage"]
wow_log = pd.read_table(data,
                        delim_whitespace=True, 
                        skiprows=1, 
                        names = my_cols)
#%%

#%%
#print(wow_log.head(5))
#print(wow_log.sourceName.unique())
#print(wow_log.shape)
#%%

#%%
#Dataframe that will allow me to subset based on Boss Fights
boss_fights_df = wow_log[(wow_log.Event == 'ENCOUNTER_START') | 
                          (wow_log.Event == 'ENCOUNTER_END')]

#print(boss_fights_df.head())
#%%

#%%
#using the baove dataframe I can slice a dataframe from our Vectis Kill
vectis_kill_df = wow_log.loc[63524:109849]
victis_kill_csv = vectis_kill_df.to_csv('C:\\Users\\Nate\\Documents\\DataSet\\warcraftlogsarchive\\Vectis_kill.csv')
#%%
