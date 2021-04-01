## About The Project

This is a simple secret santa script built with Python 3.

It randomly pairs up all participants, then sends each participant an email telling them who they got paired with.


## Requirements
All modules used are included in the python standard library.

Python >= 3.2 is required.


## Installation

1. Clone the repo
   ```sh
   git clone git@github.com:brendenwaits/secret-santa.git
   ```


## Usage

1. Add your email username and password to the config file for smtp
2. Add all player names and emails, as well as bad pairs
3. Customize the email that will be sent to all players
4. To test matching, run the script like so
   ```sh
   python secret-santa.py
   ```
5. To run the script and send emails to all participants with their match
   ```sh
   python secret-santa.py -s
   ```


## Roadmap

Here is a list of features I am working on trying to add:
1. Ability to force a match
2. Integration testing script
3. Determine the logistics of ensuring all matches are in big circle
4. An efficient way to determine if correct matches will be possible to compute

Crazy and/or weird ideas:
1. Running the script bring up an interactable prompt with numbered options
2. Save or email a backup file with every pairing
