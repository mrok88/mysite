import sys
import ora_test
import my_test

def mk_dict(rows):
    d = {}
    for row in rows: 
        k1 = row['SCHEMA'] + '|' + row['TBL_NM']+ '|' + row['COL_NM']
        d[k1] = row
        #print(k1, d[k1])
    return d

def mk_comp(d1,d2):
    comp = []
    for pk in d1.keys():
        #같은 컬럼이 존재하면 처리한다.
        if pk in d2:
            pk_print = True 
            rstr = ""        
            for col in ['DT','NULLABLE','DEFT'] :
                if d1[pk][col] != d2[pk][col]:  
                    if pk_print == True :
                        #print(pk,'='*(80-len(pk)))
                        pk_print = False                            
                    #print("%40s : %15s <=> %15s " % (col,d1[pk][col],d2[pk][col]))
                    rstr  += ("%40s : %15s <=> %15s " % (col,d1[pk][col],d2[pk][col])) + "<br>"
            if pk_print == False and len(rstr) > 0:
                comp.append ( { 'SCHEMA' : d1[pk]['SCHEMA'], 'TBL_NM' : d1[pk]['TBL_NM'] , 'COL_NM' : d1[pk]['COL_NM'] , 'DIFF' : rstr })
    return comp

if  len(sys.argv) == 2 :
    subj_area = sys.argv[1]
else:
    subj_area = '%'
rows1 = ora_test.get_mdl(subj_area)
d1 = mk_dict(rows1)

rows2 = my_test.get_tbl(subj_area)
d2 = mk_dict(rows2)

comp = mk_comp(d1,d2)

print(comp)


            