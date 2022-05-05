import joblib 
import os

model_path = os.path.abspath(os.path.split(__file__)[0] + "/models/emotion_classifier_pipe.pkl")
pipe = joblib.load(open(model_path,"rb"))

def predict_emo(text):
	classes = pipe.classes_
	results = pipe.predict_proba([text])
	results_dict = dict()
	for index in range(len(classes)):
		results_dict[classes[index]] = results[0][index]
	return results_dict

def test():
	mockup = "I'm going to list where I'm looking..I, we have the original wipe material..Go to the ancient seven seas to read the different shovel..Limp soup.News man and therefore today.Jiagao City Night Chef T.There is no discount..Yu Caiyang association"
	predict_emo(mockup)