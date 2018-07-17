# -*- coding: utf-8 -*-


def generate_task_v2(script_types, taskfilename, run_path, command_line, log_names, MB_thread_usage, user, script, emails_en, emails, final_comments, next_script):
    
    if "tsk" in script_types:
        new_task_file = open( taskfilename+".tsk", 'w')
        new_task_file.write("#"+str(MB_thread_usage[0])+"\n")
        new_task_file.write("#"+str(MB_thread_usage[1])+"\n")
        new_task_file.write("#"+user+"\n")
        new_task_file.write("#"+script+"\n")
        new_task_file.write("#")
        if emails_en:
            for email in emails:
                new_task_file.write(email+" ")
        
        new_task_file.write("\n")
        new_task_file.write("#"+run_path+"\n")
        new_task_file.write("#"+command_line[0]+"\n")
        new_task_file.write("#")
        for cmdi in range(1,len(command_line)):
            new_task_file.write(command_line[cmdi]+" ")
        new_task_file.write("\n")
        new_task_file.write("#"+log_names[0]+"\n")
        new_task_file.write("#"+log_names[1]+"\n")
        if len(next_script)>0:
            new_task_file.write("#"+next_script+".tsk\n");
        else:
            new_task_file.write("#\n");

        for comment in final_comments:
            new_task_file.write("#"+comment+"\n")
        new_task_file.close()

    if "sh" in script_types:
        new_task_file = open( taskfilename+".sh", 'w')
        new_task_file.write("#!/bin/sh\n")
        new_task_file.write("pushd ../"+run_path.replace("\\","/")+"\n")
        new_task_file.write("./"+command_line[0].replace("\\","/")+" ")
        for cmdi in range(1,len(command_line)):
            new_task_file.write(command_line[cmdi].replace("\\","/")+" ")
        new_task_file.write(" 1>")
        new_task_file.write(log_names[0].replace("\\","/")+" 2>")
        new_task_file.write(log_names[1].replace("\\","/")+"\n")
        new_task_file.write("popd\n");
        if len(next_script)>0:
            new_task_file.write("./"+next_script.replace("\\","/")+".sh\n");

        for comment in final_comments:
            new_task_file.write("#"+comment+"\n")

        new_task_file.close()

    if "bat" in script_types:
 
        new_task_file = open( taskfilename + '.bat', 'w')
        new_task_file.write("pushd ..\\"+run_path+"\n")
        new_task_file.write(command_line[0]+" ")
        for cmdi in range(1,len(command_line)):
            new_task_file.write(command_line[cmdi]+" ")
        new_task_file.write(" 1>")
        new_task_file.write(log_names[0]+" 2>")
        new_task_file.write(log_names[1]+"\n")
        new_task_file.write("popd\n");
        if len(next_script)>0:
            new_task_file.write(next_script+".bat\n");
        for comment in final_comments:
            new_task_file.write("REM "+comment+"\n")
       
        new_task_file.close()

    return
