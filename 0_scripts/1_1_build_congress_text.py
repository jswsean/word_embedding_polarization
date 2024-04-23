# Script to build Congress compiled text from Gentzkow et al. Congressional Records.
# Adapted from Rheault & Cochrane (2020)
# Output format:
# 0: Congress
# 1: Speech ID
# 2: Raw text
# 3: Speaker ID
# 4: Speaker Name
# 5: Chamber (House/Senate)
# 6: State
# 7: Party
# 8: Majority Party (0/1)
# 9: Presidential Party (0/1)

import pandas as pd
import numpy as np
import pathlib

# Set path to folder that contains the text data working directory
text_data_dir = pathlib.Path("C:/Users/Sean Hambali/Desktop/DATA")
proj_dir = pathlib.Path.cwd()

# Adjust the paths.
locbound = text_data_dir / 'hein-bound'
locdaily = text_data_dir / 'hein-daily'
output_file = proj_dir / '2_build' / 'congress.txt'

# majority party and presidential party dictionaries
housemap = {81 : 'D', 82 : 'D', 83 : 'R', 84 : 'D',
            85 : 'D', 86 : 'D', 87 : 'D', 88 : 'D', 89 : 'D', 90 : 'D',
            91 : 'D', 92 : 'D', 93 : 'D', 94 : 'D', 95 : 'D', 96 : 'D',
            97 : 'D', 98 : 'D', 99 : 'D', 100 : 'D', 101 : 'D', 102 : 'D',
            103 : 'D', 104 : 'R', 105 : 'R', 106 : 'R', 107 : 'R', 108 : 'R',
            109 : 'R', 110 : 'D', 111 : 'D', 112 : 'R', 113 : 'R', 114 : 'R', 115 : 'R'}
senatemap ={81 : 'D', 82 : 'D', 83 : 'R', 84 : 'D',
            85 : 'D', 86 : 'D', 87 : 'D', 88 : 'D', 89 : 'D', 90 : 'D',
            91 : 'D', 92 : 'D', 93 : 'D', 94 : 'D', 95 : 'D', 96 : 'D',
            97 : 'R', 98 : 'R', 99 : 'R', 100 : 'D', 101 : 'D', 102 : 'D',
            103 : 'D', 104 : 'R', 105 : 'R', 106 : 'R', 107 : 'R', 108 : 'R',
            109 : 'R', 110 : 'R', 111 : 'D', 112 : 'D', 113 : 'D', 114 : 'R', 115 : 'R'}
presidentmap = {81 : 'D', 82 : 'D', 83 : 'R', 84 : 'R',
                85 : 'R', 86 : 'R', 87 : 'D', 88 : 'D', 89 : 'D', 90 : 'D',
                91 : 'R', 92 : 'R', 93 : 'R', 94 : 'R', 95 : 'D', 96 : 'D',
                97 : 'R', 98 : 'R', 99 : 'R', 100 : 'R', 101 : 'R', 102 : 'R',
                103 : 'D', 104 : 'D', 105 : 'D', 106 : 'D', 107 : 'R', 108 : 'R',
                109 : 'R', 110 : 'R', 111 : 'D', 112 : 'D', 113 : 'D', 114 : 'D', 115 : 'R'}

if __name__=="__main__":

    with open(output_file, 'w', encoding='utf-8') as out_:
        for i in range(107,112):
            house_majority = housemap[i]
            senate_majority = senatemap[i]
            president = presidentmap[i]

            record_name = 'speeches_%03d.txt' % i
            meta_name = '%03d_SpeakerMap.txt' % i

            # Collecting speech file (bound edition).
            speeches=[]
            with open(locbound/record_name, encoding='latin_1') as f:
                for line in f:
                    ls = line.split('|')
                    text = ls[1].encode('utf-8').decode('latin-1')
                    text = text.replace('\t',' ').replace('\n',' ').replace('\r',' ')
                    speeches.append((str(ls[0]), text))
            df = pd.DataFrame(speeches)
            df.columns = ['speech_id','speech']

            # Collecting meta data.
            metadf = pd.read_table(locbound/meta_name, sep="|", header=0, encoding='utf-8', dtype=object)
            metadf = metadf[metadf.nonvoting=='voting']
            metadf['namec'] = metadf.firstname + '_' + metadf.lastname
            metadf['majority'] = ''
            metadf.loc[(metadf.chamber=='H') & (metadf.party==house_majority),'majority'] = '1'
            metadf.loc[(metadf.chamber=='H') & (metadf.party!=house_majority),'majority'] = '0'
            metadf.loc[(metadf.chamber=='S') & (metadf.party==senate_majority),'majority'] = '1'
            metadf.loc[(metadf.chamber=='S') & (metadf.party!=senate_majority),'majority'] = '0'
            metadf['president'] = np.where(metadf.party==president,'1','0')
            metadf = metadf[['speakerid','speech_id','namec','chamber','state','party','majority','president']]
            df = df.merge(metadf, on='speech_id', how='right')
            df = df[pd.notnull(df.speech)]
            df = df[df.party.isin(['D','R'])]


            # Saving as tab-separated values.
            for idx, row in df.iterrows():
                out_.write(
                    str(i) + '\t' +
                    str(row.speech_id) + '\t' +
                    row.speech + '\t' +
                    str(row.speakerid) + '\t' +
                    str(row.namec) + '\t' +
                    str(row.chamber) + '\t' +
                    str(row.state) + '\t' +
                    str(row.party) + '\t' +
                    str(row.majority) + '\t' +
                    str(row.president) + '\n'
                )
            print("Completed Congress %d" %i)

        for i in range(112,115):

            house_majority = housemap[i]
            senate_majority = senatemap[i]
            president = presidentmap[i]

            record_name = 'speeches_%03d.txt' % i
            meta_name = '%03d_SpeakerMap.txt' % i

            # Collecting speech file (daily edition).
            speeches=[]
            with open(locdaily/record_name, encoding='latin_1') as f:
                for line in f:
                    ls = line.split('|')
                    text = ls[1].encode('utf-8').decode('latin-1')
                    text = text.replace('\t',' ').replace('\n',' ').replace('\r',' ')
                    speeches.append((str(ls[0]), text))
            df = pd.DataFrame(speeches)
            df.columns = ['speech_id','speech']

            # Collecting metadata.
            metadf = pd.read_table(locdaily/meta_name, sep="|", header=0, encoding='utf-8',dtype=object)
            metadf = metadf[metadf.nonvoting=='voting']
            metadf['namec'] = metadf.firstname + '_' + metadf.lastname
            metadf['majority'] = ''
            metadf.loc[(metadf.chamber=='H') & (metadf.party==house_majority),'majority'] = '1'
            metadf.loc[(metadf.chamber=='H') & (metadf.party!=house_majority),'majority'] = '0'
            metadf.loc[(metadf.chamber=='S') & (metadf.party==senate_majority),'majority'] = '1'
            metadf.loc[(metadf.chamber=='S') & (metadf.party!=senate_majority),'majority'] = '0'
            metadf['president'] = np.where(metadf.party==president,'1','0')
            metadf = metadf[['speakerid','speech_id','namec','chamber','state','party','majority','president']]
            df = df.merge(metadf, on='speech_id', how='right')
            df = df[pd.notnull(df.speech)]
            df = df[df.party.isin(['D','R'])]

            # Saving as tab-separated values.
            for idx, row in df.iterrows():
                out_.write(
                    str(i) + '\t' +
                    str(row.speech_id) + '\t' +
                    row.speech + '\t' +
                    str(row.speakerid) + '\t' +
                    str(row.namec) + '\t' +
                    str(row.chamber) + '\t' +
                    str(row.state) + '\t' +
                    str(row.party) + '\t' +
                    str(row.majority) + '\t' +
                    str(row.president) + '\n'
                )
            print("Completed Congress %d" %i)