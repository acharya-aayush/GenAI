def creating_sample_data():
    # Sample data for sentiment analysis
    reviews=[
        "This movie was great",
        "I love this film", 
        "Amazing story",
        "Best movie ever",
        "Excellent acting",
        
        "This movie is bad",
        "I hate this film",
        "Boring story", 
        "Worst movie ever",
        "Terrible acting"
    ]
    labels = [1,1,1,1,1,0,0,0,0,0]
    return reviews, labels

def displaydata():
    reviews, labels = creating_sample_data()
    
    print("Aileko lagi simple dataset: ")
    print("-"*30)
    
    for i in range(len(reviews)):
        sentiment="positive" if labels[i] == 1 else "negative"
        print(f"{i+1}. {reviews[i]} | Sentiment: {sentiment}")
        
displaydata()

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def training_bayesmodel():
    reviews, labels = creating_sample_data()
    #converting the words to numbers yo countvectorizer ley
    vectorizer = CountVectorizer() 
    
    # Convert text reviews to numerical features
    X = vectorizer.fit_transform(reviews)
    model = MultinomialNB()
    model.fit(X, labels)
    return model, vectorizer

def test(model,vectorizer,test):
    rvw_vctr = vectorizer.transform([test])
    prediction = model.predict(rvw_vctr)
    return "positive" if prediction[0] == 1 else "negative"