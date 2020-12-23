import math
import csv

Name = []
Glucose = []
BloodPressure = []
BMI = []
Age = []
Outcome = []

with open("diabetes.csv", "r") as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for lines in csv_reader:
      #print(lines['COUNTRY_ID'], lines['COUNTRY_NAME'])
      Name.append(lines['Name'])
      Glucose.append(int(float(lines['Glucose'])))
      BloodPressure.append(int(float(lines['BloodPressure'])))
      BMI.append(round(float(lines['BMI'])))
      Age.append(int(lines['Age']))
      Outcome.append(int(lines['Outcome']))

# unset = 0 ---- nth bit starts form right ---- x number
def unset_nth_bit(x: int, n: int):
  return bin(x & ~(1 << n))

# set = 1 ---- nth bit.....starts form right ---- x number
def set_nth_bit(x: int, n: int):
  return bin(x | 1 << n)


g = 4 #group size
Dataset = Glucose
D = len(Dataset) #144

print(Dataset)
preservedDataset = []

Seed = [1, 2, 4, 6]
#weights range [0, g-1]
weights = [1, 2, 1, 2]
full_watermark = [1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1]
n = math.floor((abs(D)/g)) - 1
l = 1
dcount = 0
wcount = 0
#first_column = 0; #add watermark if first

for x in range(n+1):

  gList = [Dataset[dcount], Dataset[dcount+1], Dataset[dcount+2], Dataset[dcount+3]]

  watermark = [full_watermark[wcount], full_watermark[wcount+1], full_watermark[wcount+2]]

  qDash1 = math.floor((weights[0]*gList[0] + weights[1]*gList[1] + weights[2]*gList[2] + weights[3]*gList[3]) / (weights[0] + weights[1] + weights[2] + weights[3]))

  qDash2 = gList[1] - gList[0]
  qDash3 = gList[2] - gList[0]
  qDash4 = gList[3] - gList[0]

  qCurl1 = qDash1
  qCurl2 = qDash2 * 2
  qCurl3 = qDash3 * 2
  qCurl4 = qDash4 * 2

  binary1 = bin(qCurl1)
  binary2 = bin(qCurl2)
  binary3 = bin(qCurl3)
  binary4 = bin(qCurl4)

  binaryList = [binary1, binary2, binary3, binary4]

  
  for y in range(3):
    if (watermark[y] == 0):
      binaryList[y+1] = unset_nth_bit(int(binaryList[y+1], 2), 0)
    elif (watermark[y] == 1):
      binaryList[y+1] = set_nth_bit(int(binaryList[y+1], 2),0)

  qDoubleDash1 = qCurl1 - math.floor((weights[1]*int(binaryList[1][2:], 2) + weights[2]*int(binaryList[2][2:], 2) + weights[3]*int(binaryList[3][2:], 2)) / (weights[0] + weights[1] + weights[2] + weights[3]))

  qDoubleDash2 = int(binaryList[1][2:], 2) + qDoubleDash1
  qDoubleDash3 = int(binaryList[2][2:], 2) + qDoubleDash1
  qDoubleDash4 = int(binaryList[3][2:], 2) + qDoubleDash1

  preservedDataset.append(qDoubleDash1)
  preservedDataset.append(qDoubleDash2)
  preservedDataset.append(qDoubleDash3)
  preservedDataset.append(qDoubleDash4)
  
  dcount += 4
  wcount += 3
  #if (first_column == 0):
  #first_column += 1

print(preservedDataset)