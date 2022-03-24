# creditsuisse_task

INSTALLATION

git clone https://github.com/osamaliaqat/creditsuisse_task.git

pip install requirements.txt

run app.py

I have used JWT(json web token) just for the user identity purpose .

API Endpoints :

Create the User.
http://127.0.0.1:5000/create_user
Parameters required : email , name , password

Create the post .
http://127.0.0.1:5000/create_post
Parameters required : post_description


Get All Posts
http://127.0.0.1:5000/allposts

Update the post .
http://127.0.0.1:5000/update_post
Parameters required : id , post_description
