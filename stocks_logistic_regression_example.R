require(ISLR)
names(Smarket)
summary(Smarket)

#Model 1
glm.fit <- glm(Direction ~ .-Year-Today, data = Smarket, family = binomial)
summary(glm.fit)
glm.probs <- predict(glm.fit, type = 'response')
glm.pred <- ifelse(glm.probs > .5, "Up", "Down")
table(glm.pred, Smarket$Direction)
mean(glm.pred == Smarket$Direction) #Correct prediction rate

#Model 2
#Split into training and test sets
train = Smarket$Year < 2005
summary(glm.fit)
glm.fit = glm(Direction ~ .-Year-Today, data = Smarket, family = binomial, subset = train)
glm.probs = predict(glm.fit, newdata = Smarket[!train, ], type = 'response')
glm.pred = ifelse(glm.probs > .5, 'Up', 'Down')
table(Smarket$Direction[!train], glm.pred)
mean(Smarket$Direction[!train] == glm.pred) #Correct prediction rate

#Model 3
#Simpler model with only two predictors
glm.fit = glm(Direction ~ Lag1 + Lag2, data = Smarket, family = binomial, subset = train)
summary(glm.fit)
glm.probs = predict(glm.fit, newdata = Smarket[!train, ], type = 'response')
glm.pred = ifelse(glm.probs > .5, 'Up', 'Down')
table(Smarket$Direction[!train], glm.pred)
mean(Smarket$Direction[!train] == glm.pred) #Correct prediction rate
