require(class)

lag1_lag2 <- cbind(Smarket$Lag1, Smarket$Lag2)
train <- Smarket$Year < 2005
test <- Smarket$Year == 2005
knn.pred <- knn(lag1_lag2[train, ], lag1_lag2[test, ], Smarket$Direction[train], k=1)
table(knn.pred, Smarket$Direction[test])
mean(knn.pred == Smarket$Direction[test])
 