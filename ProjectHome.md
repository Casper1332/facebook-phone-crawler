This is a concurrent processing script that grabs either an input file of numbers or CLI arguments for a range of numbers and associates it to the user's supplied real name and fb id.

There is no rate limiting and it runs default an average of 1 match a second (a little less, but it's a good solid average). Speed ups could be made, possibly with keep-alive, definitely with multiple accounts and more processes.

**UPDATE: Dead! All it takes is proof and a day I guess.**

They first decided to throttle down, then they added some extra checks, now you must opt in to include your name in the phone lookup. Even other bypasses don't seem to work now. I do believe it has finally been fixed!


---


This was written in an hour for Suriya's bug that FB thinks is a feature.

  * Facebook needs to apply rate limiting.
  * There's no reason a name needs to be associated with non-friends when a search is made for a number. Just allow them to send a friend request and possibly see a picture.


---


TUTORIAL:

Like I said, this was a really quick write-up in some spare time. Please create an account, validate, and then find your cookies. When you have your cookies, place them into the "cookies" variable. I made this a variable in case you wanted to span users and for loop through them.
I might later add support for getting the cookies right into the script, but it's not straight forward static POST values like most sites, help is always welcome.


---


python facebook-hit.py -start 12818665050 -end 12818665100

  * Input size: 50	Chunk size: 5	Pool size: 10
  * Facebook number 12818665070 = ('Jx Px Px', '113711x')
  * Facebook number 12818665071 = ('Sx Mx', '100003176479x')
  * Facebook number 12818665052 = ('Kx SOMEBODY', '30406x')
  * Facebook number 12818665097 = ('Alex Vix', '100002x73148x')
  * Facebook number 12818665063 = ('Jx B Lox', '10000x684260x')
  * Facebook number 12818665058 = ('Chris Dx', '603911x')
  * Facebook number 12818665084 = ('Jose Rx', '100001611639x')
  * Facebook number 12818665099 = ('James Gx', '100000777456x')
  * Facebook number 12818665074 = ('Toni Sx', '100001686761x')
  * Facebook number 12818665100 = ('Paul Tx', '100002524536x')

Name and id's protected for public post in case someone decides to fix this.