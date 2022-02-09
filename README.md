# Overview

## NetworkingGame

I want to learn about networking, so I'm going to build a game where two players can interact over a network.

This program provides the framework for a game where multiple client programs on the same or different computers can interact with each other via the server program. The game is simple for now: you move the character on one screen, and the change in location will be reflected on all the client's screens!

#### How to use

1. You will need to add a firewall rule to each computer running this program. It will need to allow access in and out through port 20001.

2. Decide which computer will be running the server, and find its public IP address. Generally, that can be found by running "ip a" on linux or "ipconfig" on Windows. The IP address you're looking for will probably not start with 198.162.?.?

3. Add the server machine's IP address to the constants.py file down at the bottom. Put it between the double quotes on the line that says SERVER_ACCESS_PORT = ("", 20001). Make sure this change is made to the constants.py file on both the client machine(s) and the server machine.

4. You may need to connect all participating computers to the same network. I tried this on three different networks and two of them just plain refused connections between my laptops.

5. Run server.py

6. Run as many client.py programs as you'd like. I currently only have 7 different colors of character, and haven't tested it with more than that, but it's set up to loop through the colors so you should be able to have unlimited players (as long as your server machine and router can support that much traffic!).

7. Use the arrow keys to move your character around on the client windows. There's currently no goal, but you can move around!

#### Video Overview

This video provides a demonstration and walks through the code as of 2/6/2022.

[Demo Video](https://youtu.be/lFiUlTi1qhM)

## Network Communication

For this project I used a client/server architecture so that multiple clients can connect to the same server. It uses UDP on port 20001.

There are two types of information sent across the connection. The first is a pickled object containing the user's character color (or name) and location. Whenever the server receives a pickled object of that type, it rebroadcasts the list of character locations it has to all connected clients.

The second type of information is a simple string that says "Name Requested". This signifies to the server that this client is connecting for the first time, needs the next color available, and needs to be added to the server's list of clients for future updates.

## Development Environment

I'm using Python 3.8.7 and several of its libraries to bring this project to life.
 - The built-in pathlib, threading, pickle, and socket libraries.
 - arcade 2.5.5

Aside from that, I also used GIMP to create the player graphics.

## Useful websites:

Used for the example client and example server in python:

https://pythontic.com/modules/socket/udp-client-server-example

Used for general question researching:

https://stackoverflow.com/

## Future Work

#### Completed:

Set up a server and a client
Send information back and forth
Abstract the waiting-on-server to a thread
Send objects back and forth
Create player graphics
Move from localhost to an actual wifi network

#### To Do:
Move from wifi network to across wifi networks
Add purpose to the game (fight other players? race them?)
Add more player actions
Make it more intuitive by having the server check its own public IP address, binding to that, and then displaying to to the screen so that the clients can enter it while running instead of editing a file.
