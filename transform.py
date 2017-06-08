import pandas as pd

df = pd.read_csv('linked_movies.csv')
df = df.fillna('')
fa  = ['oscar', 'bafta film award', 'golden globe', 'primetime emmy', 'grammy']
awards = df['Movie-Awards@imdb']
famous_awards = []
other_awards = []

for award in awards:
    try:

        tokens = award.split(',')
        faw = []
        othaw = []
        for token in tokens:
            if token.lower() in fa:
                faw.append(token)
            else:
                othaw.append(token)
        famous_awards.append(','.join(faw))
        other_awards.append(','.join(othaw))
    except Exception as e:
        print 'Error in transforming', e

df['Famous-Awards@imdb'] = famous_awards
df['Other-Awards@imdb'] = other_awards
del df['Movie-Awards@imdb']
df.to_csv('tranformed.csv', index = False)
