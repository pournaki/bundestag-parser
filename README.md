# Bundestag Parser

## Description
A parser that transforms XMLs from the 19th election period* of [Deutscher Bundestag](https://www.bundestag.de/services/opendata) to a list of JSONs. The speeches are saved in `./speeches.jsonl`. Every line consists of one speech dictionary. See [sample output](#sample-output) for more information. 


*2017/10/24 until today

## How to use
Clone and enter this repo:
``` 
$ git clone https://github.com/pournaki/bundestag-parser
$ cd bundestag-parser
```

Install the necessary libraries: 

``` 
$ pip3 install -r requirements.txt
```

Run the parser: 
```
$ python3 run.py
```

## Sample output

```
{
  "id": "ID192100100",
  "period": "19",
  "party": "CDU/CSU",
  "name": "Peter Tauber",
  "date": "2018-03-16",
  "text": "Herr Präsident! Meine sehr verehrten Damen! Meine Herren! Liebe Kolleginnen und Kollegen! Das Mittelmeer ist eines der meistbefahrenen Seegebiete der Welt. Rund ein Drittel aller über See verschifften Güter und ein Viertel aller Öltransporte werden durch das Mittelmeer geleitet. In Zeiten der Globalisierung und des freien Handels ist die sichere Nutzung des Mittelmeeres auch im deutschen Interesse. Ferner ist das Mittelmeer Europas Südgrenze und zugleich seine maritime Brücke zur nordafrikanischen Gegenküste...",
  "discussion_title": "Tagesordnungspunkt 18 2018-03-16"
 }
```

## Known issues
- Sometimes, the party information of a speaker is missing in the XML files. When this happens, the parser crashes and asks you to input the missing party information to `./data/missing_metadata.json`. To ease this process, the parser kindly outputs the speaker's Wikipedia page.

- To the best of my knowledge, there is no automatic way of downloading the latest speech XMLs. Therefore, the updating has to be done manually.

- The specific title of the "Tagesordnungspunkte" cannot be retrieved at the moment, which is why the date is added as a reference. 
