# Overview

This repository hosts all scripts and outputs that are relevant for my final project of the [PPOL 6801: Text as Data](https://tiagoventura.github.io/PPOL_6801_2024) course. For the final project, I use the [a-la-carte embedding approach](https://www.cambridge.org/core/journals/american-political-science-review/article/embedding-regression-models-for-contextspecific-description-and-inference/4C90013E5C714C8483ED95CC699022FB) to look at the overall trends in semantic polarization and identify issue framing strategies employed by Democratic and Republican senators from the 107<sup>th</sup>-114<sup>th</sup> Congress.

In this project, I corroborate the value of the ALC method in exploring semantic polarization trends and identifying issue framing strategies, emphasizing its role as a computationally cheap alternative to transformers-based methods in computing contextualized embeddings. 

The following sections in this README provide information on the overall structure of this repository, as well as the original source for the raw data.


# Structure

This repository has three main folders:

* `0_scripts`: this folder contains the scripts for building the raw data, training the model, and visualizing the analytical outputs. The script that builds the raw Congress text is a Python script that is mostly adapted from [Rheault and Cochrane (2020)'s script](https://github.com/lrheault/partyembed/tree/master/src) with some modifications to the number of sessions being parsed. Meanwhile, the training and analytical scripts are R scripts that rely heavily on the `conText` package that is proposed by [Rodriguez, Spirling and Stewart (2023)](https://www.cambridge.org/core/journals/american-political-science-review/article/embedding-regression-models-for-contextspecific-description-and-inference/4C90013E5C714C8483ED95CC699022FB). The scripts are separated based on their sequences in the analytical stages as well as their outputs, and the tasks implemented by each scripts are described as follows:

    - `1_1_build_congress_text.py`: Builds the raw U.S. corpus
    - `2_1_train_glove_matrix.R`: Trains local GloVE model and computes transformation matrix
    - `2_2_train_alc_embedding_analytics.R`: Computes ALC embedding and other analytical exercises
    - `2_3_visualize_alc_embeddings.R`: Visualizes the analytical output

* `3_docs`: this folder contains the figures output (in the figure subfolder). Additionally, this folder also contains the project proposal, presentation and report, all of which are stored in the `report` folder.


# Data 

All materials for the final project, including the raw data, are sourced from this [Harvard Dataverse repository](https://dataverse.harvard.edu/dataset.xhtml;jsessionid=ccbe4ad771f0ce57d8169462f553?persistentId=doi%3A10.7910%2FDVN%2FK0OYQF&version=&q=&fileTypeGroupFacet=%22Unknown%22&fileAccess=). We do not track the input and output data in this repository. Readers who wish to follow along can create the data folders in their own local machine.

# References

Rheault, L., & Cochrane, C. (2020). Word embeddings for the analysis of ideological placement in parliamentary corpora. _Political Analysis, 28_(1), 112-133.

Rodriguez PL, Spirling A., Stewart BM. Embedding Regression: Models for Context-Specific Description and Inference. _American Political Science Review_. 2023;117(4):1255-1274. doi:10.1017/S0003055422001228
