#sAutomation of IRR using package irr

#set working directory for where you have this script and your data file saved

dir<-"C:/Users/ailbhe/Automation-InterRater-Reliability"
setwd(dir)


#install packages required to run the script - may take a few minutes to install
install.packages('irr')
install.packages('data.table')
install.packages('plyr')
install.packages('dplyr')
install.packages('reshape2')
install.packages('splitstackshape')
install.packages('tidyverse')


#load the installed packages to your workspace
library(irr)
library(data.table)
library(plyr)
library(dplyr)
library(reshape2)
library(splitstackshape)
library(tidyverse)

#load the data from your working directory
DataFile<-read.csv("IrrSpreadsheetBinary.csv", header = TRUE,sep = ",")
DataFile<-na.omit(DataFile)
 
head(DataFile, n=5)
names(DataFile)

#restructure dataframe
DataFile_Attributes<-DataFile[,c((4),(2:3),(6:7))]
head(DataFile_Attributes, n=5)

#make sure the number of papers and entites are correct - they should match the ontoloy and the set of papers annotated
NumPapers<-unique(DataFile_Attributes$shortTitle)
NumEntities<-unique(DataFile_Attributes$AttributeTitle)
length(NumPapers)
length(NumEntities)

#creates a list of each attribute and gives a count of the number of times it has been coded
AttributeCount<-ddply(DataFile_Attributes, "AttributeTitle", numcolwise(sum))

#subset attributes that have data and those that have no data for coder 1 and coder 2
HasData<-as.data.frame(AttributeCount[ which(AttributeCount$Coder1Text > 0 | AttributeCount$Coder2Text > 0), ])
HasNoData<-as.data.frame(AttributeCount[ which(AttributeCount$Coder1Text == 0 & AttributeCount$Coder2Text == 0), ])

length(unique(HasData$AttributeTitle))
print(HasData)

#subset the original data using only the entities which have data present
NewData<-match_df(DataFile_Attributes, HasData, on = "AttributeTitle")

#order the dataset by the attribute title then the paper author
NewData<-NewData[order(NewData$AttributeTitle, NewData$shortTitle),]

#calculate krippendorfs alpha on the entire dataset with all entites
All_Attributes<-t(DataFile_Attributes[,4:5])
Result<-kripp.alpha(All_Attributes, method = c("ordinal"))
Statistic<-as.character("All Entities")
Value<-as.numeric(Result$value)
All_Data_Result<-data.frame(Statistic,Value)
print(All_Data_Result)


#calculate krippendorfs alpha on the dataset with entities with data
Attributes_with_Data<-t(NewData[,4:5])
Result<-kripp.alpha(Attributes_with_Data, method = c("ordinal"))
Statistic<-as.character("Entities with data")
Value<-as.numeric(Result$value)
Attribute_Result<-data.frame(Statistic,Value)
print(Attribute_Result)

#calculate krippendorf's alpha on the individual entities with data

all_results <- data.frame() 

for (attributetitle in unique(NewData$AttributeTitle)) {
  
  temp_data = NewData[NewData$AttributeTitle==attributetitle,]
  temp_data$Coder1Text<-as.numeric(temp_data$Coder1Text)
  temp_data$Coder2Text<-as.numeric(temp_data$Coder2Text)
  
  temp_data2<-t(temp_data[4:5])
  
  result<-kripp.alpha(temp_data2, method = c("ordinal"))
  value<-as.numeric(result$value)
  
  new_data_frame = data.frame(AttributeTitle=attributetitle,Result=value)
  
  all_results <- rbind(all_results,new_data_frame)
  
}

WholeSample<-rbind(All_Data_Result, Attribute_Result)
names(WholeSample) <- c("AttributeTitle", "Result")


AllResults <-rbind(all_results, WholeSample) 
head(AllResults, n=10)

write.csv(AllResults, "IRR_RScript_Results.csv")

