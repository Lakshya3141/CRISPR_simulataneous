library(readxl)
raw_data <- read_excel(path = "raw_mean_data.xlsx")
raw_data[['category']] <- 0
circ_list <- unique(raw_data$sample)
circ_list <- c("Heterogenous_offsite","Heterogenous_onsite",
               "Homogenous_offsite","Homogenous_onsite")
circ_ass <- c(2, 1, 4, 3)
for(i in seq(1,length(raw_data$category))){
  raw_data$category[i] <- circ_ass[which(circ_list==raw_data$sample[i])]
}
GFP_mean_data <- subset(raw_data, subset = fluo == "GFP")
RFP_mean_data <- subset(raw_data, subset = fluo != "GFP")
write.csv(GFP_mean_data, "GFP_data.csv")
write.csv(RFP_mean_data, "RFP_data.csv")
