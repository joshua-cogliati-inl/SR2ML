import csv,os,sys,math,re
import simUtils

data = []
with open(sys.argv[1], newline="") as csvfile:
  reader = csv.reader(csvfile)
  header1 = next(reader)
  header2 = next(reader)
  for row in reader:
    #print(row)
    data.append((row[3],float(row[11]),float(row[13])))

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

orig_data = data; data = [(getWords2(x[0]),) + x for x in orig_data]