#!/usr/bin/python
import sys
import commands

'''
zabbix messages configure
  {
    "app_id":id;
    "eventType":(trigger,resolve);
    "eventid": {EVENT.ID};
    "alarmName":{TRIGGER.STATUS}:{TRIGGER.NAME};
    "alermContent":{TRIGGER.DESCRIPTION}
    "priority":{TRIGGER.SERVERITY} 'High,','Warning','Average','Disaster' 1,2,3

  }
'''
def parse_args(app_id,subject,messages):
    Dict={}
    Dict['app_id']=app_id
    if subject == 'trigger':
        Dict['eventType']=subject.strip()
    elif subject== 'resolve':
        Dict['eventType']=subject.strip()
    else:
        print 'the zabbix action configuring error ,please check it '
        exit(1)
    def parse_mesg(mesg):
        tmp_l=[]
        mesg_dict={}
        mesg_to_list=mesg.split('\n')
        cut_mesg=[x.strip().replace('\r','') for x in mesg_to_list]
        for s in cut_mesg:
            if s !='':
                tmp_l.append(s)
        for m in tmp_l:
            if m.find(':'):
                l=m.split(':')
                mesg_dict[l[0]]=l[1]
        return mesg_dict
    mesg_dict=parse_mesg(messages)
    Dict['mesg']=mesg_dict
    return Dict

eventType=''
alarmName=''
eventId=''
app_id=''
priority=''
alarmContent=''

def send_mesg(mesg_dict):
    global eventType,alarmname,eventId,app_id,priority,alarmContent
    mesg=mesg_dict['mesg']
    eventId=mesg.get('eventId','')
    app_id=mesg_dict.get('app_id','')
    eventType=mesg_dict.get('eventType','')
    alarmName=mesg.get('alarmName','')
    alarmContent=mesg.get('alarmContent','')
    if mesg.get('priority') == 'Warning' or mesg.get('priority') == 'Average':
        priority='2'
    else:
        priority='3'
    params={}
    params['app']=app_id
    params['eventType']=eventType
    params['alarmName']=alarmName
    params['eventId']=eventId
    params['priority']=priority
    params['alarmContent']=alarmContent
    cmd=''' curl -H "Content-type: application/json" -X POST -d"%s" "http://api.110monitor.com/alert/api/event" -o /tmp/xixi.log''' %params
    params_str=urllib.urlencode(params)
    URL="http://api.110monitor.com/alert/api/event?%s" %params_str
    res,ouput=commands.getstatusoutput(cmd)
if __name__=='__main__':
    send_mesg(parse_args(sys.argv[1],sys.argv[2],sys.argv[3]))



