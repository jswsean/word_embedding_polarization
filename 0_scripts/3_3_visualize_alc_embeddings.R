# Script to visualize results from ALC embedding analysis

# ----------------------------------------------
# Preliminaries
# ----------------------------------------------

# Load the required libraries
library(dplyr)
library(tidyr)
library(ggplot2)
library(here)
library(stringr)
library(ggwordcloud)
library(ggrepel)

# Set default theme 
default_theme <- theme_minimal()
theme_set(default_theme)


# ----------------------------------------------
# Load objects
# ----------------------------------------------

# Load 2_3 results
load(
    here('2_build', 'result_nn.RData')
)

load(
    here('2_build', 'result_cos_sim.RData')
)

load(
    here('2_build', 'result_cos_sim_ratio.RData')
)

load(
    here('2_build', 'result_nc.RData')
)

load(
    here('2_build', 'result_embedreg.RData')
)


# ----------------------------------------------
# Define visualizer functions
# ----------------------------------------------

r_color = "tomato1"
d_color = "steelblue2"

# Function to export top nearest neighbor terms
plot_alc_nn <- function(topic, top_nn_terms = 20) {

    # Set seed
    set.seed(41)

    # Plot 
    plot <- ggplot(
        (
            bind_rows(result_nn_list[[topic]]) %>% 
                arrange(target, desc(value)) %>% 
                mutate(
                    target = if_else(target == "D", "Democrat", "Republican"), 
                    seq = row_number(), 
                    .by = target
                ) %>% 
                filter(seq <= top_nn_terms)
        ), 
        aes(label = feature, size = value, color = value)
    ) + 
        geom_text_wordcloud_area() + 
        scale_size_area(max_size = 30, trans = power_trans(5)) +
        facet_wrap(~target) +
        scale_color_continuous(trans = "reverse") +
        theme(
            strip.text = element_text(size = 15)
        )

    # Create filename 
    filename = str_c("alc_nn_", topic, "_plot.pdf")

    # Export plot.
    ggsave( 
        here('3_docs', 'figure', filename),
        plot,
        width = 8,
        height = 4, 
        units = "in", 
        dpi = 500
    )    
}


# Function to visualize cosine similarity along pre-defined features.
plot_alc_cos_sim <- function(topic) {

    # Plot
    plot <- ggplot(
        (
            result_cos_sim_list[[topic]] %>% 
                mutate(
                    target = if_else(target == "D", "Democrat", "Republican")
                )
        ), 
        aes(x = feature, y = value, fill = target)
    ) + 
        geom_col(position = "dodge") +
        geom_errorbar(
            aes(ymin = lower.ci, ymax = upper.ci), 
            width = .2, position = position_dodge(.9) 
        ) +
        labs(
            x = "Dimension keyword", 
            y = "Cosine similarity",
            fill = "Party"
        ) +
        scale_fill_manual(
            values = c(d_color, r_color)
        ) +
        theme(
            axis.text = element_text(size = 8),
            axis.title = element_text(size = 10)
        )

    # Create filename 
    filename = str_c("alc_cos_sim_", topic, "_plot.pdf")

    # Export plot.
    ggsave( 
        here('3_docs', 'figure', filename),
        plot,
        width = 8,
        height = 5, 
        units = "in", 
        dpi = 500
    )    
}


# Function to visualize cosine similarity ratio
plot_alc_cos_sim_ratio <- function(topic) {

    # Plot
    plot <- ggplot(
        (
            result_cos_sim_ratio_list[[topic]] %>% 
                mutate(
                    group = case_when(group == "D" ~ "Democrat",
                                    group == "R" ~ "Republican", 
                                    .default = "Shared")
                )
        ), 
        aes(x = value, y = reorder(feature, value), color = group)
    ) +
        geom_vline(xintercept = 1, color = "red") +
        geom_errorbarh(aes(xmin = lower.ci, xmax = upper.ci), height = .35) +
        geom_label_repel(
            aes(label = feature),
            segment.color = "white",
            point.padding = .1,
            box.padding = .1
        ) +
        geom_point(size = 2) +
        labs(
            x = expression("Cosine similarity ratio:" %->% "more discriminant of Republicans"), 
            y = "Term",
            color = ""
        ) + 
        scale_color_manual(
            values = c(d_color, r_color, "grey60")
        ) +
        theme(
            axis.text.x = element_text(size = 10),
            axis.text.y = element_blank(), 
            axis.title = element_text(size = 12)
        )

    # Create filename 
    filename = str_c("alc_cos_sim_ratio_", topic, "_plot.pdf")

    # Export plot.
    ggsave( 
        here('3_docs', 'figure', filename),
        plot,
        width = 8,
        height = 6, 
        units = "in", 
        dpi = 500
    )        
}
    


# Function to plot embedding regression coefficients.
plot_alc_embedreg <- function(topic) {

    # Plot
    plot <- ggplot(
        (
            result_embedreg_list[[topic]] %>% 
                filter(str_sub(coefficient, -5, -1) %in% 
                    c("D_108", "D_109", "D_110", "D_111", "D_112", "D_113", "D_114",
                      "R_108", "R_109", "R_110", "R_111", "R_112", "R_113", "R_114")
                ) %>% 
                mutate( 
                    session = str_sub(coefficient, -3, -1),
                    party = str_sub(coefficient, -5, -5),
                    party = if_else(
                        party == "D", "Democrats", "Republican"
                    ),
                    year = case_when( 
                        session == "108" ~ "2003-2005", 
                        session == "109" ~ "2005-2007", 
                        session == "110" ~ "2007-2009", 
                        session == "111" ~ "2009-2011", 
                        session == "112" ~ "2011-2013", 
                        session == "113" ~ "2013-2015", 
                        session == "114" ~ "2015-2017"
                    ),
                    year = factor(
                        year, levels = c("2003-2005", "2005-2007", "2007-2009", 
                                         "2009-2011", "2011-2013", "2013-2015", 
                                         "2015-2017"))
                )
        ), 
        aes( y = normed.estimate, x = year , color = party, group = party)
    ) +
    geom_hline(yintercept = 0, color = "red") +
    geom_point(size = 3.5) +
    geom_errorbar(aes(ymin = lower.ci, ymax = upper.ci), 
                  width = .1) +
    coord_cartesian(
        ylim = c(-.5, NA)
    ) +
    scale_color_manual(
        values = c(d_color, r_color)
    ) +
    labs( 
        x = "Congress sessions in year ...", 
        y = "Estimated semantic differences r.t. 2003-2004 Dems.",
        color = "Party"
    ) +
    theme(
        axis.text.y = element_text(size = 11),
        axis.text.x = element_text(size = 9), 
        axis.title = element_text(size = 12)
    )


    # Create filename 
    filename = str_c("alc_embedreg_", topic, "_plot.pdf")

    # Export plot.
    ggsave( 
        here('3_docs', 'figure', filename),
        plot,
        width = 8,
        height = 6, 
        units = "in", 
        dpi = 500
    )        

}

# ----------------------------------------------
# Write output 
# ----------------------------------------------

# Define topics
topics = c("immigration", "abortion", "guns", "climate", "tax", "race")

# Plot ALC NN
for (topic in topics) {
    plot_alc_nn(topic = topic)
}

# Plot ALC cos-sim
for (topic in topics) {
    plot_alc_cos_sim(topic)
}

# Plot ALC cos-sim ratio
for (topic in topics) {
    plot_alc_cos_sim_ratio(topic)
}

# Plot ALC embed reg results
for (topic in topics) {
    plot_alc_embedreg(topic)
}
