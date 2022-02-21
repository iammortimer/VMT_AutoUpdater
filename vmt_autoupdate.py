import time
import Config as config

from AVAXAPI import AvalancheAPI

avapi = AvalancheAPI()

tycoonids = avapi.getTycoonIds()

if len(tycoonids) == 0:
    print("No tycoons found on address, exiting.")
    exit()

dolla = avapi.get_token_holdings(config.DOLLA_CONTRACT_ADRESS)
symbol, decimals = avapi.get_token_info(config.DOLLA_CONTRACT_ADRESS)
print(f'We have {dolla/(10**decimals)} {symbol}')

while True:
    #get tycoon info
    myTycoons = []

    for tid in tycoonids:
        mytycoon = avapi.getTycoonInfo(tid)
        forNxtLvl = avapi.getLevelInfo(mytycoon[0]) - mytycoon[3]
        tycoon = {
            "tid" : tid,
            "level" : mytycoon[0],
            "sinceTs" : mytycoon[1],
            "lastSkippedTs": mytycoon[2],
            "dollaAmount" : mytycoon[3],
            "cooldownTs": mytycoon[4],
            "reqDollaForNxtLvl" : forNxtLvl*(10**decimals)
        }
        myTycoons.append(tycoon)

    calcDolla = avapi.get_token_holdings(config.DOLLA_CONTRACT_ADRESS)
    waituntil = 0
    for tycoon in myTycoons:
        
        print("Processing Tycoon #" + str(tycoon['tid']))
        doUpgrade = False
        doWait = True
        #add dolla's to tycoons
        if calcDolla > tycoon['reqDollaForNxtLvl']:
            if tycoon['reqDollaForNxtLvl'] > 0:
                try:
                    tx = avapi.addDolla(tycoon['tid'], tycoon['reqDollaForNxtLvl'])
                    time.sleep(7)
                    print("Tycoon #" + str(tycoon['tid']) + " - added " + str(tycoon['reqDollaForNxtLvl']/(10**decimals)) + " dolla for upgrades.")
                    print("https://snowtrace.io/tx/" + str(tx))
                    doUpgrade = True
                    
                    calcDolla = calcDolla - tycoon['reqDollaForNxtLvl']
                except:
                    print("Error occured during tx, will try again.")
                    time.sleep(5)
                    try:
                        tx = avapi.addDolla(tycoon['tid'], tycoon['reqDollaForNxtLvl'])
                        time.sleep(7)
                        print("Tycoon #" + str(tycoon['tid']) + " - added " + str(tycoon['reqDollaForNxtLvl']/(10**decimals)) + " dolla for upgrades.")
                        print("https://snowtrace.io/tx/" + str(tx))
                        doUpgrade = True
                        
                        calcDolla = calcDolla - tycoon['reqDollaForNxtLvl']
                    except:
                        print("Error occured during tx again, will try again on next run.")
            else:
                doUpgrade = True
        else:
            print("Tycoon #" + str(tycoon['tid']) + " - Insufficient dolla for upgrades.")
            
        #upgrade tycoon
        if doUpgrade:
            nowtime = int(time.time())
            if nowtime >= tycoon['cooldownTs']:
                try:
                    tx = avapi.lvlTycoon(tycoon['tid'])
                    time.sleep(7)
                    print("Tycoon #" + str(tycoon['tid']) + " - updated to level " + str((tycoon['level']/100)+1) + ".")
                    print("https://snowtrace.io/tx/" + str(tx))
                    doWait = False
                except:
                    print("Error occured during tx, will try again.")
                    time.sleep(5)
                    try:
                        tx = avapi.lvlTycoon(tycoon['tid'])
                        time.sleep(7)
                        print("Tycoon #" + str(tycoon['tid']) + " - updated to level " + str((tycoon['level']/100)+1) + ".")
                        print("https://snowtrace.io/tx/" + str(tx))
                        doWait = False
                    except:
                        print("Error occured during tx again, will try again on next run.")
            else: 
                print("Tycoon #" + str(tycoon['tid']) + " - Still on cooldown.")
                
                if waituntil == 0 or waituntil > tycoon['cooldownTs']:
                    waituntil = tycoon['cooldownTs']
    
    #wait for the cooldown period
    if doWait:
        if waituntil > nowtime:
            print ("Processed all tycoons, wait cycle started for " + str(waituntil - nowtime) + " seconds.")
            time.sleep(waituntil - nowtime)

    time.sleep(10)
        
    
