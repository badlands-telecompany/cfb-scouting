# College Football Stats Shiny App
# 
# Author: Federico Scivittaro
# Last Modified: 1/17/19

setwd("C:/Users/fgsci/OneDrive/Documents/GitHub/cfb-scouting/")

library(shiny)
library(shinythemes)
library(data.table)

passing <- fread("Data/passing.csv")
rush_rec <- fread("Data/rush_receiving_shares.csv")
defense <- fread("Data/defense_shares.csv")
combine <- fread("Data/combine.csv")


# Define UI for app
ui <- navbarPage("Mesh Point Scouting",
                 theme = shinytheme("cosmo"),
           
  tabPanel("Raw Stats",
   
    fluidRow(
     
      column(4,
            
        "test"
            
      ),
     
      column(4,
            
        "test"
            
      ),
     
      column(4,
            
        img(src='logo.jpg',
            width = 250,
            align = "right"
        )
      )
    )                 
  ),
  
  tabPanel("Market Share Stats",
           
    fluidRow(
     
      column(4,
            
        "test"
            
      ),
     
      column(4,
            
        "test"
            
      ),
     
      column(4,
            
        img(src='logo.jpg',
            width = 250,
            align = "right"
        )
      )
    ) 
  ),
  
  tabPanel("Combine Data",
   
    fluidRow(
     
      column(4,
            
        "test"
            
      ),
     
      column(4,
            
        "test"
            
      ),
     
      column(4,
            
        img(src='logo.jpg',
            width = 250,
            align = "right"
        )
      )
    ) 
  )
)

# Define server logic
server <- function(input, output) {
  
  output$test <- renderTable(
    
    combine[1:input$num_results, ]
    
  )
  
}

# Create Shiny app ----
shinyApp(ui = ui, server = server)