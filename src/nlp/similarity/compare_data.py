import csv,os,sys,math,re
import simUtils
import numpy as np
import pandas as pd
import synsetUtils as SU
import time

def getLabeled(filename):
  xls = pd.ExcelFile(filename)
  df_TASK = pd.read_excel(xls, 'TASK')
  df_TASK = df_TASK.drop(0)
  df_TASKRSRC = pd.read_excel(xls, 'TASKRSRC')
  df_TASKRSRC = df_TASKRSRC.drop(0)

  df_TASK_selected = df_TASK[['task_code','task_name','target_drtn_hr_cnt','total_drtn_hr_cnt']]

  def getOnlyWords(s):
    """
     returns a string with only the words (removes things like T8, A-b, etc)
    """
    l = re.split("([-A-Za-z0-9]+)", s)
    return "".join([x for x in l if not re.search("[-0-9]+",x)])



  df_TASK_selected = pd.concat([df_TASK_selected,df_TASK_selected.rename(columns={'task_name':'short_name'})['short_name'].apply(getOnlyWords)],axis=1)
  df_TASKSRC_selected = df_TASKRSRC[['task_id','role_id']].rename(columns={'task_id':'task_code'})
  df_TASK_labeled = pd.merge(df_TASK_selected, df_TASKSRC_selected, how="left", on="task_code")
  return df_TASK_labeled




database_labeled = pd.read_csv(sys.argv[1]) #getLabeled(sys.argv[1])
lookups_labeled_pre = getLabeled(sys.argv[2])


def findClosestMatrix(database, lookups):
  databaseSynset = simUtils.convertSentsToSynsets(database)
  lookupSynset = simUtils.convertSentsToSynsets(lookups)
  simMatrix = np.zeros((len(databaseSynset),len(lookupSynset)))
  for i in range(len(databaseSynset)):
    for j in range(len(lookupSynset)):
      if databaseSynset[i] == lookupSynset[j]:
        simMatrix[i,j] = 1.0
      else:
        simMatrix[i,j] = SU.synsetListSimilarity(databaseSynset[i], lookupSynset[j])
        if np.isnan(simMatrix[i,j]):
          simMatrix[i,j] = -1.0
  return simMatrix


import sys
sys.path.append("..")
import Preprocessing

abbrExpander = Preprocessing.AbbrExpander('../data/abbreviations.xlsx')

abbrProcess = abbrExpander.abbrProcess

def addAbbrs(df_labeled):
  abbr_expand = df_labeled['short_name'].apply(abbrProcess)
  abbr_expand.name = 'abbr_expand'
  df_abbrs = pd.concat([df_labeled, abbr_expand],axis=1)
  return df_abbrs

# lookups_labeled_elec = lookups_labeled_pre[lookups_labeled_pre['role_id'] == 'ELEC']
# lookups_labeled_abbr = addAbbrs(lookups_labeled_elec.iloc[[100,500,1000]])
# mat2 = findClosestMatrix(database_labeled.abbr_expand, lookups_labeled_abbr.abbr_expand)
#  mat2.argmax(axis=0)
# database_labeled[['abbr_expand','total_drtn_hr_cnt']].iloc[mat2.argmax(axis=0)]
