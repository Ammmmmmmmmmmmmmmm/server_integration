#GNU/Linux Factorio Command Integration

Run a server and send commands to the server from within the game chat feature!

##How it Works

By chatting a command in a game chat such as: 

```bash
[CHAT] Real_Laroy: ~back
```

The Python script that runs when the game starts will check the log every 2 seconds to see if there is a command an admin sent in there!

Once it has figured out if the admin has sent a command it will then find out what command it is and run bash scripts to manage the server!

##Follow Along

Usefull Video but don't write his bash scripts such as stop.sh and run.sh, just import my improved ones.
https://www.youtube.com/watch?v=EfG2Y6mayDY

In the video he shows changing alot of data files such as map-gen-settings.example.json

I recommend setting this up after you already know bin/64/factorio is working and is on the port you want.

##Steps to Use

Install the headless version of factorio on the website

Import all my files into your headless factorio folder

You will need to make make run.sh, stop.sh, and log_file_parser.py executable and own the entire server folder:

```bash
sudo chown (factorio server folder)
chmod +x ./log_file_parser
chmod +x ./stop.sh
chmod +x ./run.sh
```

In order to make yourself admin you will have to add your name to the server-adminlist.json file.