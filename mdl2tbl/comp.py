import sys
from mdl2tbl import ora_test
from mdl2tbl import my_test

def mk_dict(rows):
    d = {}
    for row in rows: 
        k1 = row['SCHEMA'] + '|' + row['TBL_NM']+ '|' + row['COL_NM']
        d[k1] = row
        #print(k1, d[k1])
    return d

def mk_comp(d1,d2):
    comp = []
    #같은데 컬럼의 속성이 다른 경우 
    for pk in d1.keys():
        #같은 컬럼이 존재하면 처리한다.
        if pk in d2:
            pk_print = True 
            rstr = ""        
            for col in ['DT','NULLABLE','DEFT'] :
                #예외케이스 추가 시작
                #now() <=> CURRENT_TIMESTAMP
                #if ( d1[pk][col] == 'now()' and d2[pk][col] == 'CURRENT_TIMESTAMP'  ):
                #    pass
                #예외케이스 추가 종료                                    
                #elif d1[pk][col] != d2[pk][col]: 
                if d1[pk][col] != d2[pk][col]: 
                    if pk_print == True :
                        #print(pk,'='*(80-len(pk)))
                        pk_print = False                            
                    #print("%40s : %15s <=> %15s " % (col,d1[pk][col],d2[pk][col]))
                    rstr  += ("%40s : %15s <=> %15s " % (col,d1[pk][col],d2[pk][col])) + "<br>"
            if pk_print == False and len(rstr) > 0:
                comp.append ( { 'SCHEMA' : d1[pk]['SCHEMA'], 'TBL_NM' : d1[pk]['TBL_NM'] , 'COL_NM' : d1[pk]['COL_NM'] , 'DIFF' : rstr })
    # d1(MODEL)에만 존재하는 컬럼이 있는경우
    d1_only = d1.keys() - d2.keys()
    d2_tbls = set(row['TBL_NM'] for row in d2.values())
    for pk in d1_only:
        if ( d1[pk]['TBL_NM'] in d2_tbls ):
            comp.append ( { 'SCHEMA' : d1[pk]['SCHEMA'], 'TBL_NM' : d1[pk]['TBL_NM'] , 'COL_NM' : d1[pk]['COL_NM'] , 'DIFF' : "MODEL ONLY" })
    # d2(TABLE)에만 존재하는 컬럼이 있는경우
    d2_only = d2.keys() - d1.keys()
    d1_tbls = set(row['TBL_NM'] for row in d1.values())
    for pk in d2_only:
        if ( d2[pk]['TBL_NM'] in d1_tbls ):
            comp.append ( { 'SCHEMA' : d2[pk]['SCHEMA'], 'TBL_NM' : d2[pk]['TBL_NM'] , 'COL_NM' : d2[pk]['COL_NM'] , 'DIFF' : "TABLE ONLY" })
    return comp

##############################
# TEST START 
##############################
if __name__ == "__main__":
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


            