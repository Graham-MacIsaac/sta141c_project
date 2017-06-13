## ----setup, include=FALSE------------------------------------------------
# knitr::opts_chunk$set(echo = TRUE, 
#                       message = FALSE,
#                       comment = NA,
#                       cache = TRUE
#                      )

## ----lib-----------------------------------------------------------------
# library(pander)
# library(h5)

## ------------------------------------------------------------------------
# crime_file <- h5file("crime.h5")
# crime_file["table"]

## ------------------------------------------------------------------------
# crime <- read.csv("miniPoliceZipNum.csv", header = TRUE)
crime <- read.csv("policeZipNum.csv", header = TRUE)

crime$zipcode <- as.factor(crime$zipcode)

## ------------------------------------------------------------------------
# Idea from https://stackoverflow.com/questions/17200114/how-to-split-data-into-training-testing-sets-using-sample-function-in-r-program

# The proportion to use for training data
train_prop <- 0.8

train_size <- floor(train_prop * nrow(crime))

set.seed(42)
train_ind <- sample(1:nrow(crime), size = train_size)

crime_train <- crime[train_ind, ]
crime_test <- crime[-train_ind, ]


## ------------------------------------------------------------------------
# numfolds <- 100
# 
# assertthat::are_equal(0, nrow(crime) %% numfolds)
# 
# crime_shuffled <- crime[sample(nrow(crime), replace = FALSE),]
# 
# 
# sapply(1:numfolds, function(i) {
#   
# })


## ------------------------------------------------------------------------
# How to use for multi-class prediction?
# logit.model =  glm(formula = CategoryNumber ~ PdDistrictNum + DayOfWeek, 
#                    family = binomial(logit), 
#                    data = crime_train)

## ------------------------------------------------------------------------
action.model =  glm(formula = action_taken ~ CategoryNumber + PdDistrictNum + zipcode, # + DayOfWeek
                    family = binomial(logit), 
                    data = crime_train)
action.model

## ------------------------------------------------------------------------
crime_predicted <- predict(action.model, newdata = crime_test, type = "response")

# Consider a prediction of a probability > 0.5 of an action being taken 
# as a prediction of an action being taken.  
crime_predicted_bin <- crime_predicted > 0.5

# class(crime_predicted_bin[1])
# class(crime_test$action_taken[1])

prediciton_accuracy <- mean(crime_predicted_bin == as.logical(crime_test$action_taken))

paste("Prediction accuracy: ", prediciton_accuracy)


