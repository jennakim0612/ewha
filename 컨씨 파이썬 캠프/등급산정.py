std=[45, 84, 94, 42 ,86, 34, 59, 31, 22, 76]
for x in std :
    if (x<40) :
        grd="D"
        
    elif (x<60) :
        grd="C"
                
    elif (x<80) :
        grd="B"
                
    else :
        grd="A"
        
    print("%d점 - %s" %(x, grd))
        