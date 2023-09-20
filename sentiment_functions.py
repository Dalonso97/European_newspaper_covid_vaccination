import pandas as pd
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

matplotlib.rc('font', **font)
params = {'axes.labelsize': 22,
          'axes.titlesize': 22}
plt.rcParams.update(params)
def date_headlines(subset):
    neg_titles=subset[subset['sentiment_title']==0]
    pos_titles=subset[subset['sentiment_title']==2]
    df_overtime=neg_titles.copy()

    # df_overtime.dropna(inplace=True)
    df_overtime['date'] = pd.to_datetime(df_overtime['Date'])
    # Set date column as index 
    df_overtime = df_overtime.set_index('date')
    # Count the number of articles by month
    df_monthly_n = df_overtime.resample('M').size()

    df_overtime=pos_titles.copy()

    # df_overtime.dropna(inplace=True)
    df_overtime['date'] = pd.to_datetime(df_overtime['Date'])
    # Set date column as index 
    df_overtime = df_overtime.set_index('date')
    # Count the number of articles by month
    df_monthly_p = df_overtime.resample('M').size()
    # Create figure and plot space
    fig, ax = plt.subplots(figsize=(10, 10))

    # Add x-axis and y-axis
    ax.scatter(df_monthly_n.index.values,
               df_monthly_n.values, label='negative headlines')
    ax.scatter(df_monthly_p.index.values,
               df_monthly_p.values, label='positive headlines')
    ax.legend()
    # Set title and labels for axes
    ax.set(xlabel="Date",
           ylabel="Number of articles",
           title="Number of articles by month")

    plt.show()

def positive_negative_distribution(df,date_start_vaccination):
    df_overtime=df.copy()

    # df_overtime.dropna(inplace=True)
    df_overtime['date'] = pd.to_datetime(df_overtime['Date'])
    # Set date column as index 
    df_overtime = df_overtime.set_index('date')
    # Mean of porcentage of sentences positive/negative by month
    df_monthly_n = df_overtime.resample('M')['porcentage_negative'].mean()
    df_weekly_n = df_overtime.resample('W')['porcentage_negative'].mean()
    df_monthly_p = df_overtime.resample('M')['porcentage_positive'].mean()
    df_weekly_p = df_overtime.resample('W')['porcentage_positive'].mean()
    #Fill /monthsweeks without articles with 0
    df_monthly_p = df_monthly_p.replace(np.nan, 0)
    df_monthly_n = df_monthly_n.replace(np.nan, 0)
    df_weekly_p = df_weekly_p.replace(np.nan, 0)
    df_weekly_n = df_weekly_n.replace(np.nan, 0)
    fig, ax = plt.subplots(2,figsize=(20, 20))
    plt.rcParams['font.size'] = '16'

    #Points in the fig
    ax[0].scatter(df_monthly_n.index.values,
               df_monthly_n.values, label='% negative sentences')
    #Line connecting points in the fig
    ax[0].plot(df_monthly_n.index.values,
               df_monthly_n.values)
    ax[0].scatter(df_monthly_p.index.values,
               df_monthly_p.values, label='% positive sentences')
    ax[0].plot(df_monthly_p.index.values,
               df_monthly_p.values)
    ax[0].legend()
    # Set title and labels for axes
    ax[0].set(xlabel="Month",
           ylabel="% sentences positive-negative",
           title="Average percentage of positive/negative sentences per month")
    ax[0].axvline( pd.to_datetime(date_start_vaccination), ls=":")
    ax[1].scatter(df_weekly_n.index.values,
               df_weekly_n.values, label='% negative sentences')
    ax[1].plot(df_weekly_n.index.values,
               df_weekly_n.values)
    ax[1].scatter(df_weekly_p.index.values,
               df_weekly_p.values,label='% positive sentences')
    ax[1].plot(df_weekly_p.index.values,
               df_weekly_p.values)
    ax[1].legend()
    # Set title and labels for axes
    ax[1].set(xlabel="Week",
           ylabel="% sentences positive-negative",
           title="Average percentage of positive/negative sentences per week")
    ax[1].axvline(pd.to_datetime(date_start_vaccination), ls=":")

 
    plt.show()

    
def frequency_topics(df, df_sub): 
    df_overtime_total=df.copy()
    # df_overtime_total.dropna(inplace=True)
    df_overtime_total['date'] = pd.to_datetime(df_overtime_total['Date'])
    # Set date column as index 
    df_overtime_total = df_overtime_total.set_index('date')
    # Number  of total articles by month and by week
    df_monthly_total_samples = df_overtime_total.resample('M')['Link'].count()
    df_weekly_total_samples = df_overtime_total.resample('W')['Link'].count()

    #Fill /monthsweeks without articles with 0
    df_monthly_total_samples = df_monthly_total_samples.replace(np.nan, 0)
    df_weekly_total_samples = df_weekly_total_samples.replace(np.nan, 0)


    df_overtime_subtopic=df_sub.copy()

    df_overtime_subtopic['date'] = pd.to_datetime(df_overtime_subtopic['Date'])
    # Set date column as index 
    df_overtime_subtopic = df_overtime_subtopic.set_index('date')
    # Number  of total articles by month and by week
    df_monthly_subtopic_samples = df_overtime_subtopic.resample('M')['Link'].count()
    df_weekly_subtopic_samples = df_overtime_subtopic.resample('W')['Link'].count()

    #Fill /monthsweeks without articles with 0
    df_monthly_subtopic_samples = df_monthly_subtopic_samples.replace(np.nan, 0)
    df_weekly_subtopic_samples = df_weekly_subtopic_samples.replace(np.nan, 0)
    #Create dataframes with subtopic and full data to calculate the frequency of subtopic
    df_monthly_total_samples=pd.DataFrame(df_monthly_total_samples)
    df_monthly_subtopic_samples=pd.DataFrame(df_monthly_subtopic_samples)

    df_weekly_total_samples=pd.DataFrame(df_weekly_total_samples)
    df_weekly_subtopic_samples=pd.DataFrame(df_weekly_subtopic_samples)

    #MErge data 
    merged_data_monthly = pd.merge(df_monthly_total_samples,df_monthly_subtopic_samples, how='outer', on='date')
    merged_data_monthly  = merged_data_monthly.replace(np.nan, 0)

    merged_data_weekly = pd.merge(df_weekly_total_samples,df_weekly_subtopic_samples, how='outer', on='date')
    merged_data_weekly  = merged_data_weekly.replace(np.nan, 0)

    frequency_month=merged_data_monthly.Link_y.values/merged_data_monthly.Link_x.values
    frequency_week=merged_data_weekly.Link_y.values/merged_data_weekly.Link_x.values



    fig, ax = plt.subplots(2,figsize=(20, 20))

    #Points in the fig
    ax[0].scatter(merged_data_monthly.index.values,
               frequency_month)
    #Line connecting points in the fig
    ax[0].plot(merged_data_monthly.index.values,
               frequency_month)
    # Set title and labels for axes
    ax[0].set(xlabel="Month",
           ylabel="Frequency of topic",
           title="sub-theme frequency per month")
    #Points in the fig
    ax[1].scatter(merged_data_weekly.index.values,
               frequency_week)
    #Line connecting points in the fig
    ax[1].plot(merged_data_weekly.index.values,
               frequency_week)
    # Set title and labels for axes
    ax[1].set(xlabel="Week",
           ylabel="Frequency of topic",
           title="sub-theme frequency per week")

    plt.show()    
    
    
def sentiment_analysis(subset, date_start_vaccination):
    #POSITIVE HEADLINES
    print('\033[1m' +"SAMPLES OF POSITIVE HEADLINES")
    try:
        for i in subset[subset['sentiment_title']=="Positive"].sample(3).Title_en: 
            print('\033[0m' + i)
    except: 
        try:
            for i in subset[subset['sentiment_title']=="Positive"].sample(2).Title_en: 
                print('\033[0m' + i)
        except:
            print("No samples of positive headlines")
    #NEGATIVE HEADLINES
    print('\033[1m' +"SAMPLES OF NEGATIVE HEADLINES")
    try:
        for i in subset[subset['sentiment_title']=="Negative"].sample(3).Title_en: 
            print('\033[0m' + i)
    except: 
        try: 
            for i in subset[subset['sentiment_title']=="Negative"].sample(2).Title_en: 
                print('\033[0m' + i)
        except:
            print("No samples of negative headlines")
            
        
    #date_headlines(subset)
    df_mean_pos = subset['porcentage_positive'].mean()
    df_mean_neg = subset['porcentage_negative'].mean()
    df_mean_neu = subset['porcentage_neutral'].mean()
    labels = 'Mean negative sentences', 'Mean positive sentences', 'Mean neautral sentences'
    sizes = [df_mean_neg,df_mean_pos,df_mean_neu]
    
    df_headlines_pos = len(subset[subset['sentiment_title']=="Positive"])/len(subset)
    df_headlines_neg = len(subset[subset['sentiment_title']=="Negative"])/len(subset)
    df_headlines_neu = len(subset[subset['sentiment_title']=="Neutral"])/len(subset)
    labels_headlines = 'negative headlines', 'Positive headlines', 'Neautral headlines'
    sizes_headlines = [df_headlines_neg,df_headlines_pos,df_headlines_neu]
    # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots(1,2,figsize=(15, 5))
    ax1[0].pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1[0].set(title="distribution of sentence sentiment")
    
    ax1[1].pie(sizes_headlines, labels=labels_headlines, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1[1].axis('equal')
    ax1[1].set(title="distribution of headline sentiment")
    plt.show()
    
    positive_negative_distribution(subset,date_start_vaccination)
    
def sentences_with_word(df,word):
    list_sentences=[]
    list_labels=[]
    for index,row in df.iterrows(): 
        for sentence in df['list_sentences'][index]:
            list_sentences.append(sentence)
        for label in df['list_labels'][index]: 
            list_labels.append(label)
    df_sentences=pd.DataFrame()
    df_sentences['sentence']=list_sentences
    df_sentences['label']=list_labels
    df_sentences=df_sentences[df_sentences['sentence'].str.contains(word)]
    #eliminate neutral sentences
#     df_sentences=df_sentences.drop(df_sentences[df_sentences['label']==1].index, inplace=False)
    print('\033[1m' +"SAMPLES OF POSITIVE SENTENCES")
    try:
        for i in df_sentences[df_sentences['label']==2].sample(2).sentence: 
            print('\033[0m' + i)
    except:
        print("No samples of positive sentences")
    #NEGATIVE HEADLINES
    print('\033[1m' +"SAMPLES OF NEGATIVE SENTENCES")
    try:
        for i in df_sentences[df_sentences['label']==0].sample(2).sentence:
            print('\033[0m' + i)
    except: 
        print("No samples of negative headlines")
    df_pos_sentences = len(df_sentences[df_sentences['label']==2])/len(df_sentences)
    df_neg_sentences = len(df_sentences[df_sentences['label']==0])/len(df_sentences)
    df_neu_sentences = len(df_sentences[df_sentences['label']==1])/len(df_sentences)

    labels_sentences = 'Negative sentences', 'Positive sentences', 'Neautral sentences'
    sizes_sentences = [df_neg_sentences,df_pos_sentences,df_neu_sentences]  
    fig1, ax1 = plt.subplots(figsize=(15, 5))
    ax1.pie(sizes_sentences, labels=labels_sentences, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set(title="distribution of specific sentence sentiment")
    plt.show()
