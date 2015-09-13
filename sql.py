#SQL problem
#http://cdb.io/1i5ssO3

import sqlite3
import numpy as np
from scipy import stats

def score_by_zipcode():
    
    sqlite_file = 'RESTAURANT'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    sql_command = "SELECT ZIPCODE, count(ZIPCODE) from webextract GROUP by ZIPCODE"
    c.execute(sql_command)
    zips = c.fetchall()
    
    zips.sort(key=lambda x: x[1])
    zips.reverse()
    zips_with_more_than_hundred_insp = zips[0:184]
    zips_with_more_than_hundred_insp = [list(i) for i in zips_with_more_than_hundred_insp]
    
    for i in range(len(zips_with_more_than_hundred_insp)):
        zz = zips_with_more_than_hundred_insp[i][0]
        sql_command = 'SELECT SCORE FROM webextract WHERE ZIPCODE=='+str(zz)
        c.execute(sql_command)
        scores_of_zips_with_more_than_hundred_insp = c.fetchall()
        
        scores_of_zips_with_more_than_hundred_insp = np.array([kk[0] for kk in scores_of_zips_with_more_than_hundred_insp])
        zips_with_more_than_hundred_insp[i].append(scores_of_zips_with_more_than_hundred_insp.mean())
        zips_with_more_than_hundred_insp[i].append(stats.sem(scores_of_zips_with_more_than_hundred_insp))
        
        
        #scores_of_zips_with_more_than_hundred_insp[0][0]
    zips_with_more_than_hundred_insp = [(str(int(i[0])),i[2],i[3],i[1]) for i in zips_with_more_than_hundred_insp]
    zips_with_more_than_hundred_insp.sort(key=lambda x: x[1])
    #zips_with_more_than_hundred_insp.reverse()
    
    return zips_with_more_than_hundred_insp


def score_by_map():
    
    zips_with_more_than_hundred_insp = score_by_zipcode()
    f=open('data.csv','w')
    for l in zips_with_more_than_hundred_insp:
        print >>f, l[0],l[1]
    f.close()

#################################################################

def score_by_borough():
    
    sqlite_file = 'RESTAURANT'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    sql_command = "SELECT webextract.BORO, BORONAME, count(webextract.BORO) from webextract JOIN boroughs ON (boroughs.BORO = webextract.BORO) GROUP by webextract.BORO"
    c.execute(sql_command)
    boro = c.fetchall()
    boro = [list(i) for i in boro]
    
    for i in range(len(boro)):
        zz = boro[i][0]
        sql_command = 'SELECT SCORE FROM webextract WHERE BORO=='+str(zz)
        c.execute(sql_command)
        scores_of_boros = c.fetchall()
        
        scores_of_boros = np.array([kk[0] for kk in scores_of_boros])
        boro[i].append(scores_of_boros.mean())
        boro[i].append(stats.sem(scores_of_boros))
        
        
    boro = [(str(i[1]),i[3],i[4],i[2]) for i in boro]
    boro.sort(key=lambda x: x[1])

    return boro
    


#####################################################

def score_by_cuisine():

    sqlite_file = 'RESTAURANT'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    
    sql_command = "SELECT webextract3.CUISINECODE, count(webextract3.CUISINECODE), cuisine.CODEDESC from webextract3 JOIN cuisine ON (cuisine.CUISINECODE = webextract3.CUISINECODE) GROUP by webextract3.CUISINECODE"
    c.execute(sql_command)
    cuisines = c.fetchall()
    
    cuisines.sort(key=lambda x: x[1])
    cuisines.reverse()
    cuisines_with_more_than_hundred_insp = cuisines[0:75]
    cuisines_with_more_than_hundred_insp = [list(i) for i in cuisines_with_more_than_hundred_insp]
    #return cuisines_with_more_than_hundred_insp
    
    for i in range(len(cuisines_with_more_than_hundred_insp)):
        zz = cuisines_with_more_than_hundred_insp[i][0]
        sql_command = 'SELECT SCORE FROM webextract3 WHERE CUISINECODE=='+str(zz)
        c.execute(sql_command)
        scores_of_cuisines_with_more_than_hundred_insp = c.fetchall()

        scores_of_cuisines_with_more_than_hundred_insp = np.array([kk[0] if kk[0] else 0. for kk in scores_of_cuisines_with_more_than_hundred_insp])
        cuisines_with_more_than_hundred_insp[i].append(scores_of_cuisines_with_more_than_hundred_insp.mean())
        cuisines_with_more_than_hundred_insp[i].append(stats.sem(scores_of_cuisines_with_more_than_hundred_insp))
        
    cuisines_with_more_than_hundred_insp = [(str(i[2]),i[3],i[4],i[1]) for i in cuisines_with_more_than_hundred_insp]
    cuisines_with_more_than_hundred_insp.sort(key=lambda x: x[1])
    
    return cuisines_with_more_than_hundred_insp
    
#####################################################

import copy
def violation_by_cuisine():
    
    sqlite_file = 'RESTAURANT'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
                
    sql_command = "SELECT AAA.CUISINECODE, AAA.VIOLCODE, AAA.Count1, AAA.Count1 * 1.0 / BBB.Count2 As Freq\
                    FROM ( \
                    SELECT webextract3.CUISINECODE, webextract3.VIOLCODE, Count(*) AS Count1 \
                    FROM webextract3 \
                    GROUP BY webextract3.CUISINECODE, webextract3.VIOLCODE \
                    ) AS AAA \
                    INNER JOIN ( \
                        SELECT webextract3.CUISINECODE, COUNT(*) AS Count2 \
                        FROM webextract3 \
                        GROUP BY webextract3.CUISINECODE \
                        ) AS BBB \
                        ON AAA.CUISINECODE = BBB.CUISINECODE "
    
    c.execute(sql_command)
    cond_probs = c.fetchall()    
    cond_probs = [cp for cp in cond_probs if cp[2] > 100]

    sql_command = "SELECT VIOLCODE, count(VIOLCODE) from webextract3 GROUP by VIOLCODE"
    c.execute(sql_command)
    uncond_probs = c.fetchall()
    uncond_probs = [up for up in uncond_probs if up[1] > 100]
    number_of_valid_rows = sum([i[1] for i in uncond_probs])
    uncond_probs = dict((x, float(y)/number_of_valid_rows) for x, y in uncond_probs)

    sql_command = "SELECT * from cuisine"
    c.execute(sql_command)
    cuisine_lookup = c.fetchall()
    cuisine_lookup = dict((x, y) for x, y in cuisine_lookup)
    #print cuisine_lookup
    
    sql_command = "SELECT VIOLATIONCODE, VIOLATIONDESC from violations2"
    c.execute(sql_command)
    violations_lookup = c.fetchall()
    violations_lookup = dict((x, y) for x, y in violations_lookup)

    result = []
    for cc in cond_probs:
        try:
            result.append( ((cuisine_lookup[cc[0]],violations_lookup[cc[1]]),(cc[3]/uncond_probs[cc[1]]),cc[2]) )
        except KeyError:
            continue

    result.sort(key=lambda x: x[1])
    result.reverse()
    return result[0:20]