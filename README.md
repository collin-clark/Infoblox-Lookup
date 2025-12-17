A simple webapp the queries your local Infoblox Grid Master to get information about a host or network. It will show all the containers the host/network is in from least to most specific. It will also show the DNS record type(s) for the host if any exist outside of A or AAAA.

# Installation

Either clone this repo into your Flask server or search packetpros\infoblox-lookup on Docker Hub.
Which ever way you choose you will need to create a .env file to set the credentials, URL and WAPI version. There is an example in the repo.

<img width="800" height="471" alt="infoblox_lookup" src="https://github.com/user-attachments/assets/e084eba3-7f6f-417a-989c-111c89208a64" />
