import uvicorn
from fastapi import FastAPI, HTTPException
import numpy as np
import pandas as pd
import pickle
from pydantic import BaseModel
import difflib
import requests
import json
from fastapi.middleware.cors import CORSMiddleware

class Item(BaseModel):
    movie:str




app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
movie = "iron man"
res = []

new = pickle.load(open('new.pkl','rb'))
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


# function to recommend movies 

        
def recommend(movie_name):
    list_of_all_titles = movies['title'].tolist()
    find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
    close_match = find_close_match[0]
    if(len(find_close_match) == 0):
        return res
    index = new[new['title'] == close_match].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    print('Movies suggested for you : \n')
    res = []
    i = 1

    for i in distances[1:10]:
        movie_id = movies.iloc[i[0]].movie_id
        response = requests.get('https://api.themoviedb.org/3/movie/'+ str(movie_id) + '?api_key=0092ad3d52a414b557e84706ad391d41&language=en-US')
        data = response.json()
        if(response):
            res.append(data)
    return res

#fucntion to search movie in dataset

@app.get('/{movie}')

def get_movie(movie:str):        
    res = recommend(movie)
    pickle.dump(res,open("res.pkl","wb"))
    return {"successfull"}

@app.get('/items/predict')

def get_movie():
    res = pickle.load(open('res.pkl','rb'))
    return res

if __name__ == '__main__':
    uvicorn.run(app,host ='127.0.0.1',port = 5000)



