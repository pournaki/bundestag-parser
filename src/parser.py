def parser():

    def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
        # Print New Line on Complete
        if iteration == total: 
            print()
    
    import os
    import sys
    
    # load libraries
    import wikipediaapi 
    from lxml import etree
    import nested_lookup as nl
    import json
    from datetime import datetime

    datadir = "./data/speeches/"
    # get all the filenames in the directory
    filenamelist = []
    def absoluteFilePaths(datadir):
        for dirpath,_,filenames in os.walk(datadir):
            for f in filenames:
                filenamelist.append(os.path.join(dirpath, f))
        return filenamelist
    filenamelist = absoluteFilePaths(datadir)
    l = len(filenamelist)

    with open(f"./data/missing_metadata.json", 'r', encoding='utf-8') as json_file:
        missing_metadata = json.load(json_file)
    
    # initialise dict
    jsondict = {}

    # Initial call to print 0% progress
    printProgressBar(0, l, prefix = 'Parsing...', suffix = 'Complete', length = 50)
    
    # initialize wikipedia page in case a speaker is missing
    wiki_wiki = wikipediaapi.Wikipedia('de')

    # iterate over all filenames
    for progresso, filename in enumerate(filenamelist):
        
        # load the data
        parser = etree.XMLParser(dtd_validation=False)
        tree = etree.parse(filename, parser)
        root = tree.getroot()
        date = root.attrib.get('sitzung-datum')
        date = datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
        
        printProgressBar(progresso + 1, l, prefix = 'Parsing...', suffix = 'Complete', length = 50)
        
        # define the context
        context =  root.findall(".//sitzungsverlauf/tagesordnungspunkt")
    
        for elem in context:        

            # set the TOP-structure
            if elem.tag == 'tagesordnungspunkt':
                jsondict[f"{elem.attrib['top-id']} {date}"] = {}

            # add information same for all TOPs
            jsondict[f"{elem.attrib['top-id']} {date}"]["speeches"] = []
            
            # add the speeches
            for element in elem.getchildren():
                if element.tag == 'rede':
                    rededict = {}

                    # dive into the information of the speech:
            
                    text = ''
                    
                    for info in element.getchildren():
            
                        # get the policitian's name and party
                        if info.attrib == {'klasse': 'redner'}:

                            party = ''
                            name  = ''
                            surname = ''
                            
                            for p in info.getchildren()[0].getchildren()[0].getchildren():
                                if p.tag == 'fraktion':
                                    party += p.text
                                if p.tag == 'vorname':
                                    try:
                                        name  += p.text
                                    except TypeError:
                                        name += ''
                                if p.tag == 'nachname':
                                    surname += p.text

                            printname = name + " " + surname
                            
                            if party == '':
                                try:
                                    party += missing_metadata[printname]
                                except KeyError:
                                    print()
                                    print("Fatal error!")
                                    print(f"No party information about {printname} in the XMLs!") 
                                    print("Please add it to './data/missing_metadata.json' and restart the parser.")                                    
                                    page_py = wiki_wiki.page(printname)
                                    print("---")
                                    print("Here is the summary of their Wikipedia page:")
                                    print(page_py.summary)
                                    sys.exit()

                            rededict["id"] = element.attrib['id']
                            rededict["period"] = root.attrib.get('wahlperiode')
                            rededict["date"] = date
                            rededict["name"] = name + " " + surname
                            rededict["party"] = party

                        # now get the politician's speech
                        if (info.attrib == {'klasse': 'J'})  \
                        or (info.attrib == {'klasse': 'J_1'})\
                        or (info.attrib == {'klasse': 'O'}):
                            if type(info.text) is str:
                                text += info.text
                                text += ' '

                                # remove encoding errors
                                text = text.replace(u'\xa0', u' ') 
                                text = text.replace(u'\xad', u'')

                        # paste the text into the dict entry
                        rededict["text"] = text
                        
                    jsondict[f"{elem.attrib['top-id']} {date}"]["speeches"].append(rededict)

    parsed_speeches = jsondict
            
    for element in parsed_speeches:
        for speech in parsed_speeches[element]["speeches"]:
            speech["discussion_title"] = element

    flatdict = []
    for element in parsed_speeches:
        for speech in parsed_speeches[element]["speeches"]:
            flatdict.append(speech)

    for speeches in flatdict:
        speeches["text"] = speeches["text"].replace('"', '``').replace("'",'`')

        try:
            speeches["name"] = speeches["name"].replace('"', '``').replace("'",'`')
        except AttributeError:
            pass
    
    with open ("./speeches.jsonl", "w", encoding = "utf-8") as f:
        for line in flatdict:
            json.dump(line, f, ensure_ascii=False)
            f.write("\n")

    print("Success! Saved parsed speeches to './speeches.jsonl'.")

    return flatdict
