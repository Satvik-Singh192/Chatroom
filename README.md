## v0
- right now, its pretty simple.
- frontend is just html cuz i am focusing on the websocket part rn
- when user enter, he is assigned a 3 digit intger called clinet_id . 
- each user gets a list of all the users online (excluding self) and backend sends updated list when someone new connects or disconnects
- users can type a message and select a reciepient from the dropdown . all (broadcast) or some specific user_id (dm type stuff)
- v(negative 1) was even trashier lol, it didnt have even option to dm or broadcast and the message was passed around in raw text . unlike now it is passed around as objects of a pydantic model .


## WIP
- i am thinking of removing the clinet_id and introducing user_id, user_name and password alsong with signup and login. so people can actually know who are they texting to ....not some random number lol
