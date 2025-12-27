## v1
- client_id is now a string, not int
- before the client was generating the client id and telling it to server which is a security issue, so now server makes the client_id and never trust the sender_id sent by clinet .... its purely for showing purpose. the server over writes it
- earlier each client got its own endpoint sometihng like this ws/{client_id} but thats not the case anymore . there is only /ws
- improved the UI a LITTLE BIT
- made the self message stable
- made Server messages distinguished

### demo pics

![how did this fail...](images/v1_demo.png)

## v0
- right now, its pretty simple.
- frontend is just html cuz i am focusing on the websocket part rn
- when user enter, he is assigned a 3 digit intger called clinet_id . 
- each user gets a list of all the users online (excluding self) and backend sends updated list when someone new connects or disconnects
- users can type a message and select a reciepient from the dropdown . all (broadcast) or some specific user_id (dm type stuff)
- v(negative 1) was even trashier lol, it didnt have even option to dm or broadcast and the message was passed around in raw text . unlike now it is passed around as objects of a pydantic model .

"""
MESSAGE PROTOCOL (v0)

1. Broadcast message
{
  message_type: "broadcast",
  sender_id: string,
  reciever_id: null,
  message: string
}

2. Direct message (DM)
{
  message_type: "dm",
  sender_id: string,
  reciever_id: string,
  message: string
}

3. User list (system message)
{
  message_type: "user_list",
  sender_id: "server",
  reciever_id: null,
  message: JSON string of [user_id]
}

Rules:
- sender_id sent by client is ignored
- server overwrites sender_id
- client must not send user_list
"""


## WIP
- i am thinking of removing the clinet_id and introducing user_id, user_name and password alsong with signup and login. so people can actually know who are they texting to ....not some random number lol
