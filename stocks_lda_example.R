require(ISLR)
require(MASS)

train <- subset(Smarket, Year < 2005)
test <- subset(Smarket, Year == 2005)
lda.fit <- lda(Direction ~ Lag1 + Lag2, data = train)
plot(lda.fit)
lda.pred <- data.frame(predict(lda.fit, test))
table(lda.pred$class, test$Direction)
mean(lda.pred$class == test$Direction) #Accuracy rate
