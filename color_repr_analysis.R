# Charger les librairies nécessaires
library(readr)
library(dplyr)
library(ggplot2)
library(purrr)
library(stringr)
library(tools)
library(scales)  # pour la fonction hue_pal()

setwd(dirname(rstudioapi::getSourceEditorContext()$path))

get_data <- function(files){
  data_all  <- files |>
    set_names() |>
    map_dfr(\(file) {
      read_csv(paste0('data/', file)) |>
        mutate(
          error = ((response - stim + 180) %% 360 - 180),
          source = file_path_sans_ext(basename(file)),
          hue = (stim %% 360) / 360,
          color = hsv(h = hue, s = 0.5, v = 1)
        )
    })

  data_all <- data_all |>
    mutate(
      stim_corrected =
        case_when(grepl('blue', source) ~ stim * 90 / 360 + 180,
                  TRUE ~ stim),
      response_corrected =
        case_when(grepl('blue', source) ~ response * 90 / 360 + 180,
                  TRUE ~ response),
      error_corrected =
        case_when(grepl('blue', source) ~ ((response_corrected - stim_corrected + 180) %% 360 - 180),
                  TRUE ~ error),

    ) |>
    select(
      source,
      stim,
      stim_corrected,
      response,
      response_corrected,
      error,
      error_corrected,
      hue,
      color)

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
  ggplot(df |> filter(source == source_value),
         aes(x = stim, y = abs(error), fill =color)) +
    geom_bar(stat = "identity") +
    ylim(0, 100) +
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
      aes(x = x, y = y, label = text, angle = angle_label, hjust = hjust),
      color = "black", size = 3
    ) +
    coord_fixed() +
    theme_void() +
    labs(title = "Textes placés autour de la roue chromatique")

}

data_files = fichiers <- c(
  'aphantasia_lc_match.csv',
  'aphantasia_lc_recall_1.csv',
  'aphantasia_lc_trad_text_to_color_1.csv',
  'aphantasia_lc_trad_color_to_spatial_1.csv',
  'aphantasia_lc_blue_match.csv',
  'aphantasia_lc_blue_recall.csv',
  'aphantasia_lc_blue_trad_text_to_color.csv',
  'aphantasia_lc_blue_trad_color_to_spatial.csv',
  'aphantasia_lc_blue_match_1.csv',
  'aphantasia_lc_blue_recall_1.csv',
  'aphantasia_lc_recall_squares.csv'
)

df <- get_data(data_files)

sources_to_plot = c(
  'aphantasia_lc_blue_match',
  'aphantasia_lc_blue_match_1',
  'aphantasia_lc_blue_recall',
  'aphantasia_lc_blue_recall_1',
  'aphantasia_lc_blue_trad_text_to_color',
  'aphantasia_lc_blue_trad_color_to_spatial',
  'aphantasia_lc_recall_squares'
)


plot_error_distribution_by_file(df, sources_to_plot)
plot_error_by_color(df, 'aphantasia_lc_match')
plot_error_by_color(df, 'aphantasia_lc_blue_recall')

plot_error_by_color(df, 'aphantasia_lc_blue_match')
plot_error_by_color(df, 'aphantasia_lc_blue_trad_text_to_color')
plot_error_by_color(df, 'aphantasia_lc_blue_trad_color_to_spatial')


plot_color_description('data/aphantasia_lc_blue_describe.csv')


