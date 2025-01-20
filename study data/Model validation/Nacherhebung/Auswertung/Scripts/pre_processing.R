# Load Data

data_en <- read.csv(file = data_path_eng)


rm(data_path_eng)

# Add Country column

data_en$country <- "England"

# Combine data

data <- data_en

rm(data_en)


ai_items <- read.xlsx("Sources/sample_items.xlsx")

items <- ai_items

rm(ai_items)
# Exclude Participants

data <- data%>%
  filter((country == "Germany" & !(Q15 <= 23|is.na(SQ09)|Q125==1))|
           (country == "England" & !(is.na(SQ09)|Q125==1|Q16_1>3|Q16_2<6)))





# Create functions for data cleaning

## Invert items

invert_items <- function(item_vector,max=6){
  
  new_item_vector = (max+1)-item_vector
  return(new_item_vector)
}

## Repair incorrect values: 18,19,20,22,23,24 to 1,2,3,4,5,6

repair_values <- function(item_vector){
  
  new_item_vector <- (item_vector)%>%as.numeric()
  
  new_item_vector[new_item_vector==18] <- 1
  new_item_vector[new_item_vector==19] <- 2
  new_item_vector[new_item_vector==20] <- 3
  new_item_vector[new_item_vector==22] <- 4
  new_item_vector[new_item_vector==23] <- 5
  new_item_vector[new_item_vector==24] <- 6
  
  return(new_item_vector)
}


# Format data

## Convert to numeric

data[,13:60] <- data[,13:60]%>%apply(FUN=as.numeric, MARGIN = 2)




## Invert items

for(i in 1:nrow(items)){
  if(items$inverted[i]==TRUE){
    
    data[,12+i] <- invert_items(data[,12+i])
    
  }
}

# Make minimum of scales equal to zero

data[,13:60] <- data[,13:60]-1

## Collect Items into a list of constructs


#items$construct <- mapply(items$construct,FUN = function(x) str_replace_all(x,pattern = "_\\d+",replacement = ""))

scales <- list()

for(level in names(table(items$construct))){
  
  ids <- which(items$construct==level)
  ids <- ids+12
  scales <- append(scales, list((data[,ids])))
  
}

names(scales) <- names(table(items$construct))

## Create Scales from the list of constructs

nfc_total <- data.frame(scales[c("need_for_closure_1", "need_for_closure_2", "need_for_closure_3", "need_for_closure_4", "need_for_closure_5")])

oc <- data.frame(scales[c("o_commit_1")])



# Get the means 

item_means <- apply(data[,13:60],FUN = mean,MARGIN = 2)

