from random import randrange
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "My friends", "content": "I do not have a lot of friends", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1_000_000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #delete post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    post_dic = post.model_dump()
    post_dic['id'] = id
    my_posts[index] = post_dic
    return {"data": post_dic}

