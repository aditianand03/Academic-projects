# Load required libraries
library(readxl)
library(dplyr)
library(ggplot2)
library(lubridate)
library(plotly)
library(tidyr)

# Step 1: Read and clean data
data <- read_excel("IAEA_DATABASE.xlsx", sheet = "Status of Nuc globally")

clean_data <- data %>%
  rename(
    Comm_Op = `Comm. Operation`,
    Shut_Down = `Suspended operation date`,
    Net_Cap = Capacity_Net,
    Status = Staus
  ) %>%
  mutate(
    Comm_Op = as.Date(paste0(Comm_Op, "-01"), format = "%Y-%m-%d"),
    Shut_Down = as.Date(paste0(Shut_Down, "-01"), format = "%Y-%m-%d"),
    Net_Cap = as.numeric(Net_Cap),
    Year = year(Comm_Op)
  ) %>%
  filter(Status == "Operational", !is.na(Comm_Op), !is.na(Net_Cap), Net_Cap > 0) %>%
  filter(is.na(Shut_Down) | Comm_Op < Shut_Down) %>%
  mutate(
    Country_Group = ifelse(Country == "USA", "USA", "Rest of World")
  )

# Step 2: Create shutdown year and expand to each plant's life
expanded_data <- clean_data %>%
  mutate(Shutdown_Year = Year + 60) %>%
  rowwise() %>%
  mutate(Year_Range = list(seq(Year, min(Shutdown_Year, 2050)))) %>%
  unnest(cols = c(Year_Range)) %>%
  ungroup() %>%
  select(Country_Group, Net_Cap, Year = Year_Range)

# Step 3: Aggregate capacity by year and country group
agg_capacity <- expanded_data %>%
  group_by(Country_Group, Year) %>%
  summarise(Net_Capacity = sum(Net_Cap, na.rm = TRUE), .groups = "drop") %>%
  arrange(Country_Group, Year)

# Step 4: Create scenarios -----------------------------------

# 4A. Historical (up to 2025)
historical <- agg_capacity %>%
  filter(Year <= 2025) %>%
  select(Year, Country_Group, Value = Net_Capacity) %>%
  mutate(Scenario = "Historical & No New Builds")

# 4B. No new builds (post-2025)
no_new_builds <- agg_capacity %>%
  filter(Year > 2025 & Year <= 2050) %>%
  select(Year, Country_Group, Value = Net_Capacity) %>%
  mutate(Scenario = "No New Builds")

# 4C. Required new builds to maintain 2025 levels
baseline_2025 <- agg_capacity %>%
  filter(Year == 2025) %>%
  select(Country_Group, Target_Capacity = Net_Capacity)

future_required <- agg_capacity %>%
  filter(Year > 2025 & Year <= 2050) %>%
  left_join(baseline_2025, by = "Country_Group") %>%
  mutate(
    Deficit = pmax(0, Target_Capacity - Net_Capacity),
    Value = Net_Capacity + Deficit
  ) %>%
  select(Year, Country_Group, Value) %>%
  mutate(Scenario = "With Required New Builds")

# Combine 3 core scenarios
combined <- bind_rows(historical, no_new_builds, future_required)
combined$Scenario <- as.character(combined$Scenario)

# Step 5: USA 300% linear growth scenario ----------------------

# Vector of years
years <- 2025:2050

# USA baseline in 2030
usa_base <- agg_capacity %>%
  filter(Country_Group == "USA", Year == 2030) %>%
  pull(Net_Capacity)

# 300% target and linear growth
usa_target <- usa_base * 3
annual_increase <- (usa_target - usa_base) / (2050 - 2030)

usa_linear_growth <- data.frame(
  Country_Group = "USA",
  Year = years,
  Net_Capacity = ifelse(
    years < 2030,
    usa_base,
    usa_base + (years - 2030) * annual_increase
  )
)

# Rest of world remains unchanged
rest_world <- agg_capacity %>%
  filter(Country_Group == "Rest of World", Year %in% years)

# Combine USA growth and Rest of World
capacity_combined <- bind_rows(usa_linear_growth, rest_world)
capacity_combined$Scenario <- "Linear 300% USA Growth"

# Format for joining
capacity_combined <- capacity_combined %>%
  rename(Value = Net_Capacity) %>%
  select(Year, Country_Group, Value, Scenario)

# Final combined data
full_combined <- bind_rows(combined, capacity_combined)

# Step 6: Final plot ------------------------------------------

p_combined <- ggplot(full_combined, aes(
  x = Year,
  y = Value,
  color = Country_Group,
  linetype = Scenario,
  group = interaction(Country_Group, Scenario),
  text = paste0("Year: ", Year,
                "<br>Capacity: ", round(Value, 0), " MW",
                "<br>Group: ", Country_Group,
                "<br>Scenario: ", Scenario))) +
  geom_line(size = 1.2) +
  labs(
    title = "Nuclear Capacity Projection Including 300% USA Growth Scenario",
    x = "Year",
    y = "Net Capacity (MW)",
    color = "Country Group",
    linetype = "Scenario"
  ) +
  theme_minimal()

# Interactive plot
ggplotly(p_combined, tooltip = "text")

