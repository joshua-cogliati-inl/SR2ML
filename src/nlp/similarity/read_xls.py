import csv,os,sys,math,re,datetime
import simUtils
import pandas as pd

xls = pd.ExcelFile(sys.argv[1])
df_TASK = pd.read_excel(xls, 'TASK')
df_TASK = df_TASK.drop(0)
df_TASKRSRC = pd.read_excel(xls, 'TASKRSRC')
df_TASKRSRC = df_TASKRSRC.drop(0)


def getOnlyWords(s):
  """
   returns a string with only the words (removes things like T8, A-b, etc)
  """
  l = re.split("([-A-Za-z0-9]+)", s)
  return "".join([x for x in l if not re.search("[-0-9]+",x)])

# datetime.datetime.strptime(b, "%m/%d/%Y %I:%M:%S %p")
def getDateTime(s):
  """
   returns a string like 10/26/2014 6:00:00 AM or 1/5/2014 as a datetime
  """
  if type(s) != type(''):
    return s
  if 8 <= len(s) <= 10:
    return datetime.datetime.strptime(s, "%m/%d/%Y")
  return datetime.datetime.strptime(s, "%m/%d/%Y %I:%M:%S %p")

df_TASK_dates =  df_TASK[['act_start_date','act_end_date']].applymap(getDateTime)
df_TASK_delta = df_TASK_dates['act_end_date']  - df_TASK_dates['act_start_date']
df_TASK_delta.name = 'duration'


df_TASK_selected = df_TASK[['task_code','task_name','target_drtn_hr_cnt','total_drtn_hr_cnt']]

df_TASK_selected = pd.concat([df_TASK_selected,df_TASK_selected.rename(columns={'task_name':'short_name'})['short_name'].apply(getOnlyWords),df_TASK_delta],axis=1)
df_TASKSRC_selected = df_TASKRSRC[['task_id','role_id']].rename(columns={'task_id':'task_code'})
df_TASK_labeled = pd.merge(df_TASK_selected, df_TASKSRC_selected, how="left", on="task_code")
