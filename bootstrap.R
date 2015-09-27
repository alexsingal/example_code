require(boot)

alpha <- function(x, y){
  vx = var(x)
  vy = var(y)
  cxy <- cov(x,y)
  return((vy-cxy)/(vx+vy-2*cxy))
}
x <- runif(n = 100, min = 0, max = 100)
y <- runif(n = 100, min = 0, max = 100)
df <- data.frame(x, y)
alpha(df$x, df$y)

alpha.fn <- function(data, index){
  with(data[index, ], alpha(x, y))
}

alpha.fn(df, 1:100)

alpha.fn(df, sample(x = 1:100, size = 100, replace = TRUE))

boot.out <- boot(df, alpha.fn, R=1000)
boot.out
plot(boot.out)

