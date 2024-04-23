# Script to visualize Doc2Vec document embedding results
# Adapted from Rheault & Cochrane (2020)

#=========================================================================================#
# Preliminaries
#=========================================================================================#

# Load the required libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from gensim.models.doc2vec import Doc2Vec
import re


#=========================================================================================#
# Data load
#=========================================================================================#

# Load pre-trained model
model = Doc2Vec.load('2_build/senate')

#=========================================================================================#
# Build dataset
#=========================================================================================#

# Get the vectors and build as dataframe
dv_df = []
for i in range(0, len(model.dv.index_to_key)):
    dv_df.append(model.dv[i])
dv_df = pd.DataFrame(dv_df)

# Build keys dataframe
keys_df = pd.DataFrame({'keys': [el for el in model.dv.index_to_key]})

# Merge the two data 
docvec_df = keys_df.merge(
    dv_df, left_index=True, right_index=True
)


#=========================================================================================#
# Fit PCA
#=========================================================================================#

# Loop across policy topics, fit-transform PCA model, and append in a single dataframe.
topics = ['immigration', 'abortion', 'guns', 'climate', 'tax', 'race']

pca_df = []
for t in topics:

    # Initiate PCA model
    pca = PCA(n_components=2)

    # Subset rows to policy-specific features
    pattern = r'[DR]_(10[8-9]|11[0-4])_{}'.format(t)
    topic_df = docvec_df[docvec_df['keys'].str.contains(pattern)]

    # Fit the PCA model
    Z = pd.DataFrame(
        pca.fit_transform(topic_df.drop(columns = 'keys', axis = 1)), 
        columns = ['dim1', 'dim2']
    )
    Z = Z.merge( 
        topic_df['keys'].reset_index(drop = True),
        left_index=True,
        right_index=True
    )

    # Clean up feature names
    Z['party'] = Z['keys'].str.extract(r'([DR])')
    Z['session'] = Z['keys'].str.extract(r'(10[8-9]|11[0-4])')
    Z['policy'] = Z['keys'].str.extract(r'_([a-zA-Z]+)$')
    Z = Z.drop(columns = 'keys', axis = 1)
    pca_df.append(Z)

# Convert to dataframe 
pca_df = pd.concat(pca_df)

#=========================================================================================#
# Visualize PCA components
#=========================================================================================#

# Instead of session, use years.
conditions = [
    pca_df['session'] == "108", 
    pca_df['session'] == "109", 
    pca_df['session'] == "110", 
    pca_df['session'] == "111", 
    pca_df['session'] == "112", 
    pca_df['session'] == "113",
    pca_df['session'] == "114" 
]
choices = [ 
    "2003-2005", 
    "2005-2007", 
    "2007-2009", 
    "2009-2011", 
    "2011-2013", 
    "2013-2015", 
    "2015-2017"
]
pca_df['year'] = np.select(conditions, choices)

# Initiate subplots
fig, axs = plt.subplots(2, 3, figsize = (15, 15))

# Plot
for i, t in enumerate(topics):
    
    # Visualize immigration policy
    plot_data = pca_df[pca_df['policy'] == t].copy()

    # Group by party
    party_grouping = plot_data.groupby('party')

    # Plot in the defined subplot 
    ax = axs[i // 3, i % 3]

    for party, group in party_grouping:
        color = 'tomato' if party == "R" else "steelblue"
        ax.plot(group['year'], group['dim1'], marker = 'o', linestyle = '-', label = party, color = color)

    # Add horizontal line at y=0
    ax.axhline(y = 0, color = "black", linestyle = "--", linewidth = 1)

    # Set labels and titles for subplot
    ax.set_xlabel('Year')
    ax.set_ylabel('First PC component value')
    ax.set_title('{}'.format(t))
    ax.legend()

    # Set axis params 
    ax.tick_params(axis = 'x', rotation=45)
    ax.tick_params(axis = 'x', labelsize = 8)

# Display the plot
plt.tight_layout()
plt.subplots_adjust(hspace = .5, wspace=.5)
plt.savefig('3_docs/figure/doc2vec_senate.pdf')