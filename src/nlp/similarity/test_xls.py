import csv,os,sys,math,re
import simUtils
import pandas as pd
import synsetUtils as SU

data = []
#with open(sys.argv[1], newline="") as csvfile:
#  reader = csv.reader(csvfile)
#  header1 = next(reader)
#  header2 = next(reader)
#  for row in reader:
#    #print(row)
#    data.append((row[3],float(row[11]),float(row[13])))
#               task_name, target_drtn_hr_cnt, total_drtn_hr_cnt
xls = pd.ExcelFile(sys.argv[1])
df_TASK = pd.read_excel(xls, 'TASK')
df_TASK = df_TASK.drop(0)
df_TASKRSRC = pd.read_excel(xls, 'TASKRSRC')
df_TASKRSRC = df_TASKRSRC.drop(0)

task_id_to_role_id = {}
for i in range(1,len(df_TASKRSRC['task_id'])+1):
  task_id_to_role_id[df_TASKRSRC['task_id'][i]] = df_TASKRSRC['role_id'][i]
for i in range(1,len(df_TASK['task_name'])+1):
  data.append((df_TASK['task_name'][i], df_TASK['target_drtn_hr_cnt'][i],  df_TASK['total_drtn_hr_cnt'][i], task_id_to_role_id.get(df_TASK['task_code'][i], None)))
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


def getSim(s, data):
  simData = []
  for d in data:
    sim = simUtils.sentenceSimilarity(s, d[0])
    simData.append((sim,)+d)
  return simData

def getSim2(s, data):
  simData = []
  for d in data:
    sim = simUtils.sentenceSimilarity(s, d[0], infoContentNorm=False, delta=0.85)
    simData.append((sim,)+d)
  return simData

_words = re.compile("[a-z]+")
def getWords(s):
  return " ".join(_words.findall(s.lower()))
# new_data = [(getWords(x[0]),) + x for x in data]

def getWords2(s):
  l = re.split("([-A-Za-z0-9]+)", s)
  return "".join([x for x in l if not re.search("[-0-9]+",x)])
# new_data = [(getWords2(x[0]),) + x for x in data]

def getOnlyWords(s):
  """
   returns a string with only the words (removes things like T8, A-b, etc)
  """
  l = re.split("([-A-Za-z0-9]+)", s)
  return "".join([x for x in l if not re.search("[-0-9]+",x)])

def getSimOnlyWords(s, data):
  simData = []
  sw = getWords(s)
  for d in data:
    sim = simUtils.sentenceSimilarity(sw, getWords(d[0]), infoContentNorm=False, delta=0.85)
    simData.append((sim,)+d)
  return simData


def getSimWithDis(s, data):
  simData = []
  for d in data:
    sim = simUtils.sentenceSimilarityWithDisambiguation(s, d[0], senseMethod='simple_lesk', simMethod='semantic_similarity_synsets', delta=0.85)
    simData.append((sim,)+d)
  return simData


#sd1 = getSim(data[0][0], data[:100])
#sd2 = getSim(data[-1][0], data[:100])
#swdo = getSimWithDis(data[0][0], data[:100])
#swdo.sort()

def denan(l):
  def denanSub(x):
    if math.isnan(x):
      return -1
    else:
      return x
  return [(denanSub(x[0]),)+x[1:] for x in l]

#orig_data = data; data = [(getWords2(x[0]),) + x for x in orig_data]


# sents = df_TASK_labeled[:2].task_name
# sentSynsets = simUtils.convertSentsToSynsets(sents)
# similarity = SU.synsetListSimilarity(sentSynsets[0], sentSynsets[1], delta=.8)
# fullSynsets = simUtils.convertSentsToSynsets(df_TASK_labeled.task_name)
# partSynsets = simUtils.convertSentsToSynsets(df_TASK_labeled[:100].task_name)

# simData = []
# for i in range(len(partSynsets)):
#   sim = SU.synsetListSimilarity(partSynsets[i], partSynsets[0])
#   simData.append((sim,)+tuple(df_TASK_labeled[i:i+1].values.tolist()[0]))
# simData = denan(simData)
# simData.sort(key=lambda x:x[0])

def getMatrix(synsets):
  simMatrix = {}
  for i in range(len(synsets)):
    for j in range(0,i):
      simMatrix[(i,j)] = SU.synsetListSimilarity(synsets[i],synsets[j])
  return simMatrix

#   0 1 2 3
# 0
# 1 x
# 2 x x
# 3 x x x

# m = getMatrix(partSynsets)
