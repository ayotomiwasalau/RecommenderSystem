import numpy as np
import pandas as pd
import recommender_functions as rf
import sys # can use sys to take command line arguments

class Recommender():
    '''
    A Recommender that recommends movie using FunkSVD by predicting the likely user movie rating, or recommends using Knowledge based recommendation(ranked/popular recommendation), but where a movie is provided by the user, Cnntent Based recommender would be used, it would provide similar movies as the one provided,
    '''
    def __init__(self ):
        '''
        what do we need to start out our recommender system
        '''



    def fit(self, reviews_pth, movies_pth, latent_features=5, iters=100, learning_rate = 0.001 ):#FunkSVD & Knowledge based
        '''
        fit the recommender to your dataset and also have this save the results
        to pull from when you need to make predictions
        
        This function performs matrix factorization using FunkSVD 
        
        INPUT:
        reviews_pth - path to csv with at least the four columns: 'user_id', 'movie_id'. 'rating', 'timestamp'
        movies_pth
        latent_features -  the number of latent  features used
        iters - the number of iterations
        learning_rate - the learning rate        
        
        OUTPUT:
        No Output - Stores the fllw attributes
        
        n_users - the number of users(int)
        n_movies - the number of movies(int)
        num_ratings - the number of ratings made
        reviews - dataframe with four columns: 'user_id', 'movie_id', 'rating', 'timestamp
        movies - dataframe of
        user_item_mat - (np arrays) a use by items numpy array with rating and nans for values
        Latent_features - the number of latent features used
        learning_rate - the learning rate
        iters - the number of iterations
        
        '''
        #Store inputs as attributes
        self.reviews = pd.read_csv(reviews_pth)
        self.movies = pd.read_csv(movies_pth)
        
        #Create user-item matrix
        usr_itm = self.reviews[['user_id', 'movie_id', 'rating', 'timestamp']]
        self.user_item_df = usr_itm.groupby(['user_id', 'movie_id'])['rating'].max().unstack()
        self.user_item_mat = np.array(self.user_item_df)
        
        #Store more inputs
        self.latent_features = latent_features
        self.learning_rate = learning_rate
        self.iters = iters
        
        #set up useful values to be used throught the rest of the function
        self.n_users = self.user_item_mat.shape[0]
        self.n_movies = self.user_item_mat.shape[0]
        self.num_ratings = np.count_nonzero(~np.isnan(self.user_item_mat))
        self.user_ids_series =np.array(self.user_item_df.index)
        self.movie_ids_series = np.array(self.user_item_df.columns)
        
        #initialize the user and movie matrices with random values
        user_mat = np.random.rand(self.n_users, self.latent_features)
        movie_mat = np.random.rand(self.latent_features, self.n_movies)
        
        #intialize sse at 0 for first iteration
        sse_accum = 0
        
        #keeping track of the iteration and MSE
        print('Optimization Statistics')
        print('Iterations | Mean Squared Error')
        
        #for each iteration
        for iteration in range(sellf.iters): 
            #update our sse
            old_sse  = see_accum
            see_accum = 0    
            #for each user-movie pair
            for i in range (self.n_users):
                for j in range(self.n_movies):
                    
                    #if  the rating exists
                    if self.user_item_mat[i, j] > 0:
                        
                        # compute the error as the actual minus the dot product of the user and movie latent features
                        diff = self.user_item_mat[i, j] - np.dot(user_mat[i, :], movie_mat[:, j])

                        # Keep track of the sum of squared errors for the matrix
                        sse_accum += diff**2

                        # update the values in each matrix in the direction of the gradient
                        for k in range(self.latent_features):
                            user_mat[i, k] += self.learning_rate * (2*diff*movie_mat[k, j])
                            movie_mat[k, j] += self.learning_rate * (2*diff*user_mat[i, k])
             # print results
        print("%d \t\t %f" % (iteration+1, sse_accum / self.num_ratings))
                
                   
        #svd based fit
        # Keep user_mat and movie-mat for safe keeping
        self.user_mat = user_mat
        self.movie_mat = movie_mat
        # Knowledge based fir
        self.ranked_movies = rf.create_ranked_df(self.movies, self.reviews)           
            

        

    def predict_rating(self, ):
        '''
        makes predictions of a rating for a user on a movie-user combo
        
        INPUT:
        user_id - the user_d from the reviews df
        movie_id - movie_id according to movies df
        
        OUTPUT:
        pred - the predicted rating for the user_id - movie_id according to FunkSVD
        '''
        try:
            user_row = np.where(self.user_ids_series == user_id)[0][0]
            movie_col = np.where(self.movie_ids_series == movie_id)[0][0]
            
            #Take dot product of theat row and column in the U and V to make prediction
            pred = np.dot(self.user_mat[user_row, :], self.movie_mat[:, movie_col])
            
            movie_name = str(self.movies[self.movies['movie_id'] == movie_id]['movie'])[5:]
            movie_name = movie_name.replace('\nName: movie, dtype: object', '')
            print("For user {} we predict a {} rating for the movie {}.".format(user_id, round(pred, 2), str(movie_name)))
            return pred
        
        except:
            print("I'm sorry, but a prediction cannot be made for this user-movie pair.  It looks like one of these items does not exist in our current database.")
            return None
            
    def make_recs(self, _id, _id_type = 'movie', rec_num = 5):
        '''
        given a user id or a movie that an individual likes
        make recommendations
        
        INPUT:
        _id - either a user or movie id (int)
        _id_type - "movie" or "user" (str)
        rec_num - number of recommendations to return (int)

        OUTPUT:
        recs - (array) a list or numpy array of recommended movies like the
                       given movie, or recs for a user_id given
        '''
        rec_ids, rec_names = None, None
        if _id_type == 'user':
            if _id in self.user_ids_series:
                # Get the index of which the row the user is in for use in the U matrix
                idx = np.where(self.user_ids_series == _id)[0][0]

                # take the dot product of that row and the V matrix
                preds = np.dot(self.user_mat[idx,:],self.movie_mat)

                # pull the top movies according to the prediction
                indices = preds.argsort()[-rec_num:][::-1] #indices
                rec_ids = self.movie_ids_series[indices]
                rec_names = rf.get_movie_names(rec_ids, self.movies)

            else:
                # if we don't have this user, give just top ratings back
                rec_names = rf.popular_recommendations(_id, rec_num, self.ranked_movies)
                print("Because this user wasn't in our database, we are giving back the top movie recommendations for all users.")

        # Find similar movies if it is a movie that is passed
        else:
            if _id in self.movie_ids_series:
                rec_names = list(rf.find_similar_movies(_id, self.movies))[:rec_num]
            else:
                print("That movie doesn't exist in our database.  Sorry, we don't have any recommendations for you.")

        return rec_ids, rec_names
                    
        
        
if __name__ == '__main__':
    # test different parts to make sure it works
    import recommender_template as r
    
    #instantiate recommender
    rec = r.Recommender()
    
    #fit recommender
    rec.fit(reviews_pth='data/train_data.csv', movies_pth= 'data/movies_clean.csv', learning_rate=.01, iters=1)
    
    #predict 
    rec.predict_rating(user_id =8, movie_id = 2844)
    
    #make recommendations
    print(rec.make_recommedations(8, 'user'))
