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
There once was a spirit named Yuzhen,
Who went oft to the peak of Taihua.                                        
At dawn she would strike a heavenly drum,                                                     
Soaring and prancing on twin dragons.

Struck by lightening, she still didn't stop,
Traveling through clouds, she left not a trace.                          
When she come to Mt. Shaoshi,
Who shall she meet but Wangmu (Queen Mother).
'''

