INSTALLATION

git clone https://github.com/osamaliaqat/creditSuisse_task.git

pip install requirements.txt

run app.py

I have used JWT(json web token) just for the user identity purpose .

API Endpoints :

1. Create the User :
http://127.0.0.1:5000/create_user
Parameters required : email , name , password

2. Create the post :
http://127.0.0.1:5000/create_post
Parameters required : post_description

3. Get All Posts :
http://127.0.0.1:5000/allposts

4. Update the post :
http://127.0.0.1:5000/update_post
Parameters required : id , post_description
