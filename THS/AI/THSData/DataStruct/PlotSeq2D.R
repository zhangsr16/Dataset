library(writexl)
library(openxlsx)
library(tidyr)
library(abind)
library(stringr)
library(ggplot2)

#Type
dayCols=2:5
dayRowLen=12
#Summary
dayCols=2:6
dayRowLen=8
#Area
dayCols=3:7
dayRowLen=34
#Field
dayCols=4:9
dayRowLen=20

###Field
dayLayers=10
dayColLen=length(dayCols)
setwd("F:/Desktop/THS/AI/THSData/DataStruct/XLSX/Type/Months")
list_name = dir("./",pattern = ".xlsx") 
list_nameLen=length(list_name)

for (i in 1:dayLayers) {
  dayData=read.xlsx(list_name[list_nameLen-dayLayers+i], startRow = 1, sheet=1) #skip header rows
  dayMatrix=as.matrix(dayData[,dayCols])
  if (i==1){
    dayMatrix3d <- abind(dayMatrix, along = 3)
  }else{
    dayMatrix3d <- abind(dayMatrix3d, dayMatrix, along = 3)
  }
}
for (i in 1:(dayLayers-1)) {
  dayD=dayMatrix3d[,,i+1]-dayMatrix3d[,,i]
  for (j in 1:dayColLen) {
    ctr=scale(dayD[,j])
    dayD[,j]=ctr[,1]
  }
  if (i==1){
    DMatrix3d <- abind(dayD, along = 3)
  }else{
    DMatrix3d <- abind(DMatrix3d, dayD, along = 3)
  }
}
ylimMin=min(DMatrix3d, na.rm = TRUE)
ylimMax=max(DMatrix3d, na.rm = TRUE)

tempx=1:(dayLayers-1)
plot(tempx, DMatrix3d[1,1,], ylim = c(ylimMin,ylimMax), type='b', col=1, lty=1, pch=1)
for (i in 1:dayColLen) {
  for (j in 1:dayRowLen) {
    points(tempx, DMatrix3d[j,i,], ylim = c(ylimMin,ylimMax), type='b', col=j, lty=i, pch=i)
  }
}


##########聚类分析
dayDK=as.data.frame(dayD)
kmeans_result <- kmeans(dayDK, centers = 4)

# 将聚类结果添加为数据框的一列
dayDK$Cluster <- as.factor(kmeans_result$cluster)

# 绘制聚类结果
# Type
ggplot(dayDK, aes(x = dayDK[,1], y = dayDK[,2], color = Cluster)) +
  geom_point(size = 3) +
  geom_text(aes(label = Cluster), vjust = -1, hjust = 1, size = 3) +
  labs(title = "K-Means Clustering", x = "Feature1", y = "Feature2") +
  theme_minimal()
