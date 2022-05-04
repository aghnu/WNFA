import joblib 
# pipe = joblib.load(open("./models/emotion_classifier_pipe.pkl","rb"))

def predict_emo(text):
	classes = pipe.classes_
	results = pipe.predict_proba([text])
	results_dict = dict()
	for index in range(len(classes)):
		results_dict[classes[index]] = results[0][index]
	return results_dict