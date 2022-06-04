#!/usr/bin/env python
# coding: utf-8

# # Electricity Imports

# In[1]:


import pandas as pd


# In[2]:


countries = pd.read_csv('../raw_data/CountryCodes.csv', encoding = 'unicode_escape')
countries.dropna(inplace=True)
countries.head()


# In[3]:


countries.info()


# In[4]:


countries[countries['Alpha_2_code'].isnull()==True]


# # EU Countries Dictionary

# In[5]:


EU_countries = pd.DataFrame.from_dict([{'Belgium': 'BE', 'Bulgaria': 'BG', 'Czechia': 'CZ', 'Denmark': 'DK', 'Germany': 'DE', 'Estonia': 'EE', 'Ireland': 'IE', 'Greece': 'EL',
                'Spain': 'ES', 'France': 'FR', 'Croatia': 'HR', 'Italy': 'IT', 'Cyprus': 'CY', 'Latvia': 'LV', 'Lithuania': 'LT', 'Luxembourg': 'LU', 
                'Hungary': 'HU', 'Malta': 'MT', 'Netherlands': 'NL', 'Austria': 'AT', 'Poland': 'PL', 'Portugal': 'PT', 'Romania': 'RO', 'Slovenia': 'SI',
                'Slovakia': 'SK', 'Finland': 'FI', 'Sweden': 'SE'}])
EU_countries = EU_countries.T.reset_index()
EU_countries.rename(columns={'index': 'EU_country', 0: 'Alpha_2_code'}, inplace=True)
EU_countries


# # Imports by Country

# In[6]:


imports = pd.read_csv('../raw_data/ElecImportsByPartnerCountry.csv', encoding = 'unicode_escape')
imports.head()


# In[7]:


imports.info()


# In[8]:


# merge imports df with countries df
imports = imports.merge(countries, on='Alpha_2_code', how='left')

# create new column 'EU?' and fill with True/False based on whether country is in EU dictionary
imports['EU?'] = imports['Alpha_2_code'].isin(EU_countries['Alpha_2_code'])
imports


# In[9]:


# rename Alpha 2 code in countries df to 'Partner_country'
countries.rename({'Alpha_2_code': 'partner'}, axis=1, inplace=True)
countries


# In[10]:


# create new df EU_imports by merging imports and countries to get the name of the partner countries
EU_imports = imports.merge(countries, on='partner', how='left')
EU_imports


# ## Rearrange columns

# In[11]:


EU_imports.columns


# In[12]:


EU_imports = EU_imports[['Alpha_2_code', 'Country_x', 'EU?', 'partner', 'Country_y', 'siec', 'unit',
                         '1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998',
                         '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007',
                         '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016',
                         '2017', '2018', '2019', '2020']]
EU_imports


# In[13]:


EU_imports.rename({'Country_x': 'Country', 'Country_y': 'Partner_country'}, axis=1, inplace=True)
EU_imports


# In[14]:


# Filter out non-EU importing countries
EU_imports_filtered = EU_imports[EU_imports['EU?'] == True]
EU_imports_filtered


# In[15]:


EU_imports_filtered = EU_imports_filtered[EU_imports_filtered['siec'] == 'E7000']
EU_imports_filtered


# In[16]:


EU_imports_filtered = EU_imports_filtered[EU_imports_filtered['unit'] == 'GWH']
EU_imports_filtered


# In[17]:


EU_imports_filtered.reset_index(drop=True, inplace=True)
EU_imports_filtered


# In[18]:


EU_imports_filtered.dtypes


# Change data type of years to float

# In[19]:


years_columns_type = {'1990': float, '1991': float, '1992': float, '1993': float, '1994': float,
                      '1995': float, '1996': float, '1997': float, '1998': float, '1999': float,
                      '2000': float, '2001': float, '2002': float, '2003': float, '2004': float,
                      '2005': float, '2006': float, '2007': float, '2008': float, '2009': float,
                      '2010': float, '2011': float, '2012': float, '2013': float, '2014': float,
                      '2015': float, '2016': float, '2017': float, '2018': float, '2019': float,
                      '2020': float}
EU_imports_filtered = EU_imports_filtered.astype(years_columns_type)
EU_imports_filtered.dtypes


# In[20]:


EU_imports_filtered


# ## Group by Country

# In[21]:


EU_imports_grouped = EU_imports_filtered
EU_imports_grouped


# In[22]:


# create new column 'Partner_EU?' and fill with True/False based on whether Partner_country is in EU
EU_imports_grouped['Partner_EU'] = EU_imports_grouped['partner'].isin(EU_countries['Alpha_2_code'])
EU_imports_grouped


# In[23]:


EU_imports_grouped['Partner_EU'].unique()


# In[24]:


EU_imports_grouped = EU_imports_grouped[['Country', 'Partner_EU', 'Partner_country', '1990', '1991', '1992', '1993',
                                         '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001',
                                         '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
                                         '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017',
                                         '2018', '2019', '2020']]
EU_imports_grouped


# In[25]:


EU_grouped = EU_imports_grouped.groupby(['Country', 'Partner_EU', 'Partner_country']).sum()

EU_grouped


# In[26]:


EU_grouped = EU_grouped[~(EU_grouped==0).all(axis=1)]
EU_grouped


# In[27]:


s = pd.concat([EU_grouped, EU_grouped.sum(level=[0,1]).assign(Country='Total').set_index('Country', append=True)]).sort_index(level=[0,1,2])
s


# In[28]:


s_subtotals = s.groupby(by=['Country', 'Partner_EU', 'Partner_country'], observed=False).sum()
s_subtotals


# In[29]:


#pd.set_option('max_rows', None)
#s_subtotals


# COMMIT

# In[30]:


pip install openpyxl


# In[31]:


Overall_Pivot_Percent = pd.read_excel('../raw_data/s_subtotals.xlsx', sheet_name='Overall_Pivot_Percent', header=0)
Overall_Pivot_Percent = Overall_Pivot_Percent.fillna('')
Overall_Pivot_Percent


# In[32]:


Overall_Pivot_Percent.columns


# In[33]:


years=['Total_1991', 'Total_1992',
       'Total_1993', 'Total_1994', 'Total_1995', 'Total_1996', 'Total_1997',
       'Total_1998', 'Total_1999', 'Total_2000', 'Total_2001', 'Total_2002',
       'Total_2003', 'Total_2004', 'Total_2005', 'Total_2006', 'Total_2007',
       'Total_2008', 'Total_2009', 'Total_2010', 'Total_2011', 'Total_2012',
       'Total_2013', 'Total_2014', 'Total_2015', 'Total_2016', 'Total_2017',
       'Total_2018', 'Total_2019', 'Total_2020', 'Total_Total_']

for year in years:
    Overall_Pivot_Percent[year]=pd.to_numeric(Overall_Pivot_Percent[year], errors='raise', downcast='float')
    
Overall_Pivot_Percent


# In[34]:


Overall_Percent_Country = Overall_Pivot_Percent[Overall_Pivot_Percent['EU_Partner'].str.contains('Total', case=False, na=False).any(level=0)]
#Overall_Percent_Country = Overall_Pivot_Percent[Overall_Pivot_Percent['Partner_EU'].str.contains('|'.join(col_values), case=False, na=False).any(level=0)]

Overall_Percent_Country


# In[35]:


col_values = ['TRUE', 'FALSE']
Overall_Percent_Country = Overall_Percent_Country[Overall_Percent_Country['Partner_EU'].str.contains('|'.join(col_values), case=False, na=False).any(level=0)]

Overall_Percent_Country


# In[36]:


Overall_true = Overall_Percent_Country[Overall_Percent_Country['Partner_EU']=='TRUE Total'].rename(columns={'Partner_EU': 'EU Member'})
Overall_true_2020 = Overall_true[['Country', 'Total_2020']]
Overall_false = Overall_Percent_Country[Overall_Percent_Country['Partner_EU']=='FALSE Total'].rename(columns={'Partner_EU': 'Non EU Member'})
Overall_false_2020 = Overall_false[['Country', 'Total_2020']]
Overall_true_2020


# In[37]:


Overall_true_2020['Total_2020_Percentage'] = (Overall_true_2020.Total_2020 * 100).astype(str)+'%'
Overall_true_2020 = Overall_true_2020.sort_values(by=['Total_2020'], ascending=False)
Overall_true_2020


# In[38]:


Overall_false_2020


# In[39]:


Overall_false_2020['Total_2020'] *= -1
Overall_false_2020['Total_2020_Percentage'] = (Overall_false_2020.Total_2020 * 100).astype(str)+'%'
Overall_false_2020=Overall_false_2020.sort_values(by=['Total_2020'], ascending=True)
Overall_false_2020


# In[40]:


from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default = "notebook"

fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_yaxes=True, horizontal_spacing=0)


# In[41]:


# plot for Non EU Member partners

fig.append_trace(go.Bar(x=Overall_false_2020.Total_2020, y=Overall_false_2020.Country,
                       orientation='h', showlegend=True,
                       text=Overall_false_2020.Total_2020_Percentage,
                       name='Non-EU Member Partner',
                       marker_color='red'), 1, 1)


# In[42]:


# plot for EU Member partners

fig.append_trace(go.Bar(x=Overall_true_2020.Total_2020, y=Overall_true_2020.Country,
                       orientation='h', showlegend=True,
                       text=Overall_true_2020.Total_2020_Percentage,
                       name='EU Member Partner',
                       marker_color='blue'), 1, 2)


# In[43]:


fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False, categoryorder='total ascending',
                ticksuffix=' ', showline=False)

fig.update_traces(hovertemplate=None)

fig.update_layout(title='Where do EU countries import electricity from: 2020',
                 margin=dict(t=80, b=0, l=70, r=40),
                 hovermode="y unified",
                 xaxis_title=' ', yaxis_title=" ",
                 plot_bgcolor='beige', paper_bgcolor='white')

fig.update_layout(autosize=False,
                 width=900,
                 height=800,)


# In[44]:


democracy = pd.read_csv('../raw_data/Democracy_Index.csv', encoding = 'unicode_escape')
democracy.dropna(inplace=True)
democracy.head()


# In[45]:


democracy['Regime type'].unique()


# In[46]:


democracy = democracy.drop(columns=['EU?'])
democracy = democracy.rename(columns={'Country': 'Partner_country', 'Regime type': 'Regime_type'})
democracy


# In[47]:


democracy['Partner_country'].replace({'Netherlands': 'Netherlands (the)', 
                              'North Macedonia': 'Republic of North Macedonia',
                              'Russia': 'Russian Federation (the)',
                              'Moldova': 'Moldova (the Republic of)'}, inplace=True)
democracy


# In[48]:


Partners_Pivot_Percent = pd.read_excel('../raw_data/s_subtotals.xlsx', sheet_name='Partners_Pivot_Percent', header=0)
Partners_Pivot_Percent = Partners_Pivot_Percent.fillna('')
Partners_Pivot_Percent


# In[49]:


Partners_Pivot_Percent['Partner_country'] = Partners_Pivot_Percent['Partner_country'].str.replace(' Total', '')

Partners_Pivot_Percent


# In[50]:


# merge Partners_Pivot_Percent with democracy
Partners_Pivot_Percent = Partners_Pivot_Percent.merge(democracy, on='Partner_country', how='left')

Partners_Pivot_Percent


# In[51]:


Partners_Pivot_Overall = Partners_Pivot_Percent[Partners_Pivot_Percent['Country']=='']
Partners_Pivot_Overall


# In[52]:


Partners_Non_EU = Partners_Pivot_Overall[Partners_Pivot_Overall['Partner_EU']=='FALSE']
Partners_Non_EU


# In[53]:


Partners_Non_EU.columns = Partners_Non_EU.columns.str.strip('Total_')
Partners_Non_EU.columns


# In[54]:


Partners_Non_EU = Partners_Non_EU[['Partner_country', 'Regime_type', '1990', '1991', '1992',
       '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001',
       '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010',
       '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019',
       '2020']]
Partners_Non_EU


# In[55]:


Partners_Non_EU_mod = Partners_Non_EU.melt(id_vars=['Partner_country', 'Regime_type'], 
                                           value_vars=['1990', '1991', '1992', '1993', '1994', '1995', 
                                                       '1996', '1997', '1998', '1999', '2000', '2001', 
                                                       '2002', '2003', '2004', '2005', '2006', '2007', 
                                                       '2008', '2009', '2010', '2011', '2012', '2013', 
                                                       '2014', '2015', '2016', '2017', '2018', '2019', 
                                                       '2020'])
Partners_Non_EU_mod


# In[56]:


Partners_Non_EU_mod = Partners_Non_EU_mod.rename(columns={'variable': 'Year', 'value': 'Percent_total_imports'})
Partners_Non_EU_mod


# In[57]:


Partners_Non_EU_mod['Overall_Percent_Imports'] = (Partners_Non_EU_mod.Percent_total_imports * 100).astype(str)+'%'
Partners_Non_EU_mod


# In[58]:


Partners_Non_EU_mod_grouped = Partners_Non_EU_mod.groupby(['Regime_type', 'Partner_country', 'Year']).first()
Partners_Non_EU_mod_grouped


# In[59]:


Partners_Non_EU_mod_type = Partners_Non_EU_mod[['Year', 'Regime_type', 'Partner_country', 'Percent_total_imports']]
Partners_Non_EU_mod_type


# In[60]:


Partners_NonEU_pivot = pd.pivot_table(Partners_Non_EU_mod_type, values = 'Percent_total_imports', index = ['Year', 'Regime_type']).reset_index()
Partners_NonEU_pivot


# In[61]:


Partners_NonEU_pivot['Overall_Imports'] = (Partners_NonEU_pivot.Percent_total_imports * 100).astype(str)+'%'
Partners_NonEU_pivot


# In[62]:


import plotly.express as px
fig = px.line(Partners_NonEU_pivot, x='Year', y='Percent_total_imports', color='Regime_type',
             title='Percentage of Overall Imports from Non-EU Partners')
fig.show()


# In[63]:


pip install matplotlib-venn


# In[64]:


#Import libraries
from matplotlib_venn import venn2, venn2_circles, venn2_unweighted
from matplotlib_venn import venn3, venn3_circles
from matplotlib import pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[65]:


Partners_Pivot_Overall


# In[66]:


Partners_Pivot = Partners_Pivot_Overall[~Partners_Pivot_Overall.Partner_EU.str.contains('Total')]
Partners_Pivot


# In[67]:


Partners_Pivot_Table = pd.pivot_table(Partners_Pivot, values='Total_2020', index=['Regime_type', 'Partner_EU', 'Partner_country']).reset_index()
Partners_Pivot_Table

