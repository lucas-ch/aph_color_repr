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
          error = ((selected - color_angle + 180) %% 360 - 180),
          source = file_path_sans_ext(basename(file)),
          hue = (color_angle %% 360) / 360,
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
  ggplot(df |> filter(source == source_value),
         aes(x = color_angle, y = abs(error), fill =color)) +
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
      angle_rad = color_angle * pi / 180,
      x = cos(angle_rad) * 0.6,
      y = sin(angle_rad) * 0.6,
      hue = (color_angle %% 360) / 360,
      color = hsv(h = hue, s = 0.5, v = 1),
      angle_label = ifelse(between(color_angle, 90, 270), color_angle + 180, color_angle),
      hjust = ifelse(between(color_angle, 90, 270), 1, 0)
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
  'aphantasia_lc_recall.csv',
  'aphantasia_lc_recall_with_text.csv',
  'aphantasia_lc_recall_3.csv',
  'aphantasia_lc_recall_with_text_4.csv',
  'aphantasia_lc_match_without_color.csv',
  'aphantasia_lc_blue_match.csv',
  'aphantasia_lc_blue_recall.csv',
  'aphantasia_lc_blue_trad_text_to_color.csv',
  'aphantasia_lc_blue_trad_color_to_spatial.csv'
)

df <- get_data(data_files)

sources_to_plot = c(
  'aphantasia_lc_recall',
  'aphantasia_lc_recall_with_text',
  'aphantasia_lc_recall_3',
  'aphantasia_lc_recall_with_text_4',
  'aphantasia_lc_match_without_color',
  'aphantasia_lc_blue_recall',
  'aphantasia_lc_blue_trad_text_to_color',
  'aphantasia_lc_blue_trad_color_to_spatial'
)


plot_error_distribution_by_file(df, sources_to_plot)
plot_error_by_color(df, 'aphantasia_lc_match')
plot_error_by_color(df, 'aphantasia_lc_blue_recall')

plot_error_by_color(df, 'aphantasia_lc_blue_match')
plot_error_by_color(df, 'aphantasia_lc_blue_trad_text_to_color')
plot_error_by_color(df, 'aphantasia_lc_blue_trad_color_to_spatial')


plot_color_description('data/aphantasia_lc_blue_describe.csv')

df_corrected <- df |>
  mutate(
    color_angle_corrected =
      case_when(grepl('blue', source) ~ color_angle * 90 / 360 + 180,
                        TRUE ~ color_angle),
    selected_corrected =
      case_when(grepl('blue', source) ~ selected * 90 / 360 + 180,
                TRUE ~ selected),
    error_corrected =
      case_when(grepl('blue', source) ~ ((selected_corrected - color_angle_corrected + 180) %% 360 - 180),
                TRUE ~ error),

  ) |>
  select(source, color_angle, color_angle_corrected, selected, selected_corrected, error, error_corrected, hue, color) |>
   filter(color_angle_corrected > 185 & color_angle_corrected < 175 + 90) |>
  group_by(source) |>
  reframe(mean(abs(error_corrected)))

