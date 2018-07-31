from dq.dbMysql import *
dev = Conn('elltdev')
dev.ssh.start()
dev.sshDbConn()
sql1 = """SELECT UPPER(REPLACE(TABLE_NAME,'_out','')) TABLE_NM, CONCAT('{ "TGT" : [',GROUP_CONCAT(CONCAT('"',TABLE_SCHEMA,'"')) ,'] }') TABLE_COPY_EXPLN
FROM (
select TABLE_NAME,UPPER(replace(replace(TABLE_SCHEMA,'ellt',''),'dev','')) TABLE_SCHEMA from information_schema.TABLES
where table_name in ( 'GD_GOODS_OUT'
,'GD_BRND_OUT'
,'GD_MD_GSGR_OUT'
,'GD_GOODS_PRC_OUT'
,'GD_BRND_CONTS_OUT'
,'GD_ITEM_SUP_ENTPRZ_STK_OUT'
,'GD_SUP_ENTPRZ_MAGN_OUT'
,'GD_GOODS_SMRY_OUT'
,'GD_BGOODS_CPNT_OUT'
,'DP_DSHOP_OUT'
,'DP_DSHOP_DGOODS_OUT'
,'PR_DC_GSGR_POL_OUT'
,'PR_DC_XCLUD_GOODS_OUT'
,'PR_CMPN_DC_GOODS_SMRY_OUT'
,'ET_ENTSHP_OUT'
,'ET_SUP_ENTPRZ_OUT'
,'ET_ENTPRZ_OUT'
,'ET_ENTPRZ_HLDY_OUT'
,'ET_ENTSHP_OWH_WTGVAL_OUT'
,'ET_SUP_ENTPRZ_OWH_WTGVAL_OUT'
,'ET_SUP_ENTPRZ_PRIOR_OWH_OUT'
,'CC_INTRST_MBR_DTL_OUT'
,'MB_EC_CUST_OUT'
,'MB_MBR_GRD_OUT'
,'OM_ORD_OUT'
,'OM_ORD_DTL_OUT'
,'OM_ORD_DTL_HST_OUT'
,'OM_ORD_STAT_HST_OUT'
,'OM_ORD_EXP_OUT'
,'OM_ORD_FVR_OUT'
,'OM_ORD_EXP_GOODS_OUT'
,'OM_CLAIM_OUT'
,'OM_CLAIM_DTL_OUT'
,'OM_CLAIM_STAT_HST_OUT'
,'LO_ORD_DLV_OUT'
,'LO_CLAIM_DLV_OUT'
,'PY_KEEP_MNY_DTL_OUT'
,'PY_MBSH_POINT_IF_OUT'
,'PY_PYF_OUT'
,'ST_CSCO_CD_OUT'
,'ST_CSCO_GRP_CD_OUT'
)
) A 
GROUP BY TABLE_NAME
"""
rows1 = dev.execute(sql1)
dev.close()

meta = Conn('meta')
meta.dbConn()
meta.select_db('elltDQtst')
sql2 = "update dq_tablecopy a set TABLE_COPY_EXPLN = '%s' WHERE TABLE_NM = '%s'"
for r in rows1 : print( sql2 % (  r['TABLE_COPY_EXPLN'] , r['TABLE_NM']))
for r in rows1 : meta.execute( sql2 % (  r['TABLE_COPY_EXPLN'] , r['TABLE_NM']))
meta.commit()
meta.close()

