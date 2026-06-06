# Recommender System

The project entails building a recommender system that suggests movies to its users.

The system uses three scenerios to make recommendation

 - where the user does not provide information about movie preference, it recommends using Knowledge based recommendation, that is based on ranked/popular movie recommendations.

- where a movie is provided by the user, Content Based recommender system would be used, it would provide similar movies as the one provided.

- where the system has information about the user previous movie rating, it recommends movie using FunkSVD (matrix factorization) by predicting the likely user movie rating.

## Dependencies
The project was built using basic python libraries; 
- numpy 
- pandas.
and the FunkSVD model for prediction.

Recommendation systems have to be very fine tuned for effectiveness, so using third party apis might not give the desired output.
Hence a custom recommender system gives more relevant results
