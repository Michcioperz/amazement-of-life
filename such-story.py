#!/usr/bin/env python3
import pycorpora, random

class SeriousRandom(object):
    def __init__(self, objs):
        self.objs = objs
        self.last = random.choice(self.objs)
    def __call__(self):
        ret = random.choice(self.objs)
        while ret == self.last: ret = random.choice(self.objs)
        self.last = ret
        return ret
    def __list__(self):
        return self.objs

talk_topics = SeriousRandom(pycorpora.humans.authors["authors"] + [x["name"] for x in pycorpora.humans.richpeople["richPeople"]] + pycorpora.humans.scientists["scientists"] + [x["title"]+" "+x["person"]["firstname"]+" "+x["person"]["lastname"] for x in pycorpora.humans.us_presidents["objects"]] + pycorpora.humans.wrestlers["wrestlers"] + pycorpora.humans.britishActors["britishActors"] + pycorpora.corporations.cars["cars"])

adjective_opinions = SeriousRandom(pycorpora.humans.moods["moods"])

noun_opinions = SeriousRandom(pycorpora.humans.occupations["occupations"]+pycorpora.animals.common["animals"]+pycorpora.animals.dinosaurs["dinosaurs"]+pycorpora.foods.fruits["fruits"]+pycorpora.foods.vegetables["vegetables"] + pycorpora.art.isms["isms"] + pycorpora.plants.flowers["flowers"] + [x.split(" ", 1)[1] for x in pycorpora.science.minor_planets["minor_planets"]])

places = SeriousRandom(pycorpora.architecture.passages["passages"] + pycorpora.architecture.rooms["rooms"])

quotes = pycorpora.words.oprah_quotes["oprahQuotes"] + [x["incantation"] for x in pycorpora.words.spells["spells"]]
for x in pycorpora.words.proverbs["proverbs"]:
    quotes.extend(list(x.values())[0])
for x in pycorpora.words.us_president_quotes["data"]:
    quotes.extend(x["quotes"])
quotes = SeriousRandom(quotes)

response_templates = SeriousRandom(["Such a %s %s.","Reminds me of a %s %s.","Isn't it a bit like %s %s?","Feels to me like %s %s."])

question_templates = SeriousRandom(["So what do you think about %s?", "What about %s?", "I'd like to know your opinions about %s, maybe."])

class Character(object):
    def __init__(self):
        self.first = random.choice((pycorpora.humans.firstNames if random.randrange(4) else pycorpora.humans.spanishFirstNames)["firstNames"])
        self.second = " "+random.choice((pycorpora.humans.firstNames if random.randrange(4) else pycorpora.humans.spanishFirstNames)["firstNames"])+" " if random.randrange(3) else " "
        self.last = random.choice((pycorpora.humans.lastNames if random.randrange(4) else pycorpora.humans.spanishLastNames)["lastNames"])
    def full_name(self): return self.first + self.second + self.last
    def __str__(self): return self.first

def main():
    characters = SeriousRandom([Character() for i in range(random.randrange(2,5))])
    ret = ", ".join([x.full_name() for x in characters.objs[:-1]])+" and "+characters.objs[-1].full_name()+" met up in the "+places()+" near the "+places()+" to discuss the amazement of life together.\n"
    while len(ret) < 50000:
        ret = ret + '\n"'+question_templates()%talk_topics()+'", said %s.'%characters()+"\n"
        for i in range(random.randrange(2, 3*len(characters.objs))):
            ret = ret + '\n"'+response_templates()%(adjective_opinions(), noun_opinions())+'", said %s.'%characters()+"\n"
    ret = ret + "\nAt which point they were too tired to continue, so they just plain fell asleep."
    return ret

if __name__ == "__main__":
    print(main())
