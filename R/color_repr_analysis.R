# Charger les librairies nécessaires
library(readr)
library(dplyr)
library(ggplot2)
library(purrr)
library(stringr)
library(tools)
library(scales)  # pour la fonction hue_pal()

setwd(dirname(rstudioapi::getSourceEditorContext()$path))

get_data <- function(data_files){
  data_all  <- data_files |>
    set_names() |>
    map_dfr(\(file) {
      read_csv(paste0('../archive/data/', file), col_types = cols(.default = "c")) |>
        filter(!is.na(as.numeric(response))) |>
        mutate(
          response = as.numeric(response),
          stim = as.numeric(stim),
          error = ((response - stim + 180) %% 360 - 180),
          source = file_path_sans_ext(basename(file)),
          hue = (stim %% 360) / 360,
          color = hsv(h = hue, s = 0.5, v = 1)
        )
    })
  return(data_all)
}

plot_error_distribution_by_file <- function(df, sources) {
  ggplot(df
         |> filter(source %in% sources), aes(x = error, color = source)) +
    geom_density(alpha = 0.3) +
    labs(
      title = "Distribution des erreurs par tâche",
      x = "Erreur (en degrés)",
      y = "Densité",
      color = "Fichier",
      fill = "Fichier"
    ) +
    theme_minimal()
}

plot_error_by_color <- function(df, source_value){
  df_plot <- df |>
    filter(source == source_value) |>
    rowwise() |>
    mutate(
      error = min(19, abs(error))
    )

  ggplot(df_plot,
         aes(x = stim, y = error, fill = color)) +
    geom_bar(stat = "identity") +
    ylim(0, 20) +
    coord_polar(theta = "x", start = 0, direction = 1) +
    scale_fill_identity() +
    theme_minimal()
}

plot_color_description <- function(file) {
  df <- read_csv(file)
  text_data  <- df |>
    mutate(
      angle_rad = stim * pi / 180,
      x = cos(angle_rad) * 0.6,
      y = sin(angle_rad) * 0.6,
      hue = (stim %% 360) / 360,
      color = hsv(h = hue, s = 0.5, v = 1),
      angle_label = ifelse(between(stim, 90, 270), stim + 180, stim),
      hjust = ifelse(between(stim, 90, 270), 1, 0)
    )

  wheel_data <- tibble(
    angle = seq(0, 359, by = 1),
    angle_rad = angle * pi / 180,
    x = cos(angle_rad),
    y = sin(angle_rad),
    color = hsv(h = angle / 360, s = 0.5, v = 1)
  )

  ggplot() +
    geom_tile(data = wheel_data, aes(x = x, y = y, fill = color), width = 0.05, height = 0.05) +
    scale_fill_identity() +
    geom_text(
      data = text_data,
      aes(x = x, y = y, label = response, angle = angle_label, hjust = hjust),
      color = "black", size = 3
    ) +
    coord_fixed() +
    theme_void() +
    labs(title = "Textes placés autour de la roue chromatique")

}

data_files <- c(
  'aphantasia_lc_match_color_to_wheel.csv',
  'aphantasia_lc_match_text_to_wheel.csv',
  'aphantasia_lc_match_color_to_wheel_0.csv',
  'aphantasia_lc_recall_spatial_to_wheel.csv',
  'aphantasia_lc_recall_text_to_squares.csv',
  'aphantasia_lc_match_text_to_wheelGrey.csv',
  'aphantasia_lc_recall_color_to_wheel.csv'
)

df <- get_data(data_files)

sources_to_plot = c(
  'aphantasia_lc_match_color_to_wheel',
  'aphantasia_lc_match_text_to_wheel',
  'aphantasia_lc_match_color_to_wheel_0',
  'aphantasia_lc_recall_spatial_to_wheel',
  'aphantasia_lc_recall_text_to_squares',
  'aphantasia_lc_match_text_to_wheelGrey',
  'aphantasia_lc_recall_color_to_wheel'
)


plot_error_distribution_by_file(df, sources_to_plot)
plot_error_by_color(df, 'aphantasia_lc_1752174850_from_None_to_wheel_with_color')
plot_error_by_color(df, 'aphantasia_lc_1752176270_from_text_to_wheel_with_None')
plot_error_by_color(df, 'aphantasia_test_1752178125_from_color_to_wheel_with_None')


plot_color_description('../data/aphantasia_lc_describe_45_colors_from_0_to_360.csv')



