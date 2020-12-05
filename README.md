## About The Project

This is a simple secret santa script built with Python 3.

It randomly pairs up all participants, then sends each participant an email telling them who they got paired with.


## Installation

1. Clone the repo
   ```sh
   git clone git@github.com:Bwaits2/secret-santa.git
   ```


## Usage

1. Add your email username and password to the config file for smtp
2. Add all player names and emails, as well as bad pairs
3. Customize the email that will be sent to all players
4. Run the script
  ```sh
  python secretsanta.py
  ```


## Roadmap

Here is a list of features I am working on trying to add:
1. Command line flag to send or test
2. Command line help flag
3. Ability to force a match
4. Think of a smarter way to code the Parser class

Crazy and/or weird ideas:
1. Running the script bring up an interactable prompt with numbered options
2. Save or email a backup file with every pairing
