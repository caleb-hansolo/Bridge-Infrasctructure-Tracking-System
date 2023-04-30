import EPB0 # Epaper 2.13 landscape mode library
import random

if __name__=='__main__':
    epd = EPB0.EPD_2in13()
    epd.Clear(0xff)
    # COORDINATES ARE MAPPED TO 1ST QUADRANT!
    # origin is BOTTOM LEFT in landscape mode
    
    # some variables for checking status:
    weeklyScore = 0 
    totalScore = 0
    week = 0 # what week
    
    # variables received from internet/weather services
    season = ["spring","summer","fall","winter"]
    currentSeason = "spring"    
    precip = 0; # precipitation levels - 0 is no precip
    precipMultiplier = 1
    weather = ["clear","cloudy","stormy"]
    currentWeather = "clear" # displays current weather conditions
    temperature = random.randint(60, 95) # temperature in fahrenheit
    tempMultiplier = 1 # temperature has impact on tempMultiplier
    avgTraffic = 0
    
    # variables received from sensor
    bridgeLevel = 0 # how level is the bridge? higher number is less level
    moisture = 0 # moisture level of the area around bridge, also tells if it is flooded
    freezethaw = False
    decayMultiplier = 1
    
    graphWeek = 10 # x value at start of graph
    EPB0.DLineH(graphWeek, 10, graphWeek + (2 * 53)) # bold horizantal line on bottom for graph base
    EPB0.PrtLtxt("Scores:", 5, 11, 0)
    
    
    
    # loop for entire day
    while week < 53:
        estWeeklyScore = 9 # estimated amount of power (in Watts) that a panel will produce in 1 hour (perfect conditions)
        precipMultiplier = 1
        decayMultiplier = 1 - (bridgeLevel * .01)
        
        if week <= 13:
            currentSeason=season[0]
        elif week > 13 and week <= 26:    
            currentSeason=season[1]
        elif week > 26 and week <= 39:   
            currentSeason=season[2]
        elif week > 39 and week <= 52:    
            currentSeason=season[3]
        
        # temperature climbs or declines depending on time of year
        tempTemp = temperature
        if currentSeason == "spring":
            temperature += random.randint(-3, 10)
            if temperature >= 90:
                temperature += random.randint(-8, -2)
            elif temperature <= 32:
                temperature += random.randint(2, 8)
        elif currentSeason == "summer":
            temperature += random.randint(-3, 15)
            if temperature >= 110:
                temperature += random.randint(-8, -2)
            elif temperature <= 50:
                temperature += random.randint(2, 8)
        elif currentSeason == "fall":
            temperature += random.randint(-10, 3)
            if temperature >= 90:
                temperature += random.randint(-8, -2)
            elif temperature <= 32:
                temperature += random.randint(2, 8)
        elif currentSeason == "winter":
            temperature += random.randint(-15, 3)
            if temperature >= 50:
                temperature += random.randint(-8, -2)
            elif temperature <= 0:
                temperature += random.randint(2, 8)
        
        
            
        
        # weather determines precip level    
        
        currentWeather = random.choice(weather)
        if currentWeather == "clear":
            temperature += random.randint(2, 5)
            precip = 0
        elif currentWeather == "cloudy":
            temperature -= random.randint(2, 5)
            precip = 0
        elif currentWeather == "stormy":
            temperature -= random.randint(4, 7)
            precip = random.randint(1,7)
        
        if precip > 4:
            precipMultiplier = 1 - (precip/2)*.01
            #moisture = random.randint()
        
        
            
            
        # temperature range
        if temperature < 0:
            temperature += random.randint(0, 8)
        elif temperature > 123:
            temperature -= random.randint(0, 8)
            
        if temperature >= 32 and temperature <= 95:
            tempMultiplier = 1
        elif temperature > 95:
            tempMultiplier = 1 - (.001 * (temperature - 95))
        elif temperature < 60:
            tempMultiplier = 1 - (.001 * (32 - temperature))
            
        
     # DETERIORATION FACTORS 
        #traffic
        avgTraffic = 90
        avgTraffic += random.randint(-15,15)
        if avgTraffic > 150:
            decayMultiplier *= .98
        elif avgTraffic < 30:
            decayMultiplier *= 1.04
        
        # moisture/humidity levels out of 100%
        if precip > 0 and precip <= 2:
            moisuture = random.randint(38, 50)
        if precip > 2 and precip <= 4:
            moisuture = random.randint(50, 60)
        if precip > 4 and precip <= 6:
            moisuture = random.randint(60, 75)
        if precip == 7:
            moisture = random.randint(75,90)   
        decayMultiplier -= (moisture*.0005)
        
        # freezethaw true? freeze then melt and expand
        if tempTemp <= 32 and temperature > 32:
            freezethaw = True
            decayMultiplier *= .99
        
        #is bridge level?
        if week == 26:
            bridgeLevel = random.randint(1,2)
            decayMultiplier -= (bridgeLevel * .01)
        if week == 45:
            bridgeLevel == random.randint(2,3)
            decayMultiplier -= (bridgeLevel * .01)
        
        

            
        # putting environmental multipliers into effect
        if week > 1:
            estWeeklyScore = prevWeekScore * tempMultiplier * precipMultiplier * decayMultiplier
        else:
            estWeeklyScore = estWeeklyScore * tempMultiplier * precipMultiplier * decayMultiplier
        weeklyScore = estWeeklyScore

        print(currentWeather)
        print("temperature: ",temperature)
        
        # display updates to show status of bridge:
        EPB0.PrtStxt("week: " + str(week), 5, 14, 0)
        EPB0.PrtStxt("Score: " + str(int(weeklyScore)), 130, 14, 0)
        if currentSeason == "fall":
            EPB0.PrtStxt("season: " + str(currentSeason) + "  ", 130, 12, 0)
        else:
            EPB0.PrtStxt("season: " + str(currentSeason) + " ", 130, 12, 0)
        EPB0.PrtStxt("weather:" + str(currentWeather) + " ", 130, 10, 0)
        EPB0.PrtStxt("precip: " + str(precip) + " ", 130, 8, 0)
        EPB0.PrtStxt("temp (F): " + str(temperature) + " ", 130, 6, 0)
        EPB0.PrtStxt("moist: " + str(moisture) + " ", 130, 4, 0)
        EPB0.PrtStxt("traffic: " + str(avgTraffic) + "  ", 130, 2, 0)
        if weeklyScore <= 4:
            EPB0.PrtStxt("check on bridge!", 10, 0, 0)
            print("check on that bridge, man! it's deteriorating!")
        EPB0.Rect(graphWeek, 10, 2, int(weeklyScore * 8)) # grphs hourly power output in graph on left side each hour
        epd.display(EPB0.Beeld) # updates display with full refresh
        
        # for example purposes, the delay time below is set to 4000 milliseconds, or 4 second(s)
        # change number below to 3600000 for an actual hour
        epd.delay_ms(1000) # time between loops, shuts off power to display, meaning it can't be updated yet it maintains the image
        
        prevWeekScore = weeklyScore
        graphWeek += 2
        week += 1 #last operation in this while loop
    
    
    print(graphWeek)
    #epd.display(EPB0.Beeld) # Beeld is being called as an image: THIS IS WHAT MAKES STUFF APPEAR
    #epd.delay_ms(2000) # shuts off power to display, meaning it can't be updated yet it maintains the image
    epd.Clear(0xff) # clears the display
    epd.delay_ms(2000)
    epd.sleep()
