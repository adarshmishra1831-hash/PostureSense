# ===============================
# PostureSensePlus Dashboard (app.R)
# ===============================

library(shiny)
library(ggplot2)
library(readr)

# ---- Load posture data (CSV exported by Python) ----
data_file <- "results.csv"

if (file.exists(data_file)) {
  posture_data <- read_csv(data_file)
} else {
  posture_data <- data.frame(
    Session = 1:5,
    Accuracy = c(60, 70, 75, 85, 90)
  )
}

# ---- Define UI ----
ui <- fluidPage(
  titlePanel("🏋️‍♀️ Exercise Posture Progress Dashboard"),

  sidebarLayout(
    sidebarPanel(
      h4("User Details"),
      textInput("user_name", "Enter your name:", "Adarsh"),
      selectInput("exercise_type", "Exercise Type:",
                  choices = c("Squat", "Push-up", "Deadlift")),
      actionButton("refresh", "Refresh Data")
    ),

    mainPanel(
      h3("📈 Posture Accuracy Over Sessions"),
      plotOutput("accuracy_plot"),
      br(),
      h4("Last Session Feedback:"),
      textOutput("feedback")
    )
  )
)

# ---- Define Server Logic ----
server <- function(input, output, session) {

  observeEvent(input$refresh, {
    if (file.exists(data_file)) {
      posture_data <<- read_csv(data_file)
      showNotification("Data refreshed from results.csv", type = "message")
    }
  })

  output$accuracy_plot <- renderPlot({
    ggplot(posture_data, aes(x = Session, y = Accuracy)) +
      geom_line(size = 1.5, color = "blue") +
      geom_point(size = 3, color = "red") +
      ylim(0, 100) +
      theme_minimal() +
      labs(x = "Session", y = "Posture Accuracy (%)",
           title = paste("Posture Progress -", input$user_name))
  })

  output$feedback <- renderText({
    latest_acc <- tail(posture_data$Accuracy, 1)
    if (latest_acc >= 85) {
      "Excellent posture consistency! ✅"
    } else if (latest_acc >= 70) {
      "Good progress! Keep improving 👏"
    } else {
      "Needs improvement. Check your exercise form 🧍‍♂️"
    }
  })
}

# ---- Run the Shiny App ----
shinyApp(ui = ui, server = server)
