# Auction Fetcher
Python app that allows you to monitor auction sites for items that you are interested in.

Note: this is still in development and is still in its baby feet. It does not work yet and the architecture might (will) change over time...

I will (try to) update this README as the project progresses.

These are the things I want this app to do:
  - you can specify which item you are interested in, and which auction sites (ebay, 2dehands.be, ...) should be monitored
	- Example: I want to monitor ebay.be & 2dehands.be for playstation 4 consoles

 - you can also specify options, e.g:
	- I want to monitor 2dehands.be for playstation 4's that cost between 200 & 300 euro.

 - you can specify which action to take if an item was found matching your query:
	- mail you with an excerpt of the auction item
	- automatically mail the owner of the bid
	- ...

Now every auction site has to be crawled for info differently, hence I abstract this in a driver for an auction site.
The idea is that when you want to support a new auction site for which I (or someone else) have not added support yet, all you have to do is implement a driver. 

The app (might) contain the following blocks:
 - configuration engine: 
	- allows you set up queries & actuators with various settings (duty cycle of queries, options, ...)

 - query engine:
	- takes care of querying the data using drivers for auction sites

 - actuators:
 	- bound to a query, these specify the actions to take based on the output of the query engine.
	- e.g mail you, mail the owner of the item, ...

