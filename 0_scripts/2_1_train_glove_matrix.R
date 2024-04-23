# Script to train GloVe embedding on CR corpus.

# ------------------------------------------------------------
# Preliminary ----
# ------------------------------------------------------------

# Load the required libraries
library(dplyr)
library(data.table)
library(quanteda)
library(text2vec)
library(conText)
library(here)
library(fst)

# ------------------------------------------------------------
# Data load ----
# ------------------------------------------------------------

# Load the preprocessed txt data
congressional_records <- fread(
    here('2_build', 'congress.txt'), 
    quote = "",
    data.table = TRUE
)

# ------------------------------------------------------------
# Wrangle the CR data ----
# ------------------------------------------------------------

# Assign names to the parsed data
congressional_records <- congressional_records %>% 
    setnames(
        old = c("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10"),
        new = c( 
            "session", "speech_id", "raw_speech", "speaker_id", "speaker_name", 
            "chamber", "state", "party", "majority", "president"
        )
    )

# ------------------------------------------------------------
# Corpus creation and tokenization ----
# ------------------------------------------------------------

# Corpus conversion
cr_corpus <- corpus(
    congressional_records, text_field = "raw_speech"
)

# Largely adapting pre-processing recommended by https://cran.r-project.org/web/packages/conText/vignettes/quickstart.html .
# There are several pre-processing steps that I implement here:
# - Remove punctuations, symbols, numbers, separators
# - Remove English stopwords
# - Select only tokens with 3 or more characters
# - Consider only features that appear at least 5 times in the corpus.
# - As recommended by Spirling, set padding = TRUE to avoid making non-adjacent words adjacent prior to embedding computations
toks <- tokens(
    cr_corpus, 
    remove_punct = TRUE, 
    remove_symbols = TRUE, 
    remove_numbers = TRUE, 
    remove_separators = TRUE
) %>% 
    tokens_select(
        pattern = stopwords("en"),
        selection = "remove", 
        min_nchar = 3
    )

# Get features
features <- dfm( 
    toks, 
    tolower = TRUE,
    verbose = FALSE
) %>% 
    dfm_trim( 
        min_termfreq = 5
    ) %>% 
    featnames()

# Implement padding to avoid forced adjacency
toks_feats <- tokens_select( 
    toks, 
    features, 
    padding = TRUE
)

# ------------------------------------------------------------
# Estimate glove embeddings ----
# ------------------------------------------------------------

# Construct FCM 
toks_fcm <- fcm( 
    toks_feats, context = "window", window = 6, count = "frequency", tri = FALSE
)

# Estimate embedding 
glove <- GlobalVectors$new(
    rank = 300, 
    x_max = 10, 
    learning_rate = 0.05
)

main_wv <- glove$fit_transform(
    toks_fcm, n_iter = 10, 
    convergence_tol = 1e-3, 
    n_threads = parallel::detectCores()
)
context_wv  <- glove$components
local_glove <- main_wv + t(context_wv)

# Export the results locally
save(local_glove, file = here('2_build/local_glove.RData'))

# ------------------------------------------------------------
# Estimate the transformation matrix ----
# ------------------------------------------------------------

local_tf_matrix <- compute_transform(
    x = toks_fcm, 
    pre_trained = local_glove, 
    weighting = 500
)

# Export the results locally
save(local_tf_matrix, file = here('2_build/local_tf_matrix.RData'))