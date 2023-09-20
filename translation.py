import deepl
import pandas as pd

df = pd.read_csv('/idiap/temp/ddbarrio/VACCINATION_PROJECT/DATAFRAMES/articles_liberation_10_11_2021_premium.csv')

translator = deepl.Translator('')

list_articles_liberation_english=[]

for index, row in df.iterrows():
    try:
        title= translator.translate_text(df.Title[index],target_lang="EN-GB").text
    except:
        title="error"
    try:
        subheadline= translator.translate_text(df.Subheadline[index],target_lang="EN-GB").text
    except:
        subheadline="error"
    try:
        text= translator.translate_text(df.Text[index],target_lang="EN-GB").text
    except:
        text="error"
    author=df.Authors[index]
    date=df.Date[index]
    link=df.Link[index]

    list_articles_liberation_english.append({'Title': title,
                          'Subheadline':subheadline,
                          'Text':text,
                          'Authors': author,
                          'Date': date,
                          'Link':link})


articles_liberation_english = pd.DataFrame.from_dict(list_articles_liberation_english)

articles_liberation_english.to_csv(r'/idiap/temp/ddbarrio/VACCINATION_PROJECT/DATAFRAMES/articles_liberation_english.csv', index = False)

