# Script to compute ALC embeddings and export the results


# ------------------------------------------------------------
# Preliminaries ----
# ------------------------------------------------------------

# Load the required libraries
library(dplyr)
library(data.table)
library(quanteda)
library(text2vec)
library(conText)
library(hunspell)
library(here)

# ------------------------------------------------------------
# Data load ----
# ------------------------------------------------------------

# Load local_glove object
load(here('2_build/local_glove.RData'))

# Load tokenized corpus
load(here('2_build/toks_feats.RData'))

# Load feature vectors
load(here('2_build/features_vector.rds'))

# Load transformation matrix
load(here('2_build/local_tf_matrix.RData'))


# ------------------------------------------------------------
# Pre-processing ----
# ------------------------------------------------------------

# Convert session as character variable
docvars(toks_feats, "session") <- as.character(docvars(toks_feats)[['session']])

# Assign concatenation between party and session
docvars(toks_feats, "party_session") <- paste0(docvars(toks_feats)[['party']], "_", docvars(toks_feats)[['session']])

# Look at the output
head(docvars(toks_feats), 10)


# ------------------------------------------------------------
# Build ALC analytical infrastructure ----
# ------------------------------------------------------------

# Identify group-wise nearest neighbors for target term
get_nn_by_group <- function(token, seed_value) {
  
  # Set seed
  set.seed(seed_value)
  
  print("Identifying groupwise nearest neighbors.")
  
  # Get features
  feats <- featnames(dfm(token))
  
  # Get nearest neighbors of target terms and their corresponding CIs, by groups
  target_group_nns <- get_nns(
    x = token,
    N = 30,
    groups = docvars(token, 'party'),
    candidates = feats,
    pre_trained = local_glove,
    transform = TRUE,
    transform_matrix = local_tf_matrix,
    bootstrap = TRUE,
    num_bootstraps = 100,
    confidence_level = 0.95,
    as_list = TRUE
  )
  
  print("Group-wise nearest neighbors identified.")
  
  # Return output
  return(target_group_nns)
}


# Compute cosine similarity along pre-defined features
calculate_group_cos_sim <- function(token, seed_value, cos_sim_features) {
  
  # Set seed
  set.seed(seed_value)
  
  print("Computing cosine similarity.")
  
  # Compute cosine similarity
  target_cos_sim_df <- get_cos_sim(
    x = token,
    groups = docvars(token, 'party'),
    features = cos_sim_features,
    pre_trained = local_glove,
    transform = TRUE,
    transform_matrix = local_tf_matrix,
    bootstrap = TRUE,
    num_bootstraps = 100,
    as_list = FALSE
  )
  print("Cosine similarity identified.")
  
  # Return output
  return(target_cos_sim_df)
}


# Compute cosine similarity ratio
calculate_group_cos_sim_ratio <- function(token, seed_value) {
  
  # Limit candidates to features in corpus
  feats <- featnames(dfm(token))
  
  # Compute ratio
  set.seed(seed_value)
  target_nns_ratio <- get_nns_ratio(
    x = token,
    N = 20,
    groups = docvars(token, 'party'),
    numerator = "R",
    candidates = feats,
    pre_trained = local_glove,
    transform = TRUE,
    transform_matrix = local_tf_matrix,
    bootstrap = TRUE,
    num_bootstraps = 100,
    permute = TRUE,
    num_permutations = 100,
    verbose = FALSE
  )
  
  return(target_nns_ratio)
  
}


# Identify nearest contexts
get_nc_by_group <- function(token, seed_value) {
  
  print("Identifying nearest contexts.")
  
  # Get nearest neighbors between groups
  target_group_ncs <- get_ncs(
    x = token,
    N = 20,
    groups = docvars(token, "party"),
    pre_trained = local_glove,
    transform = TRUE,
    transform_matrix = local_tf_matrix,
    bootstrap = TRUE,
    num_bootstraps = 100,
    as_list = TRUE
  )
  
  print("Nearest contexts identified.")
  
  # Return output
  return(target_group_ncs)
}



# ------------------------------------------------------------
# Implement ALC analysis  ----
# ------------------------------------------------------------

# Initiate empty list for storing the results
result_nn_list = list()
result_cos_sim_list = list()
result_cos_sim_ratio_list = list()
result_nc_list = list()
result_embedreg_list = list()


# Immigration policy ----

# Build corpus of contexts surrounding the target term
target_tokens <- tokens_context( x = toks_feats, pattern = "immigr*", window = 6L )

# Get NN
result_nn_list[['immigration']] <- get_nn_by_group(
  token = target_tokens,
  seed_value = 41
)

# Get cos sim to pre-defined features
result_cos_sim_list[['immigration']] <- calculate_group_cos_sim(
  token = target_tokens,
  seed_value = 41,
  cos_sim_features = c("inclusive", "security" , "law", "reform", "enforcement", "human", "settle", "integration")
)

# Calculate cos sim ratio
result_cos_sim_ratio_list[['immigration']] <- calculate_group_cos_sim_ratio(
  token = target_tokens,
  seed_value = 41
)

# Get nearest context
result_nc_list[['immigration']] <- get_nc_by_group(
  token = target_tokens,
  seed_value = 41
)

# Embedding regression
set.seed(41)
target_group_time_model <- conText(
  formula = "immigr*" ~ party_session,
  data = toks_feats,
  pre_trained = local_glove,
  transform = TRUE,
  transform_matrix = local_tf_matrix,
  bootstrap = TRUE, num_bootstraps = 100,
  permute = TRUE, num_permutations = 100,
  window = 6, case_insensitive = TRUE,
  valuetype = "glob",
  verbose = TRUE
)
result_embedreg_list[["immigration"]] <- target_group_time_model@normed_coefficients




# Abortion policy ----

# Build corpus of contexts surrounding the target term
target_tokens <- tokens_context( x = toks_feats, pattern = "abortion*|reproducti*", window = 6L )

# Get NN
result_nn_list[['abortion']] <- get_nn_by_group(
  token = target_tokens,
  seed_value = 41
)

# Calculate cos-sim to pre-defined features
result_cos_sim_list[['abortion']] <- calculate_group_cos_sim(
  token = target_tokens,
  seed_value = 41,
  cos_sim_features = c("life", "choice", "privacy", "rights", "health")
)

# Calculate cos-sim ratio
result_cos_sim_ratio_list[['abortion']] <- calculate_group_cos_sim_ratio(
  token = target_tokens,
  seed_value = 41
)

# Get nearest context
result_nc_list[['abortion']] <- get_nc_by_group(
  token = target_tokens,
  seed_value = 41
)

# Embedding regression
set.seed(41)
target_group_time_model <- conText(
  formula = "abortion*|reproducti*" ~ party_session,
  data = toks_feats,
  pre_trained = local_glove,
  transform = TRUE,
  transform_matrix = local_tf_matrix,
  bootstrap = TRUE, num_bootstraps = 100,
  permute = TRUE, num_permutations = 100,
  window = 6, case_insensitive = TRUE,
  valuetype = "glob",
  verbose = TRUE
)
result_embedreg_list[["abortion"]] <- target_group_time_model@normed_coefficients




# Gun laws ----

# Build corpus of contexts surrounding the target term
target_tokens <- tokens_context( x = toks_feats, pattern = c("gun", "guns", "firearm", "firearms"), window = 6L )

# Get NN
result_nn_list[['guns']] <- get_nn_by_group(
  token = target_tokens,
  seed_value = 41
)

# Get cos-sim with pre-defined features
result_cos_sim_list[['guns']] <- calculate_group_cos_sim(
  token = target_tokens,
  seed_value = 41,
  cos_sim_features = c("control", "rights", "prevention", "defense")
)

# Get cos-sim ratio
result_cos_sim_ratio_list[['guns']] <- calculate_group_cos_sim_ratio(
  token = target_tokens,
  seed_value = 41
)

# Get nearest context
result_nc_list[['guns']] <- get_nc_by_group(
  token = target_tokens,
  seed_value = 41
)

# Embedding regression
set.seed(41)
target_group_time_model <- conText(
  formula = c("gun", "guns", "firearm", "firearms") ~ party_session,
  data = toks_feats,
  pre_trained = local_glove,
  transform = TRUE,
  transform_matrix = local_tf_matrix,
  bootstrap = TRUE, num_bootstraps = 100,
  permute = TRUE, num_permutations = 100,
  window = 6, case_insensitive = TRUE,
  valuetype = "glob",
  verbose = TRUE
)
result_embedreg_list[["guns"]] <- target_group_time_model@normed_coefficients



# Climate change policy ----

# Build corpus of contexts surrounding the target term
target_tokens <- tokens_context( x = toks_feats, pattern = c("climate", "climate change", "emission", "global warming"), window = 6L )

# Get NN
result_nn_list[['climate']] <- get_nn_by_group(
  token = target_tokens,
  seed_value = 41
)

# Get cos-sim with pre-defined features
result_cos_sim_list[['climate']] <- calculate_group_cos_sim(
  token = target_tokens,
  seed_value = 41,
  cos_sim_features = c("renewable", "fossil")
)

# Compute cos-sim ratio
result_cos_sim_ratio_list[['climate']] <- calculate_group_cos_sim_ratio(
  token = target_tokens,
  seed_value = 41
)

# Get nearest context
result_nc_list[['climate']] <- get_nc_by_group(
  token = target_tokens,
  seed_value = 41
)

# Embedding regression
set.seed(41)
target_group_time_model <- conText(
  formula = c("climate", "climate change", "emission", "global warming") ~ party_session,
  data = toks_feats,
  pre_trained = local_glove,
  transform = TRUE,
  transform_matrix = local_tf_matrix,
  bootstrap = TRUE, num_bootstraps = 100,
  permute = TRUE, num_permutations = 100,
  window = 6, case_insensitive = TRUE,
  valuetype = "glob",
  verbose = TRUE
)
result_embedreg_list[["climate"]] <- target_group_time_model@normed_coefficients



# Taxation policy ----

# Build corpus of contexts surrounding the target term
target_tokens <- tokens_context( x = toks_feats, pattern = c("tax", "taxes", "taxation"), window = 6L )

# Get nearest neighbor
result_nn_list[['tax']] <- get_nn_by_group(
  token = target_tokens,
  seed_value = 41
)

# Get cos-sim to pre-defined features
result_cos_sim_list[['tax']] <- calculate_group_cos_sim(
  token = target_tokens,
  seed_value = 41,
  cos_sim_features = c("poor", "rich", "progressive", "reform", "cut", "family", "corporate", "business")
)

# Get cos-sim ratio
result_cos_sim_ratio_list[['tax']] <- calculate_group_cos_sim_ratio(
  token = target_tokens,
  seed_value = 41
)

# Get NC
result_nc_list[['tax']] <- get_nc_by_group(
  token = target_tokens,
  seed_value = 41
)

# Embedding regression
set.seed(41)
target_group_time_model <- conText(
  formula = c("tax", "taxes", "taxation") ~ party_session,
  data = toks_feats,
  pre_trained = local_glove,
  transform = TRUE,
  transform_matrix = local_tf_matrix,
  bootstrap = TRUE, num_bootstraps = 100,
  permute = TRUE, num_permutations = 100,
  window = 6, case_insensitive = TRUE,
  valuetype = "glob",
  verbose = TRUE
)
result_embedreg_list[["tax"]] <- target_group_time_model@normed_coefficients



# Racial justice ----

# Build corpus of contexts surrounding the target term
target_tokens <- tokens_context( x = toks_feats, pattern = c("race", "minority", "people color", "racism", "racist", "racial"), window = 6L )

# Get NN
result_nn_list[['race']] <- get_nn_by_group(
  token = target_tokens,
  seed_value = 41
)

# Compute cos-sim to pre-defined features
result_cos_sim_list[['race']] <- calculate_group_cos_sim(
  token = target_tokens,
  seed_value = 41,
  cos_sim_features = c("opportunity", "responsibility", "affirmative", "colorblind", "reform", "law", "community")
)

# Get cos-sim ratio
result_cos_sim_ratio_list[['race']] <- calculate_group_cos_sim_ratio(
  token = target_tokens,
  seed_value = 41
)

# Get nearest context
result_nc_list[['race']] <- get_nc_by_group(
  token = target_tokens,
  seed_value = 41
)

# Embedding regression
set.seed(41)
target_group_time_model <- conText(
  formula = c("race", "minority", "people color", "racism", "racist", "racial") ~ party_session,
  data = toks_feats,
  pre_trained = local_glove,
  transform = TRUE,
  transform_matrix = local_tf_matrix,
  bootstrap = TRUE, num_bootstraps = 100,
  permute = TRUE, num_permutations = 100,
  window = 6, case_insensitive = TRUE,
  valuetype = "glob",
  verbose = TRUE
)
result_embedreg_list[["race"]] <- target_group_time_model@normed_coefficients



# ------------------------------------------------------------
# Export results  ----
# ------------------------------------------------------------

# Export the list objects:
save(result_nn_list, file = here('2_build', 'result_nn.RData'))
save(result_cos_sim_list, file = here('2_build', 'result_cos_sim.RData'))
save(result_cos_sim_ratio_list, here('2_build', 'result_cos_sim_ratio.RData'))
save(result_nc_list, file = here('2_build', 'result_nc.RData'))
save(result_embedreg_list, file = here('2_build', 'result_embedreg.RData'))

