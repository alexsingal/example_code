require(ISLR)
require(boot)
plot(mpg ~ horsepower, data = Auto)
glm.fit <- glm(mpg ~ horsepower, data = Auto)

loocv <- function(fit){
  h = lm.influence(fit)$h
  return(mean((residuals(fit)/(1-h))^2))
}

cv.error <- rep(0, 10)
degree <- 1:10

for (d in degree){
  glm.fit <- glm(mpg ~ poly(horsepower, d), data = Auto)
  cv.error[d] <- loocv(glm.fit)
}

plot(degree, cv.error, type = "b")

cv.error10 <- rep(0, 10)
for (d in degree){
  glm.fit <- glm(mpg ~ poly(horsepower, d), data = Auto)
  cv.error10[d] <- cv.glm(Auto,glm.fit, K=10)$delta[1]
}
