# Disaster Response Pipeline Project

### Installing

Clone this GIT repository:

```
git clone https://github.com/usamnet000/Disaster-Response-Pipeline-Project
```

### Background

Following a disaster, there are a number of different problems that may arise. Different types of disaster response organizations take care of different parts of the disasters and observe messages to understand the needs of the situation. They have the least capacity to filter out messages during a large disaster, so predictive modeling can help classify different messages more efficiently.

In this project, I built an ETL pipeline that cleaned messages using regex and NLTK. The text data was trained on a multioutput classifier model using random forest. The final deliverable is Flask app that classifies input messages and shows visualizations of key statistics of the dataset.

The random forest classifier model and The use of algorithm AdaBoostClassifier improves accuracy by
scored 92.75% accuracy, 98% precision, 78% recall, and 89.11% F-1 score after tuning the parameters using GridSearchCV.

> **note**
> The process takes a lot of time with the addition of a parameter so the results are very close
> The addition of the parameter was ignored at the present time, but the parameter could have been added and if you added the parameter to improve the performance of the model, but unfortunately a device takes a long time to complete this process

### Files

- `process_data.py` : ETL script to clean data into proper format by splitting up categories and making new columns for each as target variables.
- `train_classifier.py` : Script to tokenize messages from clean data and create new columns through feature engineering. The data with new features are trained with a ML pipeline and pickled.
- `run.py` : Main file to run Flask app that classifies messages based on the model and shows data visualizations.

### Instructions

1. Run the following commands in the project's root directory to set up your database and model.

   - To run ETL pipeline that cleans data and stores in database
     `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/disaster_message_categories.db`
   - To run ML pipeline that trains classifier and saves
     `python models/train_classifier.py data/disaster_message_categories.db models/model.p`

2. Run the following command in the app's directory to run your web app.
   `python run.py`

3. Go to http://127.0.0.1:3001/

## License

MIT © [usamnet000](https://github.com/usamnet000)
