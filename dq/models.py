###########################################################################
#     Meta-eXpress 2.1 
#     All right reserved by wonseokyou 
#     email : wonseokyou@gmail.com 
###########################################################################
from django.db import models

from datetime import datetime
from django.utils import timezone
from django.core.urlresolvers import reverse
# Create your models here.
YN_LIST = ( ('Y','Yes') ,('N','No' ))

class Vrfy(models.Model):
    VRFY_TYPE_CD_LIST = ( ('LC', 'Life_Cycle'), ('DR', 'Design_Rule'), ('BR', 'Biz_Rule'))
    VRFY_TYPE_DTL_CD_LIST = ( ('DMN', '도메인검증'), ('REF', '참조검증'), ('NT_NML', '비정규검증'), ('BIZ_RUL', '업무규칙검증'))
    CMD_TYPE_CD_LIST = ( ('AURORA_SQL', 'AURORA_SQL'), ('ATHENA_SQL', 'ATHENA_SQL'), ('DYNAMODB_QRY', 'DYNAMODB_QRY'), ('RED_SHIFT_QRY', 'RED_SHIFT_QRY'), ('SHELL', 'SHELL'), ('ETC', 'ETC'))

    VRFY_NO =  models.AutoField(verbose_name="검증번호",primary_key=True,editable=False)

    DB_NM = models.CharField(verbose_name="DB명",max_length=100)
    SCHEMA_NM = models.CharField(verbose_name="스키마명",max_length=100)
    CLSF_NM1 = models.CharField(verbose_name="대분류명",max_length=100,default=None, blank=True, null=True)
    CLSF_NM2 = models.CharField(verbose_name="중분류명",max_length=100,default=None, blank=True, null=True)
    VRFY_TYPE_DTL_CD = models.CharField(verbose_name="검증유형상세코드",max_length=30 ,choices=VRFY_TYPE_DTL_CD_LIST, default='BIZ_RUL')    
    VRFY_NM = models.CharField(verbose_name="검증명",max_length=100)
    VRFY_EXPLN = models.TextField(verbose_name="검증설명",max_length=500,default=None, blank=True, null=True)
    TABLE_HANGL_NM = models.CharField(verbose_name="테이블한글명",max_length=100)
    TABLE_NM = models.CharField(verbose_name="테이블명",max_length=100)
    REFRC_TABLE_HANGL_NM = models.CharField(verbose_name="참조테이블한글명",max_length=100,default=None, blank=True, null=True)
    REFRC_TABLE_NM = models.CharField(verbose_name="참조테이블명",max_length=100,default=None, blank=True, null=True)
    USE_YN = models.CharField(verbose_name="사용여부",max_length=1,choices=YN_LIST, default='Y')    
    CMD_TYPE_CD = models.CharField(verbose_name="명령유형코드",max_length=30 ,choices=CMD_TYPE_CD_LIST, default='01')
    CMD_CNTS = models.TextField(verbose_name="검증내용",max_length=14000,default=None, blank=True, null=True)

    RGSTR_ID = models.CharField(verbose_name="등록자ID",max_length=30,default='DA')
    #RGST_DTTM = models.DateTimeField(verbose_name="등록일시",default=timezone.now())
    RGST_DTTM = models.DateTimeField(verbose_name="등록일시",auto_now_add=True)
    MODR_ID = models.CharField(verbose_name="수정자ID",max_length=30,default='DA')
    #MODI_DTTM = models.DateTimeField(verbose_name="수정일시",editable=False)
    MODI_DTTM = models.DateTimeField(verbose_name="수정일시",auto_now=True)


    def __unicode__(self):
        return self.TABLE_NM

    def __str__(self):
        return str(self.VRFY_NO) + ":" + self.TABLE_NM

    def get_absolute_url(self):
        return reverse('vrfys:vrfy_edit', kwargs={'pk': self.pk})    

class Vrfy_Cmd(models.Model):
    CMD_DVS_CD_LIST = ( ('VRFY', '검증'), ('EXE', '실행'))
    CMD_TYPE_CD_LIST = ( ('AURORA_SQL', 'AURORA_SQL'), ('SHELL', 'Shell'), ('AURORA_PROC', 'AURORA프로시져'), ('ATHENA_SQL', 'ATHENA_SQL'))
    VRFY_CMD_NO =  models.AutoField(verbose_name="검증명령어번호",primary_key=True,editable=False)
    VRFY_NO =  models.ForeignKey(Vrfy)
    VRFY_SEQ = models.IntegerField(verbose_name="검증순번")

    AUTO_CK_YN = models.CharField(verbose_name="자동체크여부",max_length=1,choices=YN_LIST, default='N')    
    CMD_DVS_CD = models.CharField(verbose_name="명령어구분코드",max_length=20 ,choices=CMD_DVS_CD_LIST, default='VRFY')
    CMD_TYPE_CD = models.CharField(verbose_name="명령어유형코드",max_length=20 ,choices=CMD_TYPE_CD_LIST, default='AURORA_SQL')
    CMD_CNTS = models.TextField(verbose_name="명령어내용",max_length=4000,default=None, blank=True, null=True)

    DTL_VRFY_YN = models.CharField(verbose_name="상세검증여부",max_length=1,choices=YN_LIST, default='N')    
    
    LAST_EXE_DTTM = models.DateTimeField(verbose_name="마지막수행일시",default=datetime.now())
    
    RGSTR_ID = models.CharField(verbose_name="등록자ID",max_length=30,default='DA')
    #RGST_DTTM = models.DateTimeField(verbose_name="등록일시",default=datetime.now())
    RGST_DTTM = models.DateTimeField(verbose_name="등록일시",auto_now_add=True)
    MODR_ID = models.CharField(verbose_name="수정자ID",max_length=30,default='DA')
    #MODI_DTTM = models.DateTimeField(verbose_name="수정일시",default=datetime.now())
    MODI_DTTM = models.DateTimeField(verbose_name="수정일시",auto_now=True)

    def __unicode__(self):
        return self.VRFY_CMD_NO

    def get_absolute_url(self):
        return reverse('vrfy_Cmds:vrfy_Cmd_edit', kwargs={'pk': self.pk})