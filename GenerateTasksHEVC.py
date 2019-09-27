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
GEN_TRANSCODE = 1
#===============================================================================
GEN_ALL_CFG   = 0
#===============================================================================
GEN_SCRIPT_TYPES = ["tsk","bat","sh"] # skrypty taskow do wygenerowania
#GEN_SCRIPT_TYPES = ["tsk"] # skrypty taskow do wygenerowania
#===============================================================================
s2do = [
    # "Traffic"            ,
    "PeopleOnStreet"     ,
    # "Nebuta"             ,
    # "SteamLocomotive"    ,
    "Kimono1"            ,
    "ParkScene"          ,
    # "Cactus"             ,
    # "BQTerrace"          ,
    # "BasketballDrive"    ,
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

sys.path.append(PATH+"/"+SCRIPTS_PATH)

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

CFG_PATH_TRANS = "cfg_trans"
LOG_PATH_TRANS = "log_trans"
TASK_PATH_TRANS = "tasks%dof%d_hevc_trans"

CFG_TEMPLATE_FILENAME_TRANS = BASE_CONFIG_PATH+"/config_transcoder.cfg"
# CFG_TEMPLATE_FILENAME_TRANS = BASE_CONFIG_PATH+"/config_rewriter.cfg"

BIN_PATH_IN = "../bin"

#===============================================================================

MB_thread_usage_trans = {
    "A":[1600,1.0],
    "B":[1600,1.0],
    "C":[1600,1.0],
    "D":[1600,1.0],
    "E":[1600,1.0],
    "F":[1600,1.0]
}

#===============================================================================

FINAL_COMMENTS_TRANS = [ "Transcoding of HEVC" ]

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
    return path.replace('/',os.sep).replace('/',os.sep)
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
                ppp = path_fix(path + '/' + dir)
                if os.path.isdir(ppp):
                    safe_rmtree(ppp, ignore_errors=False)
    else:
        for i in range(len(COMPUTER_NUM)):
            ppp = path_fixed + (template % (i+1, len(COMPUTER_NUM)))
            if (not os.path.isdir(ppp)):
                safe_mkdir(ppp)
#===============================================================================

def create_bitstream_filename(s,qp):
    BITSTREAM_FILENAME_TEMPLATE = "../../%s/%s_%dx%d_%d_%dbit_bin_QP%01d.bin"
    return BITSTREAM_FILENAME_TEMPLATE%(BIN_PATH_IN,s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_yuv_bitstream_filename(s):
    YUV_BITSTREAM_FILENAME_TEMPLATE = "../../%s/%s_%dx%d_%d_%dbit.yuv"
    return YUV_BITSTREAM_FILENAME_TEMPLATEE%(BIN_PATH_IN,s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s])

def create_output_bitstream_filename(s,qp):
    OUTPUT_BITSTREAM_FILENAME_TEMPLATE = "../../%s/%s_%dx%d_%d_%dbit_bin_QP%02d_out.bin"
    return OUTPUT_BITSTREAM_FILENAME_TEMPLATE%(BIT_PATH,s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

#===========================TRANSCODER==========================================
def create_task_id_name_trans(s,qp): 
    #Create task id name form sequence number and qp value
    TASK_ID_NAME_TEMPLATE = "hevc_transcoder_%s_%dx%d_%d_%dbit_QP%02d"
    return TASK_ID_NAME_TEMPLATE%(s2name[s],s2resolution[s][0],s2resolution[s][1],s2framerate[s],s2bitdepth[s],qp)

def create_task_filename_trans(task_idcn,task_id_name):
    #Create task id name form sequence number and qp value
    TASK_FILENAME_TEMPLATE = "../%s/%s"
    return (TASK_FILENAME_TEMPLATE%(TASK_PATH_TRANS,task_id_name))%(task_idcn,len(COMPUTER_NUM))

def create_cfg_filename_trans(s,qp):
    #Create task id name form sequence number and qp value
    CFG_FILENAME_TEMPLATE = "../../%s/%s_QP%02d.cfg"
    return CFG_FILENAME_TEMPLATE%(CFG_PATH_TRANS,s2name[s],qp)

def create_log_filename_trans(s,qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "../../%s/%s_QP%02d_log.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_TRANS,s2name[s],qp)

def create_err_filename_trans(s,qp):
    #Create task id name form sequence number and qp value
    LOG_FILENAME_TEMPLATE = "../../%s/%s_QP%02d_err.txt"
    return LOG_FILENAME_TEMPLATE%(LOG_PATH_TRANS,s2name[s],qp)

def create_commandline_trans():
    #Create task id name form sequence number and qp value
    COMMAND_LINE_TEMPLATE = "../../%s/HEVC.out"
    return COMMAND_LINE_TEMPLATE%(BIN_PATH)

def create_argline_trans(s,qp):
    #Create task id name form sequence number and qp value
    ARG_LINE_TEMPLATE = "-T -c %s"
    return ARG_LINE_TEMPLATE%(create_cfg_filename_trans(s, qp))

def create_psnrline_trans():
    #Create task id name form sequence number and qp value
    PSNR_LINE_TEMPLATE = "../../%s/psnr.out"
    return PSNR_LINE_TEMPLATE%(BIN_PATH)

def create_enc_psnr_argline_trans(s,qp):
    #Create task id name form sequence number and qp value
    ENC_PSNR_ARGLINE_TEMPLATE = "-i1 %s -i2 %s -dx %d -dy %d"
    return ENC_PSNR_ARGLINE_TEMPLATE%(create_yuv_bitstream_filename(s),create_output_bitstream_filename(s,qp),s2resolution[s][0],s2resolution[s][1])

def create_trans_psnr_argline_trans(s,qp):
    #Create task id name form sequence number and qp value
    TRANS_PSNR_ARGLINE_TEMPLATE = "-i1 %s -i2 %s -dx %d -dy %d"
    return TRANS_PSNR_ARGLINE_TEMPLATE%(create_yuv_bitstream_filename(s),create_bitstream_filename(s,qp),s2resolution[s][0],s2resolution[s][1])

#===============================================================================

def prepare_paths_or_del(remove_or_create):
    #global PATH
    #global COMPUTER_NUM
    #global BIT_PATH
    #global CFG_PATH_TRANS
    #global LOG_PATH_TRANS
    #global RUN_PATH

    if (GEN_TRANSCODE|GEN_ALL_CFG|remove_or_create):

        ensure_path_or_del(remove_or_create, PATH+"/"+BIT_PATH)
        ensure_path_or_del(remove_or_create, PATH+"/"+CFG_PATH_TRANS)
        ensure_path_or_del(remove_or_create, PATH+"/"+LOG_PATH_TRANS)
        ensure_path_or_del(remove_or_create, PATH+"/"+RUN_PATH)

        ensure_path_or_del_computer_num(remove_or_create, PATH+"/", TASK_PATH_TRANS)

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

def prepare_config_trans(s,qp):
    ref_cfg_file = open("../../"+CFG_TEMPLATE_FILENAME_TRANS,'r')
    config = ref_cfg_file.readlines()
    ref_cfg_file.close()

    config = modify_parameter(config, "InputBitstreamFile", create_bitstream_filename(s,qp))
    config = modify_parameter(config, "OutputBitstreamFile", create_output_bitstream_filename(s,qp))

    #config = modify_parameter(config, "RewritingMode", mode)
    #config = modify_parameter(config, "InputBitDepth", str(s2bitdepth[s]))
    #config = modify_parameter(config, "OutputBitDepth", str(s2bitdepth[s]))
    #
    #config = modify_parameter(config, "SourceWidth", str(s2resolution[s][0]))
    #config = modify_parameter(config, "SourceHeight", str(s2resolution[s][1]))
    #
    #config = modify_parameter(config, "FrameRate", str(s2framerate[s]))
    #
    #if (MAX_FRAMES<=0):
    #    frames = s2frames[s]
    #else:
    #    frames = min(MAX_FRAMES, s2frames[s])
    #config = modify_parameter(config, "FramesToBeEncoded", str(frames))
    #
    #config = modify_parameter(config, "QP", str(qp))
    
    cfg_filename = create_cfg_filename_trans(s, qp)
    cfg = open(cfg_filename,'w')
    cfg.writelines(config)
    cfg.close()

    return cfg_filename

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

confirm = mx_input("press any key to start (or type 'clear' to clear directory and exit)? ")

if ("clear" in confirm):
    #confirm = mx_input("WARNING - CLEANING ENVIRONMENT - TYPE 'yes'\n")
    mx_input("press any key to start CLEANING (confirm)")

    prepare_paths_or_del(1)
    exit("")

mx_input("press any key to start (confirm)")

prepare_paths_or_del(0) #Create necessary paths

#experiment_seed = PATH.replace('/','/').rpartition('/')
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
    for qp in range(10,52): #Loop over qp range for given seqence

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

#        transcoding
        task_id_name_trans = create_task_id_name_trans(s,qp)
        if (GEN_TRANSCODE|GEN_ALL_CFG):
            ensure_path(PATH+"/"+RUN_PATH+"/"+task_id_name_trans)
            os.chdir(PATH+"/"+RUN_PATH+"/"+task_id_name_trans)

            prepare_config_trans(s,qp)

        log_filename   = create_log_filename_trans(s,qp)
        err_filename   = create_err_filename_trans(s,qp)
        commandline    = create_commandline_trans()
        argline        = create_argline_trans(s,qp)
        psnrline       = create_psnrline_trans()
        enc_psnrline   = create_enc_psnr_argline_trans(s,qp)
        trans_psnrline = create_trans_psnr_argline_trans(s,qp)

        os.chdir(PATH+"/"+RUN_PATH+"/")
        if (GEN_TRANSCODE):
            new_task_filename = create_task_filename_trans(task_idcn,task_id_name_trans)
            generate_task_v2(GEN_SCRIPT_TYPES, new_task_filename, RUN_PATH+"/"+task_id_name_trans, [commandline,argline], [log_filename,err_filename], MB_thread_usage_trans[s2class[s]], USER, sys.argv[0], EMAIL_ENABLE, EMAIL_RECIPIENTS, FINAL_COMMENTS_TRANS, last_task_filename)
            last_task_filename = new_task_filename

for i in range(len(COMPUTER_NUM)):
    print("TESTS FOR ", (i+1), ":  ", tests[i]);
