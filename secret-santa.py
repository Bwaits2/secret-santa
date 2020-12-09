import configparser
import smtplib
import random
import argparse

class Game():
    def __init__(self, santas, all_bad_matches):
        self.send = False
        self.santas = []
        self.players = santas
        self.all_bad_matches = all_bad_matches

    def start(self):
        self.clear()

        print("Computing valid matches")

        for player in self.players:
            player = player.split()
            name, email = player[0], player[1]

            self.build_santas(self.all_bad_matches, name, email)

        recievers = self.santas.copy()

        return Match.create_matches(self.santas, recievers)

    def build_santas(self, all_bad_matches, name, email):
        bad_matches = []
        for match in all_bad_matches:
            match = match.split(", ")
            if name in match:
                for person in match:
                    if name != person:
                        bad_matches.append(person)

        s = Santa(name, email, bad_matches)
        self.santas.append(s)

    def clear(self):
        self.santas = []


class Santa():
    def __init__(self, name, email, bad_matches):
        self.name = name
        self.email = email
        self.bad_matches = bad_matches


class Match():
    def __init__(self, santa, santee):
        self.santa = santa
        self.santee = santee

    @staticmethod
    def create_matches(santas, santees):
        aas = santas.copy()
        ees = santees.copy()

        matches = []
        try:
            for a in aas:
                ee = Match.select_santee(a, ees)
                ees.remove(ee)
                matches.append(Match(a, ee))
        except:
            return Match.create_matches(santas, santees)

        return matches

    @staticmethod
    def select_santee(santa, santees):
        rand = random.choice(santees)

        if santa.name == rand.name or santa.name in rand.bad_matches:
            if len(santees) < 2:
                raise Exception("need a redo")
            else:
                return Match.select_santee(santa, santees)

        return rand

    @staticmethod
    def printAll(matches):
        for match in matches:
            print(match)

    def __str__(self):
        return "  " + self.santa.name + " -> " + self.santee.name


class SMTP():
    def __init__(self, info):
        self.server = info[0]
        self.port = info[1]
        self.username = info[2]
        self.password = info[3]

        print("Logging in to SMTP")

        self.connect()
        self.login()

        print("Connected to SMTP")

    def connect(self):
        self.connection = smtplib.SMTP_SSL(self.server, self.port)
        self.connection.ehlo()

    def login(self):
        self.connection.login(self.username, self.password)

    def sendmail(self, match, email):
        s = self.username
        r = match.santa.email
        m = email.format(santa = match.santa.name,
                         email = r,
                         santee = match.santee.name)

        print("Sending email to "
                + match.santa.name + " at " + match.santa.email)

        self.connection.sendmail(s, r, m)


class Parser():
    def __init__(self, filename):
        self.config = configparser.RawConfigParser()
        self.config.read(filename)

        game = self.config['GAME']
        self.players = game['PLAYERS'].strip().splitlines()
        self.all_bad_matches = game['BADMATCHES'].strip().splitlines()

        smtp = self.config['SMTP']
        self.smtp_info = [smtp['SERVER'],
                            smtp['PORT'],
                            smtp['USERNAME'],
                            smtp['PASSWORD']]

        email = self.config['EMAIL']
        self.email = ('Subject: '+ email['SUBJECT']
                        + '\nTo: '  + '{email}\n' + email['BODY'])


class ArgParser():
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.add_arguments()
        self.args = self.parser.parse_args()

    def add_arguments(self):
        self.parser.add_argument('-s',
                                '--send',
                                action='store_true',
                                help='login to smtp and send all emails')


def main():
    send = ArgParser().args.send

    iniParser = Parser('config.ini')
    game = Game(iniParser.players, iniParser.all_bad_matches)

    matches = game.start()

    if send:
        smtp = SMTP(iniParser.smtp_info)

        for match in matches:
            smtp.sendmail(match, iniParser.email)
    else:
        print("\nHere is an example of the matches computed:")
        Match.printAll(matches)
        print("Use the '-s' flag to run again and send all emails")


if __name__ == "__main__":
    main()
