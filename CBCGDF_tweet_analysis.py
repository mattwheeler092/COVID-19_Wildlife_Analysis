import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import numpy as np
import os

def check_keywords(text,keywords):
    # Function to check if any keyword in the input
    # 'keywords' list is present in the input 'text' str
    for word in keywords:
        if word in text.lower():
            return True
    return False

# Load the tweet data
tweets = pd.read_excel('CBCGDF_China_tweet_history.xlsx')

# Define the different groups and corresponding key words
wildlife_keywords = ['wildlife','wet market','wet markets']
pangolin_keywords = ['pangolin','pangolins']
covid_keywords = ['covid-19','covid19','covid','coronavirus']

# Create boolean columns to check if keywords are in the tweets
tweets['wildlife_bool'] = tweets['full_text'].apply(lambda x: check_keywords(x,wildlife_keywords))
tweets['pangolin_bool'] = tweets['full_text'].apply(lambda x: check_keywords(x,pangolin_keywords))
tweets['covid_bool'] = tweets['full_text'].apply(lambda x: check_keywords(x,covid_keywords))

# Fix the tweet dates to be datetime objects
tweets['group_date'] = tweets['created_at'].apply(lambda x: dt.datetime.strftime(x,'%b-%y'))
tweets['order_field'] = tweets['created_at'].apply(lambda x: dt.datetime.strftime(x,'%Y-%m'))

# Group the dataframe by the date to the total tweet numbers
tweets['count'] = 1
grouped_tweets = tweets.groupby(['group_date','order_field'], sort=False).sum().reset_index()
grouped_tweets.sort_values(by='order_field',inplace=True)

# Compute the percentage of total tweets value for the different keyword groups
for col in grouped_tweets.columns:
    if 'bool' in col:
        new_col = col.split('_')[0] + "_perc"
        grouped_tweets[new_col] = grouped_tweets[col]/grouped_tweets['count']

# Create a list all of the month-year values
years = [17,18,19,20]
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
dates = pd.DataFrame([m + '-' + str(y) for y in years for m in months][3:],columns=['group_date'])

# Left merge these dates with the grouped tweet df to add rows for all months
plot_data = dates.merge(grouped_tweets, how='left', on='group_date')
plot_data['scaled_count_2'] = 96 * plot_data['count'] / 313
plot_data['scaled_count_2'] = 0.9 * plot_data['count'] / 313
plot_data.fillna(value=0,inplace=True)


# --------------------------------------------------  Plot total tweets ---------------------------------------------------------
sns.set_style("white")

fig, ax = plt.subplots(figsize=(8.78,6.2))
ax2 = ax.twinx()

sns.lineplot(ax=ax, data=plot_data, x="group_date", y="scaled_count_1", color='lightgrey', label='Total tweets from @CBCGDF_China')
sns.lineplot(ax=ax2, data=plot_data, x="group_date", y="count", color='lightgrey')

sns.lineplot(ax=ax, data=plot_data, x="group_date", y="pangolin_bool", color='#F6D55C', label='Pangolin related tweets')
sns.lineplot(ax=ax, data=plot_data, x="group_date", y="covid_bool", color='#ED553B', label='COVID-19 related tweets')
sns.lineplot(ax=ax, data=plot_data, x="group_date", y="wildlife_bool", color='#3CAEA3', label='Wildlife related tweets')

num_points = len(plot_data['group_date'].values)
ticks = [num_points - (val + 1) for val in range(0,num_points,3)]
ticks.reverse()

ax.set_ylabel("Number of related tweets",fontsize=14)
ax2.set_ylabel("Number of total @CBCGDF_China tweets", fontsize=14)
ax.set_xlabel(" ",fontsize=14)

ax.lines[0].set_linestyle("--")
ax2.lines[0].set_linestyle("--")

ax.set_xticks(ticks)
ax.set_xticklabels(plot_data['group_date'].values[ticks],fontsize=12,rotation=45)
ax.set_yticks(list(range(0,101,20)))
ax.set_yticklabels(list(range(0,101,20)),fontsize=12)
ax2.set_yticks(list(range(0,301,50)))
ax2.set_yticklabels(list(range(0,301,50)),fontsize=12)

ax.legend(fontsize=12)
fig.tight_layout()

plt.savefig('CBCGDF_tweet_totals_plot.png', format='png')



# --------------------------------------------------  Plot percentage tweets ---------------------------------------------------------

perc_plot_data = plot_data[-15:]

sns.set_style("white")

fig, ax = plt.subplots(figsize=(8.78,6.2))
ax2 = ax.twinx()

sns.lineplot(ax=ax, data=perc_plot_data, x="group_date", y="scaled_count_2", color='lightgrey', label='Total number of @CBCGDF_China tweets')
sns.lineplot(ax=ax2, data=perc_plot_data, x="group_date", y="count", color='lightgrey')

sns.lineplot(ax=ax, data=perc_plot_data, x="group_date", y="pangolin_perc", color='#F6D55C', label='% of tweets related to Pangolins')
sns.lineplot(ax=ax, data=perc_plot_data, x="group_date", y="covid_perc", color='#ED553B', label='% of tweets related to COVID-19')
sns.lineplot(ax=ax, data=perc_plot_data, x="group_date", y="wildlife_perc", color='#3CAEA3', label='% of tweets related to Wildlife')

num_points = len(perc_plot_data['group_date'].values)
ticks = [num_points - (val + 1) for val in range(0,num_points,1)]
ticks.reverse()

ax.set_ylabel("Percentage of total @CBCGDF_China tweets",fontsize=14)
ax2.set_ylabel("Total number of @CBCGDF_China tweets", fontsize=14)
ax.set_xlabel(" ",fontsize=14)

ax.lines[0].set_linestyle("--")
ax2.lines[0].set_linestyle("--")

ax.set_xticks(ticks)
ax.set_xticklabels(perc_plot_data['group_date'].values[ticks],fontsize=12,rotation=45)
ax.set_yticks(np.array(range(0,101,20))/100)
ax.set_yticklabels([ f'{str(val)}%' for val in range(0,101,20)],fontsize=12)
ax.set_ylim(0,1)
ax2.set_yticks(list(range(0,301,50)))
ax2.set_yticklabels(list(range(0,301,50)),fontsize=12)
ax2.set_ylim(0,348)

ax.legend(fontsize=12)
fig.tight_layout()

plt.savefig('CBCGDF_tweet_percentage_plot.png', format='png')