from background_task import background
from logging import getLogger
from . import views
logger = getLogger(__name__)

@background(schedule=60)
def demo_task(message):
    logger.debug('demo_task. message={0}'.format(message))

@background(schedule=0)
def vrfy_task(message, verbose_name="vrfy_task"):
    #try:
    no = message['VRFY_NO']
    env = message['env']
    logger.debug('[START]vrfy_task no ={0}'.format(no))
    ret = views.vrfy_job(no,env)
    logger.debug('[END]vrfy_task no ={0}'.format(no)) 
    return ret       
    #except Exception as e:
    #    logger.debug('[ERROR]vrfy_task. Error={0}'.format(e))

@background(schedule=0)
def vrfy_task_aurora(message, verbose_name="vrfy_task_aurora"):
    #try:
    env = message['env']
    logger.debug('[START]vrfy_task_aurora env ={0}'.format(env))
    ret = views.vrfy_job_aurora(env)
    logger.debug('[END]vrfy_task_aurora env ={0}'.format(env)) 
    return ret       
    #except Exception as e:
    #    logger.debug('[ERROR]vrfy_task. Error={0}'.format(e))    