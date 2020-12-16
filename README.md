# TEXbook Project
College education does not go without books. Too often, we find our textbooks and reference books come at a price too high. This platform encourages NYU Shanghai students to sell and rent used hard copies to fellow students. 
## Running

First fork the repo then do a `git clone`.

    git clone https://github.com/<yournamehere>/Robertation256/TEXbook

    pip freeze > requirements.txt

Once you have all of that, you should set up Redis and MySQL Database on your local machine.
Create a table called TEXbook and RUN:
  
    mysql -u root -p TEXbook < DB.sql

Finally, to run the project
```
python3 run.py
```

The site will be available to you at `localhost:127.0.0.1:5000`.

If you have dependency questions, reach out to the author at @yz3919@nyu.edu

## How it works

The user registers on the web application through their associated NYU email address. The email is verified and the user is allowed to set up a profile.
Afterwards, the user can list textbooks, view buyer requests and contact fellow students to sell or purchase textbooks.
