#!/usr/bin/python
import time
import sys
import os
import math

PATH = sys.argv[0]
PATH = os.path.dirname(PATH)
PATH = os.path.abspath(PATH)+'/'
os.chdir(PATH)

SCRIPTS_PATH = "!script"

sys.path.append(PATH+"\\"+SCRIPTS_PATH)

from s2name import *
from s2resolution import *
from s2class import *
from s2frames import *
from s2framerate import *
from s2qp import *
from s2bitdepth import *

#from GenerateTasksHEVC import create_task_id_name_dec
#def create_task_id_name_dec(s,qp):
#    #Create task id name form sequence number and qp value
#   TASK_ID_NAME_TEMPLATE = "hevc_decoder_%s_%dx%d_%d_%dbit_QP%02d"
#    return TASK_ID_NAME_TEMPLATE%(s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

#TG_start
def create_log_file_name_hevc(s,qp,kat):
    #Create log filename from sequence and qp value
    LOG_FILENAME_TEMPLATE = kat+"\\%s_QP%02d_log.txt"
    return LOG_FILENAME_TEMPLATE%(s2name[s],qp)

    
def get_psnr_from_log_file_hevc(s,qp,kat):
    #Read log file
    hfile = open(create_log_file_name_hevc(s,qp,kat),"r")
    slines = hfile.readlines()
    hfile.close()
 
    for iline in range(len(slines)):
      if ("SUMMARY" in slines[iline]):
        tline = slines[iline+2].replace("\t","").split()
        #czasami cos sie sklei w logach
        num=len(tline)
        return [eval(tline[num-3]),eval(tline[num-2]),eval(tline[num-1])]
        

def get_filesize_from_log_file_hevc(s,qp,kat):
    #Read log file
    hfile = open(create_log_file_name_hevc(s,qp,kat),"r")
    slines = hfile.readlines()
    hfile.close()
    for iline in range(len(slines)):
        if ("Bytes written to file:" in slines[iline]):
            tline = slines[iline].replace("\t","").split()
            return int(eval(tline[4])*8*s2framerate[s]/s2frames[s]/1024)
  
def get_time_from_log_file_hevc(s,qp,kat):
    #Read log file
    hfile = open(create_log_file_name_hevc(s,qp,kat),"r")
    slines = hfile.readlines()
    hfile.close()
    for iline in range(len(slines)):
        if ("Total Time:" in slines[iline]):
            tline = slines[iline].replace("\t","").split()
            return eval(tline[2])  
#TG_end	

RUN_PATH = "log_enc"
    
liczba_watkow = 1

s2do = [
    "Traffic"            ,
    "PeopleOnStreet"     ,
    "Nebuta"             ,
    "SteamLocomotive"    ,
    "Kimono1"            ,
    "ParkScene"          ,
    "Cactus"             ,
    "BQTerrace"          ,
    "BasketballDrive"    ,
    "RaceHorses"         ,
    "BQMall"             ,
    "PartyScene"         ,
    "BasketballDrill"    ,
    "RaceHorsesLow"      ,
    "BQSquare"           ,
    "BlowingBubbles"     ,
    "BasketballPass"     ,
    "FourPeople"         ,
    "Johnny"             ,
    "KristenAndSara"     ,
    "BasketballDrillText",
    "ChinaSpeed"         ,
    "SlideEditing"       ,
    "SlideShow"          ,
    ]

           
# for seq in s2do:
    # for qp in s2qp[seq]:
        # print (str(seq)+'  '+str(qp))
        
        # task_id_name_dec = create_task_id_name_dec(seq,qp)
        
        # statsFileName = PATH+"\\"+RUN_PATH+"\\"+task_id_name_dec + '\\Stats.txt'
        
        # s = open(statsFileName,"r")
        # statsFile = s.readlines()
        # s.close()
        
        # stats = statsFile[0].split(" ")
        # Sum = 0
        # for i in range(0,25*35):
            # area = 2**((4-i%(35*5))+2)        
            # Sum += int(stats[i])*area*area
        
        # for i in range(0,25*35):
            # area = 2**((4-i%(35*5))+2)        
            # CuResQPTUSum[s2resolution[seq][0]][qp][i] += int(stats[i])*area*area/Sum
            # CuResQPTUSum2[s2resolution[seq][0]][qp][i] += ((int(stats[i])*area*area)/Sum)**2
        
# f = open("./res.txt", "a")
# for size in CuSize:
    # f.write("%d\n"%size)
    # for qp in s2qp[seq]:
        # f.write("%s;"%qp)
        # for i in range(0,25*35):
            # #f.write("%.10f;"%(CuResQPTUSum[size][qp][i]/CuSize[size]))
            # #f.write("%.10f;"%(2*math.sqrt(CuResQPTUSum2[size][qp][i]/CuSize[size]-(CuResQPTUSum[size][qp][i]/CuSize[size])**2)/math.sqrt(CuSize[size])))
        # f.write("\n")
# f.close()


#Store data in Excel
from win32com.client import constants, Dispatch
            
EXCEL_TEMPLATE = "template.xlsm"
CODING_SHEET_NAME = "Arkusz1"
            
ExcelApp = Dispatch("Excel.Application")
ExcelWorkbook = ExcelApp.Workbooks.Open(PATH+EXCEL_TEMPLATE)
print(PATH+"\\"+EXCEL_TEMPLATE)
ExcelSheet = ExcelWorkbook.Sheets(CODING_SHEET_NAME)

ExcelSheet.Cells(1,1).FormulaR1C1 = "HEVC"

ExcelSheet.Cells(2,1).FormulaR1C1 = "Sequence"
ExcelSheet.Cells(2,2).FormulaR1C1 = "QP"
ExcelSheet.Cells(2,3).FormulaR1C1 = "Bitrata [kb/s]"
ExcelSheet.Cells(2,4).FormulaR1C1 = "PSNR Y"
ExcelSheet.Cells(2,5).FormulaR1C1 = "PSNR U"
ExcelSheet.Cells(2,6).FormulaR1C1 = "PSNR V"
ExcelSheet.Cells(2,7).FormulaR1C1 = "Time[s]"
ExcelSheet.Cells(2,8).FormulaR1C1 = "Time/frame[s]"
seq_no = 0


for s in s2do:
    print(s2name[s])
    qp_num = len(s2qp[s]) # ile qp
    ExcelSheet.Cells(3+seq_no*qp_num,1).FormulaR1C1 = s2name[s]
    #for qp in s2qp[s]:
    for k in range (0,qp_num,1): #licznik po qp
        qp=s2qp[s][k]
        ExcelSheet.Cells(3+seq_no*qp_num+k,2).FormulaR1C1 = qp
        ExcelSheet.Cells(3+seq_no*qp_num+k,3).FormulaR1C1 = get_filesize_from_log_file_hevc(s,qp,RUN_PATH)
        PSNR=get_psnr_from_log_file_hevc(s,qp,RUN_PATH)
        ExcelSheet.Cells(3+seq_no*qp_num+k,4).FormulaR1C1 = PSNR[0]
        ExcelSheet.Cells(3+seq_no*qp_num+k,5).FormulaR1C1 = PSNR[1]
        ExcelSheet.Cells(3+seq_no*qp_num+k,6).FormulaR1C1 = PSNR[2]
        times=get_time_from_log_file_hevc(s,qp,RUN_PATH)
        ExcelSheet.Cells(3+seq_no*qp_num+k,7).FormulaR1C1 = times
        ExcelSheet.Cells(3+seq_no*qp_num+k,8).FormulaR1C1 = times/s2frames[s]
        
    seq_no += 1
print(PATH+"\\wyniki_TG.xlsm")
ExcelWorkbook.SaveAs(PATH+"wyniki_TG.xlsm")
ExcelApp.Quit()
print ("done")
