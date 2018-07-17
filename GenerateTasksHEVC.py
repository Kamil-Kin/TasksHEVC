# -*- coding: utf-8 -*-
#===============================================================================
EMAIL_ENABLE = True
EMAIL_RECIPIENTS = [ 'jstankowski@multimedia.edu.pl' ]
#===============================================================================
#COMPUTER_NUM = [1,9]   # Liczba komputerow
COMPUTER_NUM = 1   # Liczba komputerow
#===============================================================================
MAX_FRAMES = 0
#===============================================================================
GEN_ENCODE                          = 1
GEN_DECODE                          = 0
# ------------------------------------
GEN_REN_DEC                         = 0
GEN_REN_DEC_TESTMISMATCH_MV_DEC     = 0
GEN_REN_DEC_TESTMISMATCH_RM_DEC     = 0
GEN_REN_DEC_TESTMISMATCH_RM_DEC_REC = 0
#===============================================================================
GEN_ALL_CFG              = 0
#===============================================================================
GEN_ANY_PYTHON = GEN_REN_DEC+GEN_REN_DEC_TESTMISMATCH_MV_DEC+GEN_REN_DEC_TESTMISMATCH_RM_DEC+GEN_REN_DEC_TESTMISMATCH_RM_DEC_REC
#===============================================================================
GEN_SCRIPT_TYPES = ["tsk","bat","sh"] # skrypty taskow do wygenerowania
#GEN_SCRIPT_TYPES = ["tsk"] # skrypty taskow do wygenerowania
#===============================================================================
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
#===============================================================================
import time
import sys
import os
import getpass
import shutil
import fnmatch
import random

PATH = sys.argv[0]
PATH = os.path.dirname(PATH)
PATH = os.path.abspath(PATH)

SCRIPTS_PATH = "!script"

sys.path.append(PATH+"\\"+SCRIPTS_PATH)

from task_generation_v2 import *
from s2name import *
from s2resolution import *
from s2class import *
from s2frames import *
from s2framerate import *
from s2qp import *
from s2bitdepth import *

USER = getpass.getuser()

BASE_CONFIG_PATH = "!base_config"
BIN_PATH = "!bin"

BIT_PATH = "bit"
RUN_PATH = "run"
REC_PATH = "rec"
DEC_PATH = "dec"

CFG_PATH_ENC = "cfg_enc"
LOG_PATH_ENC = "log_enc"
TASK_PATH_ENC = "tasks%dof%d_hevc_enc"

LOG_PATH_DEC = "log_dec"
TASK_PATH_DEC = "tasks%dof%d_hevc_dec"

DEC_OK_PATH = "dec_ok"
DEC_WRONG_PATH = "dec_wrong"
TASK_PATH_PYT = "tasks%dof%d_hevc_python"
CFG_PATH_PYT = "cfg_pyt"
LOG_PATH_PYT = "log_pyt"

CFG_TEMPLATE_FILENAME_ENC = BASE_CONFIG_PATH+"\\encoder_randomaccess_main.cfg"

SEQ_PATH = "..\\seq"

#===============================================================================    

MB_thread_usage_enc = {
    "A":[1600,1.0],
    "B":[1600,1.0],
    "C":[1600,1.0],
    "D":[1600,1.0],
    "E":[1600,1.0],
    "F":[1600,1.0]
}

MB_thread_usage_dec = {
    "A":[800,1.0],
    "B":[800,1.0],
    "C":[800,1.0],
    "D":[800,1.0],
    "E":[800,1.0],
    "F":[800,1.0]
}

#===============================================================================    

FINAL_COMMENTS_ENC = [ "Encoding of HEVC" ]

FINAL_COMMENTS_DEC = [ "Decoding of HEVC" ]

FINAL_COMMENTS_PYT = [ "Pythoing of HEVC" ]

#===============================================================================

try:
    #list
    sum = 0
    for w in COMPUTER_NUM:
        sum += w
    for i in range(len(COMPUTER_NUM)):
        COMPUTER_NUM[i] = COMPUTER_NUM[i]/sum
except:
    try:
        #integer
        num = COMPUTER_NUM
        COMPUTER_NUM = []
        for i in range(num):
            COMPUTER_NUM.append(1.0/num)
    except:
        raise

#===============================================================================
# procedures
#===============================================================================
def path_fix(path):
    return path.replace('\\',os.sep).replace('/',os.sep)
#===============================================================================
def safe_rmtree(path, ignore_errors):
    try:
        shutil.rmtree(path, ignore_errors)
    except:
        time.sleep(5)
        try:
            shutil.rmtree(path, ignore_errors)
        except:
            raise
    return
#===============================================================================
def safe_mkdir(path):
    try:
        os.mkdir(path)
    except:
        time.sleep(5)
        try:
            os.mkdir(path)
        except:
            raise
    return
#===============================================================================
def remove_path(dir):
    ddd = path_fix(dir)
    if (os.path.isdir(ddd)):
        safe_rmtree(ddd, ignore_errors=False)
#===============================================================================
def ensure_path(path):
    ppp = path_fix(path)
    if (not os.path.isdir(ppp)):
        safe_mkdir(ppp)
#===============================================================================
def ensure_path_or_del(remove_or_create, path):
    ppp = path_fix(path)
    if (remove_or_create):
        if (os.path.isdir(ppp)):
            safe_rmtree(ppp, ignore_errors=False)
    else:
        if (not os.path.isdir(ppp)):
            safe_mkdir(ppp)
#===============================================================================
def ensure_path_or_del_computer_num(remove_or_create, path, template):
    global COMPUTER_NUM
    path_fixed = path_fix(path)
    if (remove_or_create):
        template = template.replace("%d","*")
        dir_list = os.listdir(path_fix(path))
        for dir in dir_list:
            if fnmatch.fnmatch(dir, template):
                ppp = path_fix(path + '\\' + dir)
                if os.path.isdir(ppp):
                    safe_rmtree(ppp, ignore_errors=False)
    else:
        for i in range(len(COMPUTER_NUM)):
            ppp = path_fixed + (template % (i+1, len(COMPUTER_NUM)))
            if (not os.path.isdir(ppp)):
                safe_mkdir(ppp)

#===============================================================================

def create_bitstream_filename(s,qp):
    BITSTREAM_FILENAME_TEMPLATE = "..\\..\\%s\\%s_%dx%d_%d_%dbit_bin_QP%02d.bin"
    return BITSTREAM_FILENAME_TEMPLATE%(BIT_PATH,s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_decoded_filename(s,qp):
    DECODED_FILENAME_TEMPLATE = "..\\..\\%s\\%s_%dx%d_%d_%dbit_QP%02d.yuv"
    return DECODED_FILENAME_TEMPLATE%(DEC_PATH,s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_video_filename(s):
    TEMPLATE = "..\\..\\%s\\%s\\%s_%dx%d_%d_%dbit.yuv"
    return TEMPLATE%(SEQ_PATH,s2class[s],s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s])

def create_reconstructed_filename(s, qp):
    TEMPLATE = "..\\..\\%s\\%s_%dx%d_%d_%dbit_QP%02d.yuv"
    return TEMPLATE%(REC_PATH,s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

#===============================================================================
def create_task_id_name_enc(s,qp):
    #Create task id name form sequence number and qp value
    TASK_ID_NAME_TEMPLATE = "hevc_encoder_%s_%dx%d_%d_%dbit_QP%02d"
    return TASK_ID_NAME_TEMPLATE%(s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_task_filename_enc(task_idcn,task_id_name):
    #Create task id name form sequence number and qp value
    TASK_FILENAME_TEMPLATE = "..\\%s\\%s"
    return (TASK_FILENAME_TEMPLATE%(TASK_PATH_ENC,task_id_name))%(task_idcn,len(COMPUTER_NUM))

def create_cfg_filename_enc(s, qp):
    #Create task id name form sequence number and qp value
    CFG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d.cfg"
    return CFG_FILENAME_TEMPLATE%(CFG_PATH_ENC,s2name[s],qp)

def create_log_filename_enc(s, qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d_log.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_ENC,s2name[s],qp)

def create_err_filename_enc(s, qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d_err.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_ENC,s2name[s],qp)

def create_commandline_enc():
    #Create task id name form sequence number and qp value
    COMMAND_LINE_TEMPLATE = "..\\..\\%s\\TAppEncoder.exe"
    return COMMAND_LINE_TEMPLATE%(BIN_PATH) 

def create_argline_enc(s,qp):
    #Create task id name form sequence number and qp value
    ARG_LINE_TEMPLATE = "-c %s"
    return ARG_LINE_TEMPLATE%(create_cfg_filename_enc(s, qp))

#===============================================================================
def create_task_id_name_dec(s,qp):
    #Create task id name form sequence number and qp value
    TASK_ID_NAME_TEMPLATE = "hevc_decoder_%s_%dx%d_%d_%dbit_QP%02d"
    return TASK_ID_NAME_TEMPLATE%(s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_task_filename_dec(task_idcn,task_id_name):
    #Create task id name form sequence number and qp value
    TASK_FILENAME_TEMPLATE = "..\\%s\\%s"
    return (TASK_FILENAME_TEMPLATE%(TASK_PATH_DEC,task_id_name))%(task_idcn,len(COMPUTER_NUM))   

def create_log_filename_dec(s, qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d_log.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_DEC,s2name[s],qp)

def create_err_filename_dec(s, qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d_err.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_DEC,s2name[s],qp)

def create_commandline_dec():
    #Create task id name form sequence number and qp value
    COMMAND_LINE_TEMPLATE = "..\\..\\%s\\TAppDecoder.exe"
    return COMMAND_LINE_TEMPLATE%(BIN_PATH) 

def create_argline_dec(s,qp):
    #Create task id name form sequence number and qp value
    ARG_LINE_TEMPLATE = "-b %s -o %s "
    return ARG_LINE_TEMPLATE%(create_bitstream_filename(s, qp),create_decoded_filename(s,qp))

#===============================================================================

def create_task_id_name_pyt(s,qp):
    #Create task id name form sequence number and qp value
    TASK_ID_NAME_TEMPLATE = "hevc_python_%s_00_%dx%d_%d_%dbit_QP%02d"
    return TASK_ID_NAME_TEMPLATE%(s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_task_filename_pyt(task_idcn,task_id_name):
    #Create task id name form sequence number and qp value
    TASK_FILENAME_TEMPLATE = "..\\%s\\%s"
    return (TASK_FILENAME_TEMPLATE%(TASK_PATH_PYT,task_id_name))%(task_idcn,len(COMPUTER_NUM))

def create_cfg_filename_pyt(s, qp):
    #Create task id name form sequence number and qp value
    CFG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d.py"
    return CFG_FILENAME_TEMPLATE%(CFG_PATH_PYT,s2name[s],qp)

def create_log_filename_pyt(s, qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d_log.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_PYT,s2name[s],qp)
    
def create_err_filename_pyt(s, qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "..\\..\\%s\\%s_QP%02d_err.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_PYT,s2name[s],qp)
    
def create_argline_pyt(s,qp):
    #Create task id name form sequence number and qp value
    return "-x"

#===============================================================================    

def prepare_paths_or_del(remove_or_create):
    #global PATH
    #global COMPUTER_NUM
    #global BIT_PATH
    #global CFG_PATH_ENC
    #global LOG_PATH_ENC
    #global RUN_PATH
    #global REC_PATH
    #global TASK_PATH_ENC

    #global LOG_PATH_DEC
    #global TASK_PATH_DEC

    if (GEN_ENCODE|GEN_ALL_CFG|remove_or_create):

        ensure_path_or_del(remove_or_create, PATH+"\\"+BIT_PATH)
        ensure_path_or_del(remove_or_create, PATH+"\\"+CFG_PATH_ENC)
        ensure_path_or_del(remove_or_create, PATH+"\\"+LOG_PATH_ENC)
        ensure_path_or_del(remove_or_create, PATH+"\\"+REC_PATH)
        ensure_path_or_del(remove_or_create, PATH+"\\"+RUN_PATH)

        ensure_path_or_del_computer_num(remove_or_create, PATH+"\\", TASK_PATH_ENC)

    if (GEN_DECODE|GEN_ALL_CFG|remove_or_create):
        ensure_path_or_del(remove_or_create, PATH+"\\"+DEC_PATH)
        ensure_path_or_del(remove_or_create, PATH+"\\"+RUN_PATH)
        ensure_path_or_del(remove_or_create, PATH+"\\"+LOG_PATH_DEC)

        ensure_path_or_del_computer_num(remove_or_create, PATH+"\\", TASK_PATH_DEC)

    if (GEN_ANY_PYTHON|GEN_ALL_CFG|remove_or_create):
        ensure_path_or_del(remove_or_create, PATH+"\\"+DEC_OK_PATH)
        ensure_path_or_del(remove_or_create, PATH+"\\"+DEC_WRONG_PATH)
        ensure_path_or_del(remove_or_create, PATH+"\\"+CFG_PATH_PYT)
        ensure_path_or_del(remove_or_create, PATH+"\\"+LOG_PATH_PYT)

        ensure_path_or_del_computer_num(remove_or_create, PATH+"\\", TASK_PATH_PYT)

    return
#===============================================================================
def modify_parameter(config, new_parameter_name, new_parameter_value):
    new_config = []
    need_append = 1
    for line in config:
        if new_parameter_name in line:
            line = line.rstrip()
            temp = line.partition("#")
            parameter = temp[0]
            comment = temp[2]
            temp = parameter.partition(":")
            parameter_name  = temp[0]
            parameter_value = temp[2]
            parameter_value = str(new_parameter_value)
            if(parameter_name.rstrip() == new_parameter_name):
                new_config.append("%s: %s     # %s\n" % (parameter_name, new_parameter_value, comment))
                need_append = 0
            else:
                new_config.append(line+"\n")
        else:
            new_config.append(line)

    if (need_append):
        new_config.append(new_parameter_name+": "+new_parameter_value+"\n")
    return new_config
#===============================================================================
def prepare_config_enc(s,qp):
    ref_cfg_file = open("..\\..\\"+CFG_TEMPLATE_FILENAME_ENC,'r')
    config = ref_cfg_file.readlines()
    ref_cfg_file.close()

    config = modify_parameter(config,"InputFile",create_video_filename(s))
    config = modify_parameter(config,"ReconFile",create_reconstructed_filename(s, qp))
    config = modify_parameter(config, "BitstreamFile", create_bitstream_filename(s,qp))

    config = modify_parameter(config, "InputBitDepth", str(s2bitdepth[s]))
    config = modify_parameter(config, "OutputBitDepth", str(s2bitdepth[s]))

    config = modify_parameter(config, "SourceWidth", str(s2resolution[s][0]))
    config = modify_parameter(config, "SourceHeight", str(s2resolution[s][1]))

    config = modify_parameter(config, "FrameRate", str(s2framerate[s]))

    if (MAX_FRAMES<=0):
        frames = s2frames[s]
    else:
        frames = min(MAX_FRAMES, s2frames[s])
    config = modify_parameter(config, "FramesToBeEncoded", str(frames))

    config = modify_parameter(config, "QP", str(qp))

    cfg_filename = create_cfg_filename_enc(s, qp)
    cfg = open(cfg_filename,'w')
    cfg.writelines(config)
    cfg.close()

    return cfg_filename

def prepare_config_pyt(out_config_filename, sequence, qp):

    mysep = os.sep
    mysep = mysep.replace('\\', '\\\\')

    config_pyt = []
    config_pyt.append("# -*- coding: utf8 -*-\n")
    config_pyt.append("import sys\n")
    config_pyt.append("import os\n")
    config_pyt.append("import shutil\n")
    config_pyt.append("import getpass\n")
    config_pyt.append("\n")
    config_pyt.append("PATH = sys.argv[0]\n")
    config_pyt.append("PATH = os.path.dirname(PATH)\n")
    config_pyt.append("PATH = os.path.abspath(PATH)\n")
    config_pyt.append("\n")
    config_pyt.append('REC="..'+mysep+'..'+mysep+REC_PATH+mysep+'"\n')
    config_pyt.append('DEC="..'+mysep+'..'+mysep+DEC_PATH+mysep+'"\n')
    config_pyt.append('DEC_OK="..'+mysep+'..'+mysep+DEC_OK_PATH+mysep+'"\n')
    config_pyt.append('DEC_WRONG="..'+mysep+'..'+mysep+DEC_WRONG_PATH+mysep+'"\n')
    config_pyt.append("\n")
    config_pyt.append("def file_cmp(f1, f2):\n")
    config_pyt.append("    bufsize = 1024*1024\n")
    config_pyt.append("    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:\n")
    config_pyt.append("        while True:\n")
    config_pyt.append("            b1 = fp1.read(bufsize)\n")
    config_pyt.append("            b2 = fp2.read(bufsize)\n")
    config_pyt.append("            if b1 != b2:\n")
    config_pyt.append("                return False\n")
    config_pyt.append("            if not b1:\n")
    config_pyt.append("                return True\n")
    config_pyt.append("\n")
    config_pyt.append("def zero_file(filename):\n")
    config_pyt.append("    fp = open(filename,'w')\n")
    config_pyt.append("    fp.close()\n")
    config_pyt.append("\n")
    config_pyt.append("def rename_dec_file(dst, src):\n")
    config_pyt.append("    if os.path.isfile(src):\n")
    config_pyt.append("        shutil.move(src, dst)\n")

    config_pyt.append("\n")
    config_pyt.append("def compare_files(file_name1,file_name2):\n")
    config_pyt.append("    frec = file_name1\n")
    config_pyt.append("    fdec = file_name2\n")
    config_pyt.append("    file_name=os.path.basename(file_name2)\n")
    config_pyt.append("    if os.path.isfile(frec):\n")
    config_pyt.append("        if os.path.isfile(fdec):\n")
    if (GEN_REN_DEC_TESTMISMATCH_MV_DEC):
        config_pyt.append("            if (file_cmp(frec,fdec)):\n")
        config_pyt.append("                print('OK  '+file_name+' - MOVING TO DEC_OK')\n")
        config_pyt.append("                shutil.move(fdec, DEC_OK+file_name)\n")
        config_pyt.append("            else:\n")    
        config_pyt.append("                print('BAD '+file_name+' - MOVING TO DEC_WRONG')\n")
        config_pyt.append("                shutil.move(fdec, DEC_WRONG+file_name)\n")
    elif (GEN_REN_DEC_TESTMISMATCH_RM_DEC|GEN_REN_DEC_TESTMISMATCH_RM_DEC_REC):
        config_pyt.append("            if (file_cmp(frec,fdec)):\n")
        config_pyt.append("                print('OK  '+file_name+' - TOUCHING IN DEC_OK')\n")
        config_pyt.append("                os.remove(fdec)\n")
        config_pyt.append("                zero_file(DEC_OK+file_name)\n")
        if (GEN_REN_DEC_TESTMISMATCH_RM_DEC_REC):
            config_pyt.append("                os.remove(frec)\n")
        config_pyt.append("            else:\n")
        config_pyt.append("                print('BAD '+file_name+' - MOVING TO DEC_WRONG')\n")
        config_pyt.append("                shutil.move(fdec, DEC_WRONG+file_name)\n")
    else:
        config_pyt.append("            print('')\n")

    config_pyt.append("\n")

    #name = create_decoded_filename(s,qp).replace('/',os.sep).replace('\\',os.sep).replace('\\', '\\\\')
    #config_pyt.append('rename_dec_file("'+create_reconstructed_filename(s, qp)+'","'+name+'")\n')

    config_pyt.append('compare_files("'+create_reconstructed_filename(s, qp).replace('/',os.sep).replace('\\',os.sep).replace('\\', '\\\\')+'","'+create_decoded_filename(s,qp).replace('/',os.sep).replace('\\',os.sep).replace('\\', '\\\\')+'")\n')

    fp = open(out_config_filename,'wt')
    fp.writelines(config_pyt)
    fp.close()

def mx_input(str):
    try:
        sys.stdout.write(str)
        sys.stdout.flush()
        res = sys.stdin.readline()  
    except:
        return "-"
    return res

#===============================================================================
#Main Loop
#===============================================================================

print("############################################################")
print("GENERATING HTM ENCODING/DECODING/RENDERING TASK START")
print("############################################################")

if (GEN_ANY_PYTHON>1):
    print("Too many options: GEN_ANY_PYTHON")
    exit(0)

confirm = mx_input("press any key to start (or type 'clear' to clear directory and exit)? ")

if ("clear" in confirm):
    #confirm = mx_input("WARNING - CLEANING ENVIRONMENT - TYPE 'yes'\n")
    mx_input("press any key to start CLEANING (confirm)")

    prepare_paths_or_del(1)
    exit("")

mx_input("press any key to start (confirm)")

prepare_paths_or_del(0) #Create necesary paths 

#experiment_seed = PATH.replace('/','\\').rpartition('\\')
experiment_seed = os.path.basename(PATH)
random.seed(experiment_seed);
computers = []
for i in range(0,len(COMPUTER_NUM)):
    computers.append(i)
random.shuffle(computers)
print("EXPERIMENT SEED:", experiment_seed, ":  ",computers);

tests_done = 0
tests = []
for i in range(len(COMPUTER_NUM)):
    tests.append(0)

#test_idx=0
for s in s2do: #Loop over every sequence to do
    for qp in range(1,51): #Loop over qp range for given seqence

        best_i = -1
        best_dif = 0
        for j in range(len(COMPUTER_NUM)):
            i = computers[j]
            if (COMPUTER_NUM[i]>0):
                dif = COMPUTER_NUM[i] - tests[i]/float(max(tests_done,1))
                if ((dif>best_dif) | (best_i<0)):
                    best_dif = dif
                    best_i   = i

        tests_done += 1

        tests[best_i] += 1
        task_idcn = best_i+1

        print("  HTM GEN("+str(task_idcn)+"/"+str(len(COMPUTER_NUM)) + ")   "+s2name[s]+" QP:"+str(qp) )
        last_task_filename = ""

#       python
        task_id_name_pyt = create_task_id_name_pyt(s,qp)

        if (GEN_ANY_PYTHON|GEN_ALL_CFG):

            ensure_path(PATH+"\\"+RUN_PATH+"\\"+task_id_name_pyt)

            os.chdir(PATH+"\\"+RUN_PATH+"\\"+task_id_name_pyt)

        log_filename = create_log_filename_pyt(s,qp)
        err_filename = create_err_filename_pyt(s,qp)
        commandline  = create_cfg_filename_pyt(s,qp)
        argline      = create_argline_pyt(s,qp)

        os.chdir(PATH+"\\"+RUN_PATH+"\\")
        if (GEN_ANY_PYTHON):
            new_task_filename = create_task_filename_pyt(task_idcn,task_id_name_pyt)

            generate_task_v2(GEN_SCRIPT_TYPES, new_task_filename, RUN_PATH+"\\"+task_id_name_pyt, [commandline,argline], [log_filename,err_filename],[10,1], USER, sys.argv[0], EMAIL_ENABLE, EMAIL_RECIPIENTS, FINAL_COMMENTS_PYT, last_task_filename)
            last_task_filename = new_task_filename

#       decoding
        task_id_name_dec = create_task_id_name_dec(s,qp)

        if (GEN_DECODE|GEN_ALL_CFG):

            ensure_path(PATH+"\\"+RUN_PATH+"\\"+task_id_name_dec)
            os.chdir(PATH+"\\"+RUN_PATH+"\\"+task_id_name_dec)

            prepare_config_pyt( create_cfg_filename_pyt(s,qp), s, qp)

        log_filename = create_log_filename_dec(s,qp)
        err_filename = create_err_filename_dec(s,qp)
        commandline  = create_commandline_dec()
        argline      = create_argline_dec(s,qp)

        os.chdir(PATH+"\\"+RUN_PATH+"\\")
        if (GEN_DECODE):
            new_task_filename = create_task_filename_dec(task_idcn,task_id_name_dec)

            generate_task_v2(GEN_SCRIPT_TYPES, new_task_filename, RUN_PATH+"\\"+task_id_name_dec, [commandline,argline], [log_filename,err_filename],MB_thread_usage_dec[s2class[s]], USER, sys.argv[0], EMAIL_ENABLE, EMAIL_RECIPIENTS, FINAL_COMMENTS_DEC, last_task_filename)
            last_task_filename = new_task_filename


#       encoding
        task_id_name_enc = create_task_id_name_enc(s,qp)

        if (GEN_ENCODE|GEN_ALL_CFG):

            ensure_path(PATH+"\\"+RUN_PATH+"\\"+task_id_name_enc)
            os.chdir(PATH+"\\"+RUN_PATH+"\\"+task_id_name_enc)

            prepare_config_enc(s,qp)

        log_filename = create_log_filename_enc(s,qp)
        err_filename = create_err_filename_enc(s,qp)
        commandline  = create_commandline_enc()
        argline      = create_argline_enc(s,qp)

        os.chdir(PATH+"\\"+RUN_PATH+"\\")
        if (GEN_ENCODE):
            new_task_filename = create_task_filename_enc(task_idcn,task_id_name_enc)
            generate_task_v2(GEN_SCRIPT_TYPES, new_task_filename, RUN_PATH+"\\"+task_id_name_enc, [commandline,argline], [log_filename,err_filename],MB_thread_usage_enc[s2class[s]], USER, sys.argv[0], EMAIL_ENABLE, EMAIL_RECIPIENTS, FINAL_COMMENTS_ENC, last_task_filename)
            last_task_filename = new_task_filename


for i in range(len(COMPUTER_NUM)):
    print("TESTS FOR ", (i+1), ":  ", tests[i]);
