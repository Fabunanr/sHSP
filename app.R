#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(ape)
library(msaR)
library(phylobase)
library(Biostrings)

# library(htmlwidgets)
devtools::install_github('ramnathv/htmlwidgets')

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("MSA R output test"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            fileInput("fasta",
                        "Enter Fasta File:"),
            fileInput("tree",
                      "Enter Tree File")
        ),

        # Show a plot of the generated distribution
        mainPanel(
            plotOutput("treeout"),
            msaROutput("msa")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    fasta <- reactive({
        # req(input$fasta,
        #     !rv$clear)
        
        file <- input$fasta
        # output <- read.fasta(file$datapath)
        output <- readAAMultipleAlignment(file$datapath, format = "fasta")
        return(output)

        
    })
    
    
    output$msa <- renderMsaR(
        msaR(fasta())
    )
    
    tree <- reactive({
        
        tfile <- input$tree
        toutput <- read.tree(tfile$datapath)
        return(toutput)
    })
    
    output$treeout <- renderPlot(
        plot(tree())
    )
    
    output$msa <- renderMsaR(
        msaR(fasta())
    )
}

# Run the application 
shinyApp(ui = ui, server = server)
