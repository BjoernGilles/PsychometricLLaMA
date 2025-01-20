# Load data

# Participant data
data_ger_tmp <- read.csv(file = data_path_ger)
data_ger_tmp <- data_ger_tmp[0,]
data_ger <- read.csv(file = data_path_ger,skip = 3,header = FALSE)
colnames(data_ger)<- colnames(data_ger_tmp)

data_en_tmp <- read.csv(file = data_path_eng)
data_en_tmp <- data_en_tmp[0,]
data_en <- read.csv(file = data_path_eng,skip = 3,header = FALSE)
colnames(data_en)<- colnames(data_en_tmp)

rm(data_ger_tmp,data_en_tmp, data_path_eng,data_path_ger)

# Add Country column

data_ger$country <- "Germany"
data_en$country <- "England"

# Combine data

data <- plyr::rbind.fill(data_ger,data_en) 

rm(data_ger,data_en)


ai_items <- read.csv("Sources/selected_items_final.csv")
kern_items <- read.xlsx("Sources/Kern_Items.xlsx")

items <- rbind(ai_items,kern_items)

rm(ai_items,kern_items)
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

## Use repair function for variable index 13 to 114

data[data$country=="Germany",13:114] <- apply(data[data$country=="Germany",13:114],FUN = repair_values,MARGIN = 2)

## Fix inversion values in the Item frame

items$inverted[items$inverted=="True"] <- TRUE
items$inverted[items$inverted=="False"] <- FALSE

## Invert items

for(i in 1:nrow(items)){
  if(items$inverted[i]==TRUE){
    
    data[,12+i] <- invert_items(data[,12+i])
    
  }
}

# Make minimum of scales equal to zero

data[,13:114] <- data[,13:114]-1

## Collect Items into a list of constructs


items$construct <- mapply(items$construct,FUN = function(x) str_replace_all(x,pattern = "_\\d+",replacement = ""))

scales <- list()

for(level in names(table(items$construct))){
  
  ids <- which(items$construct==level)
  ids <- ids+12
  scales <- append(scales, list((data[,ids])))
  
}

names(scales) <- names(table(items$construct))

## Create Scales from the list of constructs

ocean_ai_gen <- data.frame(scales[c(1:3,11,12)])
bfi_10 <- data.frame(scales[c('kern_agreeableness','kern_extraversion','kern_openness',"kern_conscientiousness","kern_neuroticism")])
nfc_kern <- data.frame(scales["kern_need_for_closure"])
nfc <- data.frame(scales["need_for_closure"])

scale_list_efa <- list(ocean_ai_gen,bfi_10,nfc_kern,nfc)


ocean_ai_gen_o <- data.frame(scales['openness'])
ocean_ai_gen_c <- data.frame(scales['conscientiousness'])
ocean_ai_gen_e <- data.frame(scales['extraversion'])
ocean_ai_gen_a <- data.frame(scales['agreeableness'])
ocean_ai_gen_n <- data.frame(scales['neuroticism'])

bfi_10_o <- data.frame(scales['kern_openness'])
bfi_10_c <- data.frame(scales['kern_conscientiousness'])
bfi_10_e <- data.frame(scales['kern_extraversion'])
bfi_10_a <- data.frame(scales['kern_agreeableness'])
bfi_10_n <- data.frame(scales['kern_neuroticism'])


#scale_list_subscales <- list(ocean_ai_gen_o,ocean_ai_gen_c,ocean_ai_gen_e,ocean_ai_gen_a,ocean_ai_gen_n,bfi_10_o,bfi_10_c,bfi_10_e,bfi_10_a,bfi_10_n,nfc_kern,nfc)

# Incorporate Item-Selection decisions

load("Sources/scales_selected.Rdata")

ocean_ai_gen_a <- ocean_ai_gen_a[,colnames(ocean_ai_gen_a)%in%colnames(ocean_ai_gen_6)]
ocean_ai_gen_o <- ocean_ai_gen_o[,colnames(ocean_ai_gen_o)%in%colnames(ocean_ai_gen_6)]


ocean_a_mean <- apply(ocean_ai_gen_a,1,mean)
ocean_c_mean <- apply(ocean_ai_gen_c,1,mean)
ocean_e_mean <- apply(ocean_ai_gen_e,1,mean)
ocean_o_mean <- apply(ocean_ai_gen_o,1,mean)
ocean_n_mean <- apply(ocean_ai_gen_n,1,mean)

nfc_mean <- apply(nfc_3,1,mean)

bfi_10_a_mean <- apply(bfi_10_a,1,mean)
bfi_10_c_mean <- apply(bfi_10_c,1,mean)
bfi_10_e_mean <- apply(bfi_10_e,1,mean)
bfi_10_o_mean <- apply(bfi_10_o,1,mean)
bfi_10_n_mean <- apply(bfi_10_n,1,mean)

nfc_kern_mean <- apply(nfc_kern,1,mean)

scale_means <- data.frame(ocean_a_mean = ocean_a_mean,
                          ocean_c_mean = ocean_c_mean,
                          ocean_e_mean = ocean_e_mean,
                          ocean_o_mean = ocean_o_mean,
                          ocean_n_mean = ocean_n_mean,
                          nfc_mean = nfc_mean,
                          bfi_10_a_mean = bfi_10_a_mean,
                          bfi_10_c_mean = bfi_10_c_mean,
                          bfi_10_e_mean = bfi_10_e_mean,
                          bfi_10_o_mean = bfi_10_o_mean,
                          bfi_10_n_mean = bfi_10_n_mean,
                          nfc_kern_mean = nfc_kern_mean)




item_means <- apply(data[,13:114],FUN = mean,MARGIN = 2)

# Find out the items containing kern_

kern_items <- which(grepl("kern_",items$construct))

items_no_kern <- items[-kern_items,]
item_means_no_kern <- item_means[-kern_items]

# Prepeare the Prediction of the mean using difficulty with the construct label as a level 1 variable

item_means_no_kern <- data.frame(means=item_means_no_kern)
item_means_no_kern$construct <- items_no_kern$construct
item_means_no_kern$inverted <- items_no_kern$inverted %>% as.factor()
item_means_no_kern$difficulty <- items_no_kern$difficulty %>% as.factor()

item_means_no_kern$difficulty <- relevel(item_means_no_kern$difficulty,ref = "1")

items_no_kern$construct <- as.factor(item_means_no_kern$construct)

