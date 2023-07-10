import pickle
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Loading dataset
dataset = pickle.load(open("./data.pickle", "rb"))
data = np.asarray(dataset["data"])
labels = np.asarray(dataset["labels"])


# Splitting information into training and testing data from dataset
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, shuffle=True, stratify=labels
)

# Chosing our training model
model = RandomForestClassifier()

# Applying our train data to the model
model.fit(x_train, y_train)

# Getting a prediction with the test data
y_predict = model.predict(x_test)

# Getting an accuracy score for our model
score = accuracy_score(y_predict, y_test)

print("The score of our samples is {}%.".format(score * 100))

# Saving the model to our dir
f = open("model.p", "wb")
pickle.dump({"model": model}, f)
f.close()
