# Paramètres du modèle
r_p <- 0.01  # Taux de croissance des proies
a <- 0.01   # Taux de prédation
b <- 0.02   # Efficacité de reproduction des prédateurs
d <- 0.5   # Taux de mortalité des prédateurs

# Conditions initiales des populations
N_p_0 <- 50  # Population initiale des proies
N_pr_0 <- 1  # Population initiale des prédateurs

# Temps d'observation (de 0 à 100, par pas de 1)
t <- seq(0, 100, by=1)

# Modèle de Lotka-Volterra ajusté avec reproduction des prédateurs
model <- function(t, state, parameters) {
  with(as.list(c(state, parameters)), {
    # Modèle de la population des proies
    dN_p <- r_p * N_p - a * N_p * N_pr
    # Modèle de la population des prédateurs avec reproduction basée sur la prédation
    dN_pr <- b * N_p * N_pr - d * N_pr
    return(list(c(dN_p, dN_pr)))
  })
}

# Définir l'état initial
state <- c(N_p = N_p_0, N_pr = N_pr_0)

# Paramètres du modèle
parameters <- c(r_p = r_p, a = a, b = b, d = d)

# Résolution du système d'équations différentielles
library(deSolve)
out <- ode(y = state, times = t, func = model, parms = parameters)

# Convertir la sortie en data frame pour ggplot
out_df <- as.data.frame(out)

# Visualisation améliorée avec ggplot2
library(ggplot2)
ggplot(out_df, aes(x = time)) +
  geom_line(aes(y = N_p, color = "Proies"), size = 1.5) + 
  geom_line(aes(y = N_pr, color = "Prédateurs"), size = 1.5) +
  labs(title = "Dynamique Proie-Prédateur",
       x = "Temps",
       y = "Population",
       color = "Légende") +
  scale_color_manual(values = c("Proies" = "blue", "Prédateurs" = "red")) +
  theme_minimal(base_size = 15) +
  theme(legend.position = "topright",
        panel.grid.major = element_line(color = "gray", size = 0.5, linetype = "dotted"),
        panel.grid.minor = element_line(color = "gray", size = 0.25, linetype = "dotted"))
