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

testing = '''
        Silent spring is to cherish the fine flow of water, the shade of trees according to the water is soft and sunny.
        The little tender lotus had just revealed the tightly wrapped tip of the leaf, and the lovely dragonfly stood on it.
'''

