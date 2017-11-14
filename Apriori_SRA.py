#import libraries
import numpy
import csv
filename ='data.csv'     # fit for csv format
raw_data=open(filename, 'rt') #load dateset
reader=csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
mydata=list(map(tuple, reader))

#start from c1 and generate all 1-itemset
def Ck1_item(mydata):
    c1= [ ]
    for transaction in mydata:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    return list(map(frozenset, c1)) #the k-1 itemset used as the dict database
#create function using three parameters: dataset, candidatesets Ck and minimum support.
def scan_db(mydata, Ck, minsup):
    Candidate ={ }
    for ID in mydata:
        for cds in Ck:
            if cds.issubset(ID):
                Candidate.setdefault(cds,0)
                Candidate[cds] += 1   #compute support count
    total_items= float(len(mydata))
    re_list=[]
    support_db={}  #calculate support for the database
    for key in Candidate:
        support = Candidate[key]/total_items
        if support >=minsup:
            re_list.insert(0,key)
            support_db[key] = support
    return re_list, support_db

#generate k-items candidates
def createCk(Lk, k):
    re_list =[]
    len_Lk = len(Lk)
    for i in range(len_Lk):
        for j in range(i+1, len_Lk):
            L1 =list(Lk[i])[:k-2]; L2 =list(Lk[j])[:k-2]
            L1.sort(); L2.sort() # check if first k-2 items are equal
            if L1==L2:
                re_list.append(Lk[i] | Lk[j]) #then merge two itemset
    return re_list
    print len(re_list)

def frequent_item(mydata, minsup =0.01):
    C1= Ck1_item(mydata)
    Data=list(map(set, mydata))
    L1, support_db = scan_db(Data,C1,minsup)
    List = [L1]
    k =2
    while (len(List[k-2])>0):
        Ck = createCk(List[k-2], k)  # genrate length of k candidates
        Lk, supportk=scan_db(Data, Ck, minsup) #extract k-frequent itemset
        support_db.update(supportk)
        List.append(Lk)
        k += 1
    return List, support_db

#List contains all frequent itemset that pass the minsupport
def asso_rules(List, support_db, minconf=0.05):
    total_rules = []
    for i in range(1,len(List)):
        for fre_set in List[i]:
            H1=[frozenset([item]) for item in fre_set]
            if (i>1):
                rules_init(fre_set, H1, support_db, total_rules, minconf)
                #generate rules from initial frequent itemsets
            else:
                comp_conf(fre_set, H1, support_db, total_rules, minconf)
                #compute confidence of rules
    return total_rules
# evluate the rules that generated
def comp_conf(fre_set, H, support_db, total_rules, minconf=0.05):
    pruned_H =[]
    for init in H:
        conf = support_db[fre_set]/support_db[fre_set - init] #confidence computation
        Lift= conf/support_db[init] #caculate lift
        support =support_db[fre_set]/len(mydata)   #calculate support
        if conf >= minconf:
            print (fre_set-init,'-->', init ,'conf:',conf, 'Lift:', Lift, 'support',support)
            total_rules.append((fre_set-init,init, conf))
            pruned_H.append(init)
    return pruned_H
#generate candidate rules from previous dataset
def rules_init(fre_set, H, support_db, total_rules, minconf=0.05):
    m = len(H[0])
    if (len(fre_set)>(m+1)):
        Hm1=createCk(H,m+1)
        Hm1=comp_conf(fre_set, Hm1, support_db, total_rules, minconf)
        if (len(Hm1)>1):
            rules_init(fre_set, Hm1, support_db, total_rules, minconf)

import time
start_time=time.time()
List, support_db=frequent_item(mydata, minsup=0.01)
print("List of frequent itemset by Apriori with minsup of 0.01:\n")
print(List)
print("Time spent for frequent_itemset(A_0.01):\n")
print("--- %s seconds ---" % (time.time() - start_time))  #calcuate the time spent
print ("List of rules, confidence, lift, and support:\n")
print("List of rules by Apriori(0.01):\n")
rules = asso_rules(List, support_db, minconf=0.05)
c1=Ck1_item(mydata)
Count1, re_list = scan_db(mydata, c1, minsup=0.01)
print("Calculate the candidate C1 count: ")
print len(Count1)


#######
##***simple randome algorithm
## simpel random algorithm test

print("\n")
print("Simple Random Algorithm test(SRA):\n")
import numpy
import csv
filename ='data.csv'
raw_data=open(filename, 'rt')
reader=csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
mydata=list(map(tuple, reader))
subset_p1=(len(mydata)*0.1)         #change the sample size
simple_random_data = []
for i in range(0, int(subset_p1)):
    simple_random_data.append(mydata[i])

start_time=time.time()
List, support_db=frequent_item(simple_random_data, minsup=0.01)
print("List of frequent_itemset by SRA of p=10%:\n")
print(List)
print("Time spent for frequent_itemset:\n")#calcuate the time spent
print("- %s seconds -" % (time.time() - start_time))
print ("List of rules, confidence, lift, and support:\n")
print("List of rules by SRA with sample size of 10%:\n")
rules = asso_rules(List, support_db, minconf=0.05)
c1=Ck1_item(mydata)
Count1, re_list = scan_db(simple_random_data, c1, minsup=0.01)
print("Calculate the candidate C1 count: ")
print len(Count1)

##Do sample size of 20%
subset_p2=(len(mydata)*0.2)
simple_random_data2 = []
for i in range(0, int(subset_p2)):
    simple_random_data2.append(mydata[i])
start_time=time.time()
List, support_db=frequent_item(simple_random_data2, minsup=0.01)
print("List of frequent_itemset by SRA of p=20%:\n")
print(List)
print("Time spent for frequent_itemset:\n")#calcuate the time spent
print("- %s seconds -" % (time.time() - start_time))
print ("List of rules, confidence, lift, and support:\n")
print("List of rules by SRA with sample size of 20%:\n")
rules = asso_rules(List, support_db, minconf=0.05)
Count1, re_list = scan_db(simple_random_data2, c1, minsup=0.01)
print("Calculate the candidate C1 count: ")
print len(Count1)

##Do sample size of 30%
subset_p3=(len(mydata)*0.3)
simple_random_data3 = []
for i in range(0, int(subset_p3)):
    simple_random_data3.append(mydata[i])
start_time=time.time()
List, support_db=frequent_item(simple_random_data3, minsup=0.01)
print("List of frequent_itemset by SRA of p=30%:\n")
print(List)
print("Time spent for frequent_itemset:\n")#calcuate the time spent
print("- %s seconds -" % (time.time() - start_time))
print ("List of rules, confidence, lift, and support:\n")
print("List of rules by SRA with sample size of 30%:\n")
rules = asso_rules(List, support_db, minconf=0.05)
Count1, re_list = scan_db(simple_random_data3, c1, minsup=0.01)
print("Calculate the candidate C1 count: ")
print len(Count1)
####
print ("\n")
print("Change the minimum support value to 0.02, 0.05 and repeat, Done!!")
