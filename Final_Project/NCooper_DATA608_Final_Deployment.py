# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 12:38:36 2018

@author: Nate
"""

#%%
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import figure from bokeh.plotting
from bokeh.plotting import figure
from bokeh.io import output_file, output_notebook, push_notebook, show, curdoc

# Import HoverTool, ColumnDataSource and show from bokeh.models
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models import Select

#Imports from bokeh.layouts
from bokeh.layouts import widgetbox, row, column
#%%


#%%
#using the baove dataframe I can slice a dataframe from our Vectis Kill
vectis_kill_df = pd.read_csv('https://raw.githubusercontent.com/ncooper76/DATA_608/master/Final_Project/Vectis_kill.csv')

#break the dataframe into Event-based dataframes
d = {}
for catagory in vectis_kill_df.Event.unique():
    d["df_{0}".format(catagory)]= vectis_kill_df[vectis_kill_df.Event == catagory]

print(d.keys())
#%%

#%%
Vectis_spell_damage = d["df_SPELL_DAMAGE"][(d["df_SPELL_DAMAGE"].sourceName == 'Vectis')]
Raid_spell_damage = d["df_SPELL_DAMAGE"][(d["df_SPELL_DAMAGE"].sourceName != 'Vectis')]

Vectis_swing_damage = d["df_SWING_DAMAGE_LANDED"][(d["df_SWING_DAMAGE_LANDED"].sourceName == 'Vectis') 
                                           | (d["df_SWING_DAMAGE_LANDED"].sourceName == 'Plague Amalgam')]
Raid_swing_damage = d["df_SWING_DAMAGE_LANDED"][(d["df_SWING_DAMAGE_LANDED"].sourceName != 'Vectis')
                                        & (d["df_SWING_DAMAGE_LANDED"].sourceName != 'Plague Amalgam')]

#Vectis or the Plague Amalgams do not do range damage
#Vectis_range_damage = d["df_RANGE_DAMAGE"][(d["df_RANGE_DAMAGE"].sourceName == 'Vectis') 
                                           #| (d["df_RANGE_DAMAGE"].sourceName == 'Plague Amalgam')]
Raid_range_damage = d["df_RANGE_DAMAGE"][(d["df_RANGE_DAMAGE"].sourceName != 'Vectis')
                                        & (d["df_RANGE_DAMAGE"].sourceName != 'Plague Amalgam')]

Raid_spell_damage['Time'] = pd.to_datetime(Raid_spell_damage['Time'])
Vectis_spell_damage['Time'] = pd.to_datetime(Vectis_spell_damage['Time'])

Raid_swing_damage['Time'] = pd.to_datetime(Raid_swing_damage['Time'])
Vectis_swing_damage['Time'] = pd.to_datetime(Vectis_swing_damage['Time'])

Raid_range_damage['Time'] = pd.to_datetime(Raid_range_damage['Time'])

#print(d["df_SWING_DAMAGE_LANDED"].loc[d["df_SWING_DAMAGE_LANDED"]['sourceName'] == 'Gibolt-Lightbringer'].swing_damage)
#np.ndarray.tolist(Vectis_swing_damage.sourceName.unique())

Raid_spell_heal = d["df_SPELL_HEAL"][(d["df_SPELL_HEAL"].sourceName != 'Vectis') 
                                           | (d["df_SPELL_HEAL"].sourceName != 'Plague Amalgam')]
Raid_spell_heal['Time'] = pd.to_datetime(Raid_spell_heal['Time'])

Vectis_spell_dots = d["df_SPELL_PERIODIC_DAMAGE"][(d["df_SPELL_PERIODIC_DAMAGE"].sourceName == 'Vectis') 
                                           | (d["df_SPELL_PERIODIC_DAMAGE"].sourceName == 'Plague Amalgam')]
Raid_spell_dots = d["df_SPELL_PERIODIC_DAMAGE"][(d["df_SPELL_PERIODIC_DAMAGE"].sourceName != 'Vectis') 
                                           & (d["df_SPELL_PERIODIC_DAMAGE"].sourceName != 'Plague Amalgam')]
Raid_spell_dots['Time'] = pd.to_datetime(Raid_spell_dots['Time'])
Vectis_spell_dots['Time'] = pd.to_datetime(Vectis_spell_dots['Time'])

Raid_spell_HoTs = d['df_SPELL_PERIODIC_HEAL'][(d['df_SPELL_PERIODIC_HEAL'].sourceName != 'Vectis') 
                                           & (d['df_SPELL_PERIODIC_HEAL'].sourceName != 'Plague Amalgam')]
Raid_spell_HoTs['Time'] = pd.to_datetime(Raid_spell_HoTs['Time'])

#%%

#%%
# Save the minimum and maximum values of the x column: xmin, xmax
xmin, xmax = min(Raid_spell_damage.Time), max(Raid_spell_damage.Time)


# Save the minimum and maximum values of the y column: ymin, ymax
#ymin, ymax = min(Raid_spell_damage.spell_damage), max(Raid_spell_damage.spell_damage)
# Save the minimum and maximum values of the y column: ymin, ymax
ymin, ymax = 0, 80000


#inputting a dictionary from a different data file
raid_spell = ColumnDataSource(data={
    'Time'  : Raid_spell_damage.Time,
    'Spell Damage'  : Raid_spell_damage.spell_damage,
    'sourceName' : Raid_spell_damage.sourceName,
    'spellName' : Raid_spell_damage.spellName,
    'destName' : Raid_spell_damage.destName
})

boss_spell = ColumnDataSource(data={
    'Time'  : Vectis_spell_damage.Time,
    'Spell Damage'  : Vectis_spell_damage.spell_damage,
    "sourceName" : Vectis_spell_damage.sourceName,
    "spellName" : Vectis_spell_damage.spellName,
    'destName' : Vectis_spell_damage.destName
})

#%%
raid_swing = ColumnDataSource(data={
    'Time'  : Raid_swing_damage.Time,
    'Spell Damage'  : Raid_swing_damage.swing_damage,
    'sourceName' : Raid_swing_damage.sourceName,
    'destName' : Raid_swing_damage.destName
})
#%%
boss_swing = ColumnDataSource(data={
    'Time'  : Vectis_swing_damage.Time,
    'Spell Damage'  : Vectis_swing_damage.swing_damage,
    "sourceName" : Vectis_swing_damage.sourceName,
    'destName' : Vectis_swing_damage.destName
})
#%%
raid_range = ColumnDataSource(data={
    'Time'  : Raid_range_damage.Time,
    'Spell Damage'  : Raid_range_damage.spell_damage,
    'sourceName' : Raid_range_damage.sourceName,
    'spellName' : Raid_range_damage.spellName,
    'destName' : Raid_range_damage.destName
})
#%%    
raid_heals = ColumnDataSource(data={
    'Time'  : Raid_spell_heal.Time,
    'Heals'  : Raid_spell_heal.spell_damage,
    "sourceName" : Raid_spell_heal.sourceName,
    'spellName' : Raid_spell_heal.spellName,
    'destName' : Raid_spell_heal.destName
})    
#%%
#inputting a dictionary from a different data file
raid_dots = ColumnDataSource(data={
    'Time'  : Raid_spell_dots.Time,
    'DoTs'  : Raid_spell_dots.spell_damage,
    "sourceName" : Raid_spell_dots.sourceName,
    'spellName' : Raid_spell_dots.spellName,
    'destName' : Raid_spell_dots.destName
})
#%%
boss_dots = ColumnDataSource(data={
    'Time'  : Vectis_spell_dots.Time,
    'DoTs'  : Vectis_spell_dots.spell_damage,
    "sourceName" : Vectis_spell_dots.sourceName,
    'spellName' : Vectis_spell_dots.spellName,
    'destName' : Vectis_spell_dots.destName
})
#%%    
raid_hots = ColumnDataSource(data={
    'Time'  : Raid_spell_HoTs.Time,
    'Heals'  : Raid_spell_HoTs.spell_damage,
    "sourceName" : Raid_spell_HoTs.sourceName,
    "spellName" : Raid_spell_HoTs.spellName,
    'destName' : Raid_spell_HoTs.destName
})
#%%
raid_total_damage =  Raid_spell_dots.spell_damage.sum() + Raid_spell_damage.spell_damage.sum() + Raid_range_damage.spell_damage.sum() + Raid_swing_damage.swing_damage.astype(float).sum()

#%%
    
raid_total_heals =  Raid_spell_HoTs.spell_damage.sum() + Raid_spell_heal.spell_damage.sum() 

#boss_total_damage = 
#Vectis_spell_dots.spell_damage.sum() + Vectis_spell_damage.spell_damage.sum() + Vectis_swing_damage.swing_damage.astype(float).sum()


name = 'Novakaan-Lightbringer'
names = ['Player', 'Orange Team']

player_total_damage =  ColumnDataSource(data={
        'Name' : names,
        'Damage': [Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].spell_damage.sum() + Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].spell_damage.sum() + Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].spell_damage.sum() + Raid_swing_damage.loc[Raid_swing_damage['sourceName'] == name].swing_damage.astype(float).sum(), raid_total_damage]
})

player_total_heals =  ColumnDataSource(data={
        'Name' : names,
        'Heals' : [Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].spell_damage.sum() + Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].spell_damage.sum(), raid_total_heals] 
})    
    
# Define the callback function: update_plot
def update_plot(attr, old, new):
    # set the name to `select.value` and `source.data = new_data`
    name = raid_select.value
    if(name == 'Orange Team'):
        new_data1 = {
            'Time'  : Raid_spell_damage.Time,
            'Spell Damage'  :Raid_spell_damage.spell_damage,
            'sourceName' : Raid_spell_damage.sourceName,
            'spellName' : Raid_spell_damage.spellName,
            'destName' : Raid_spell_damage.destName
        }
    
        new_data2 = {
            'Time'  : Raid_swing_damage.Time,
            'Spell Damage'  :Raid_swing_damage.swing_damage,
            'sourceName' : Raid_swing_damage.sourceName,
            'destName' : Raid_swing_damage.destName
        }
    
        new_data3 = {
            'Time'  : Raid_range_damage.Time,
            'Spell Damage'  :Raid_range_damage.spell_damage,
            'sourceName' : Raid_range_damage.sourceName,
            'spellName' : Raid_range_damage.spellName,
            'destName' : Raid_range_damage.destName
        }
        
        new_data4 = {
            'Time'  : Raid_spell_dots.Time,
            'DoTs'  : Raid_spell_dots.spell_damage,
            "sourceName" : Raid_spell_dots.sourceName,
            'spellName' : Raid_spell_dots.spellName,
            'destName' : Raid_spell_dots.destName
        }
        
        new_data5 = {
            'Time'  : Raid_spell_heal.Time,
            'Heals'  : Raid_spell_heal.spell_damage,
            "sourceName" : Raid_spell_heal.sourceName,
            'spellName' : Raid_spell_heal.spellName,
            'destName' : Raid_spell_heal.destName
        }
        
        new_data6 = {
            'Time'  : Raid_spell_HoTs.Time,
            'Heals'  : Raid_spell_HoTs.spell_damage,
            "sourceName" : Raid_spell_HoTs.sourceName,
            "spellName" : Raid_spell_HoTs.spellName,
            'destName' : Raid_spell_HoTs.destName
        }
        
        new_data7 = {
                'Name' : names,
                'Damage' : [raid_total_damage, raid_total_damage]
        }
        
        new_data8 = {
               'Name' : names,
               'Heals' : [raid_total_heals, raid_total_heals] 
        }

    else:    
        new_data1 = {
            'Time'  : Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].Time,
            'Spell Damage'  :Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].spell_damage,
            'sourceName' : Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].sourceName,
            'spellName' : Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].spellName,
            'destName' : Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].destName
        }
    
        new_data2 = {
            'Time'  : Raid_swing_damage.loc[Raid_swing_damage['sourceName'] == name].Time,
            'Spell Damage'  :Raid_swing_damage.loc[Raid_swing_damage['sourceName'] == name].swing_damage,
            'sourceName' : Raid_swing_damage.loc[Raid_swing_damage['sourceName'] == name].sourceName,
            'destName' : Raid_swing_damage.loc[Raid_swing_damage['sourceName'] == name].destName
        }
    
        new_data3 = {
            'Time'  : Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].Time,
            'Spell Damage'  :Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].spell_damage,
            'sourceName' : Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].sourceName,
            'spellName' : Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].spellName,
            'destName' : Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].destName
        }
        
        new_data4 = {
            'Time'  : Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].Time,
            'DoTs'  : Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].spell_damage,
            "sourceName" : Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].sourceName,
            'spellName' : Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].spellName,
            'destName' : Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].destName
        }
        
        new_data5 = {
            'Time'  : Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].Time,
            'Heals'  : Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].spell_damage,
            "sourceName" : Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].sourceName,
            'spellName' : Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].spellName,
            'destName' : Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].destName
        }
        
        new_data6 = {
            'Time'  : Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].Time,
            'Heals'  : Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].spell_damage,
            "sourceName" : Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].sourceName,
            "spellName" : Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].spellName,
            'destName' : Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].destName
        }
        
        new_data7 = {
                'Name' : names,
                'Damage': [Raid_spell_dots.loc[Raid_spell_dots['sourceName'] == name].spell_damage.sum() + Raid_spell_damage.loc[Raid_spell_damage['sourceName'] == name].spell_damage.sum() + Raid_range_damage.loc[Raid_range_damage['sourceName'] == name].spell_damage.sum() + Raid_swing_damage.loc[Raid_swing_damage['sourceName'] == name].swing_damage.astype(float).sum(), raid_total_damage]
        }
        
        new_data8 = {
                'Name' : names,
                'Heals' : [Raid_spell_HoTs.loc[Raid_spell_HoTs['sourceName'] == name].spell_damage.sum() + Raid_spell_heal.loc[Raid_spell_heal['sourceName'] == name].spell_damage.sum(), raid_total_heals] 
        }
    
    raid_spell.data = new_data1
    raid_swing.data = new_data2
    raid_range.data = new_data3
    raid_dots.data = new_data4
    raid_heals.data = new_data5
    raid_hots.data = new_data6
    player_total_damage.data = new_data7
    player_total_heals.data = new_data8
    

options = np.ndarray.tolist(Raid_spell_damage.sourceName.unique())
options.append('Orange Team')
raid_select = Select(title="Player:", value='Orange Team', options=options)
# Attach the callback to the 'value' property of slider
raid_select.on_change('value', update_plot)
# Create a HoverTool object: hover
#show(widgetbox(raid_select))

hover = HoverTool(tooltips = [('sourceName','@sourceName'), ('spellName','@spellName'), ('destName', '@destName')])


#create a formated plot
plot = figure(title='Raid Direct Spell Damage vs. Time', x_axis_type="datetime",
              plot_height=450, plot_width=1200,
              x_axis_label = 'Time', y_axis_label = 'Damage',
              x_range=(xmin, xmax), y_range=(ymin, ymax),
              tools='box_select'
             )
# Add the HoverTool object to figure p
plot.add_tools(hover)


plot.circle('Time','DoTs', source = raid_dots, color='darkorange', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)
plot.circle('Time','DoTs', source = boss_dots, color='firebrick', size=4,alpha=0.8
           ,selection_color = 'blue', nonselection_alpha = 0.1)
plot.square('Time','Spell Damage', source = raid_spell, color='darkorange', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)
plot.square('Time','Spell Damage', source = boss_spell, color='firebrick', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)
plot.triangle('Time','Spell Damage', source = raid_range, color='darkorange', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)
plot.diamond('Time','Spell Damage', source = raid_swing, color='darkorange', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)
plot.diamond('Time','Spell Damage', source = boss_swing, color='firebrick', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)

#create a formated plot
plot2 = figure(title='Raid Healing vs. Time', x_axis_type="datetime",
              plot_height=450, plot_width=1200,
              x_axis_label = 'Time', y_axis_label = 'Heals',
              x_range=(xmin, xmax), y_range=(ymin, ymax),
              tools='box_select'
             )

# Add the HoverTool object to figure p
plot2.add_tools(hover)


plot2.circle('Time','Heals', source = raid_hots, color='darkorange', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)

plot2.triangle('Time','Heals', source = raid_heals, color='darkorange', size=4,alpha=0.8
            ,selection_color = 'red', nonselection_alpha = 0.1)

bar1 = figure(x_range = names,title = 'Player and Total Damage Output', plot_height=350)
bar1.vbar(x='Name', top='Damage', source = player_total_damage, width=1, color = 'orangered', alpha=1)

bar2 = figure(x_range = names,title = 'Player and Total Healing Output',plot_height=350)
bar2.vbar(x='Name', top='Heals', source = player_total_heals, width=1, color = 'orangered', alpha=1)


#%%


#%%
# Make a row layout of widgetbox(slider) and plot and add it to the current document
column1 = column(widgetbox(raid_select,sizing_mode='scale_both'),bar1, bar2)
column2 = column(plot,plot2)
layouts = row(column1,column2)
curdoc().add_root(layouts)
output_file('orange_v_vectis.html')
show(layouts)
#%%