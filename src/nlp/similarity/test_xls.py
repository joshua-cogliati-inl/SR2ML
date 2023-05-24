import csv,os,sys,math,re
import simUtils
import pandas as pd
import synsetUtils as SU
import time

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
      if synsets[i] == synsets[j]:
        simMatrix[(i,j)] = 1.0
      else:
        simMatrix[(i,j)] = SU.synsetListSimilarity(synsets[i],synsets[j])
  return simMatrix

#   0 1 2 3
# 0
# 1 x
# 2 x x
# 3 x x x

# m = getMatrix(partSynsets)




"""
import sys
sys.path.append("..")
import Preprocessing

abbrList = pd.read_excel('../data/abbreviations.xlsx')

preprocessorList = ['hyphenated_words',
                    'whitespace',
                    'numerize']

preprocess = Preprocessing.Preprocessing(preprocessorList, {})

text = 'Perf ann sens calib of cyl'
text = preprocess(text)

checker = Preprocessing.SpellChecker(text.lower(), checker='mixed')

cleanedText = checker.handleAbbreviations(abbrList, type='mixed')


checker = Preprocessing.SpellChecker(checker='mixed')

cleanedText = checker.handleAbbreviations(abbrList, text.lower(), type='mixed')
"""

import sys
sys.path.append("..")
import Preprocessing
"""

abbrList = pd.read_excel('../data/abbreviations.xlsx')

preprocessorList = ['hyphenated_words',
                    'whitespace',
                    'numerize']

preprocess = Preprocessing.Preprocessing(preprocessorList, {})

def abbrProcess(text):
  text = preprocess(text)
  checker = Preprocessing.SpellChecker(text.lower(), checker='mixed')
  cleanedText = checker.handleAbbreviations(abbrList, type='mixed')
  return cleanedText

# for n in df_TASK_labeled.short_name[:20]: print(n,abbrProcess(n))

# abbrNames = []
# for n in df_TASK_labeled.short_name[:20]: abbrNames.append(abbrProcess(n))
#
# abbrNamesUniq = list(set(abbrNames))
# abbrSynsets = simUtils.convertSentsToSynsets(abbrNamesUniq)
# mat = getMatrix(abbrSynsets)
"""

abbrExpander = Preprocessing.AbbrExpander('../data/abbreviations.xlsx')

abbrProcess = abbrExpander.abbrProcess

role_id_set = set(df_TASK_labeled.role_id)

# df_TASK_labeled[df_TASK_labeled["role_id"] == 'WEST']
# dict(df_TASK_labeled['role_id'].value_counts())
# df_TASK_subset = df_TASK_labeled[df_TASK_labeled["role_id"] == 'WEST']
# abbr_expand = df_TASK_subset['short_name'].apply(abbrProcess)
# df_TASK_abbr_subset = pd.concat([df_TASK_subset, abbr_expand.rename({'short_name':'abbr_expand'})],axis=1)
# abbrSubsetSynsets = simUtils.convertSentsToSynsets(df_TASK_abbr_subset.abbr_expand)
# subset_mat = getMatrix(abbrSubsetSynsets)

def getSubsetMatrix(df_TASK_labeled, role_id):
  df_TASK_subset = df_TASK_labeled[df_TASK_labeled["role_id"] == role_id]
  abbr_expand = df_TASK_subset['short_name'].apply(abbrProcess)
  abbr_expand.name = 'abbr_expand'
  df_TASK_abbr_subset = pd.concat([df_TASK_subset, abbr_expand],axis=1)
  abbrSubsetSynsets = simUtils.convertSentsToSynsets(df_TASK_abbr_subset.abbr_expand)
  subset_mat = getMatrix(abbrSubsetSynsets)
  return (df_TASK_abbr_subset, subset_mat)

def getPlainSubsetMatrix(df_TASK_labeled, role_id):
  df_TASK_subset = df_TASK_labeled[df_TASK_labeled["role_id"] == role_id]
  subsetSynsets = simUtils.convertSentsToSynsets(df_TASK_subset.short_name)
  subset_mat = getMatrix(subsetSynsets)
  return (df_TASK_subset, subset_mat)

# stuff = getSubsetMatrix(df_TASK_labeled,'SEEI')

# chem_stuff = getSubsetMatrix(df_TASK_labeled,'CHEM')

# chem_stuff[0].to_csv("/tmp/chem.csv")

def makeMatrixJsonable(origMatrix):
  matrix = {}
  for key in origMatrix:
    jkey = json.dumps(key)
    matrix[jkey] = origMatrix[key]
  return matrix

def deJsonMatrix(jsonMatrix):
  matrix = {}
  for jkey in jsonMatrix:
    key = tuple(json.loads(jkey))
    matrix[key] = jsonMatrix[jkey]
  return matrix

# json.dump(makeMatrixJsonable(chem_stuff[1]), open("/tmp/chem.json", "w"))

# jmatrix = json.load(open("/tmp/chem.json", "r"))
