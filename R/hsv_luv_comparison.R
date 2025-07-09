library(dplyr)
library(colorspace)
library(ggplot2)
library(tidyr)

# Exemple : 36 couleurs autour du cercle (tous les 10°)
n_colors <- 72
angles <- seq(0, 355, length.out = n_colors)  # HSV Hues

# Générer les HSV → RGB → hex pour couleur
hsv_colors <- HSV(H = angles, S = 0.5, V = 1)
rgb_colors <- as(hsv_colors, "RGB")
hex_colors <- hex(rgb_colors)

# Mettre dans un data frame
df <- data.frame(
  color_angle = angles,
  H = angles,
  S = 0.5,
  V = 1
)
df <- df |>
  mutate(
    color = hsv(h = H/360, 0.5, 1))

# Fonction pour convertir HSV en CIELUV coords
hsv_to_luv_coords <- function(h, s, v) {
  hsv_col <- HSV(H = h, S = s, V = v)
  rgb_col <- as(hsv_col, "RGB")
  luv_col <- as(rgb_col, "LUV")
  return(luv_col@coords)
}

# Calcule la distance ΔE (LUV) entre chaque couleur et la suivante
df <- df %>%
  rowwise() %>%
  mutate(
    LUV_coords = list(hsv_to_luv_coords(H, S, V)),
    L = LUV_coords[1],
    u = LUV_coords[2],
    v = LUV_coords[3]
  ) %>%
  ungroup()


# Boucle pour refermer le cercle
df <- df %>%
  mutate(
    next_L = lead(L),
    next_u = lead(u),
    next_v = lead(v),
    err_luv = sqrt((L - next_L)^2 + (u - next_u)^2 + (v - next_v)^2)
  )

df[n_colors, c("next_L", "next_u", "next_v")] <- df[1, c("L", "u", "v")]
df[n_colors, "err_luv"] <- sqrt(
  (df[n_colors, "L"] - df[1, "L"])^2 +
    (df[n_colors, "u"] - df[1, "u"])^2 +
    (df[n_colors, "v"] - df[1, "v"])^2
)


ggplot(df, aes(x = color_angle, y = err_luv, fill = color)) +
  geom_bar(stat = "identity", width = 360/n_colors) +
  coord_polar(theta = "x", start = 0, direction = 1) +
  scale_fill_identity() +
  ylim(0, max(df$err_luv, na.rm = TRUE)) +
  theme_minimal() +
  labs(title = "Différences perceptuelles entre teintes HSV consécutives (CIELUV)",
       x = "Angle HSV", y = "ΔE perceptif (CIELUV)")

