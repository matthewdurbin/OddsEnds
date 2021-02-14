###########################################
# This is an MCNP Automation Script,
# Running an MCNP input while chaning a particular
# card each time. Desired tally is parsed and saved.
# Last change was for a single NaI detector with
# an F8 pulse hieght tally
#
# Thank to Avery Grieve and co for initial help!
# -Matthew Durbin
###########################################
#
# ==========================================
import csv
import subprocess
import numpy as np

###############
#  FILES #
###############
# ===========================
# WHAT YOU WANT TO CHANGE EACH TIME FILE
filename = "change.csv"

# MCNP INPUT FILE
startFile = "Sing_NaI_floor.txt"

# OUTPUT FILE NAME - WHERE PARSED TALLIES WILL LIVE
outFile = "Test_Out.csv"

# SPECTRUM LENGTH: THIS IS HOW MANY CHANNELS YOUR F8 TALLEY HAS
sl = 1024
# ===========================
my_env = {}
#####################
## HELPER FUNCTIONS
#####################
# ===========================
def replacePos(inputFile, pos):
    f = open(inputFile, "r")
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        line = lines[i]
        if "SDEF" in line:
            # 		Directly place the line you want to change form your input here
            # 			Place the specific items to change in curly brackets
            lineString = "SDEF pos={0} {1} {2} erg=.6617 par=2\n".format(
                pos[0], pos[1], pos[2]
            )
            lines[i] = lineString
    f = open(inputFile, "w")
    f.writelines(lines)
    f.close()


# ----------------------------
def initMCNP():
    global my_env
    print("INITIALIZING MCNP")
    import subprocess, os

    my_env = os.environ.copy()
    print(my_env["DATAPATH"])
    #!! Modify these paths
    my_env["PATH"] = "/path/to/executable;" + my_env["PATH"]
    my_env["DATAPATH"] = "/path/to/MCNP_DATA"
    my_env["DISPLAY"] = "localhost:0"
    print(my_env["DATAPATH"])


# ----------------------------
def runMCNP(inputFile):
    print("RUNNING MCNP")
    command = "mcnp6 i={0} tasks 8".format(inputFile)
    process = subprocess.Popen(command, shell=True, env=my_env)
    process.wait()


# ----------------------------
# THIS WILL EXTRACT EACH CHANNEL OF THE SPECTRA
def readResults():
    print("READING RESULTS")
    file = open("outp", "r")
    lines = list(file)
    file.close()
    line10 = ""
    d1spect = ""
    for i in range(len(lines)):
        line = lines[i]
        if "cell  1" in line:
            for j in range(sl):
                line10 = lines[i + j + 2]
                d1spect += line10[17:28] + ", "
    with open(outFile, "a") as file:
        file.write(d1spect + "\n")


# ----------------------------


# -----------------------------
#!! Warning... This output file may be very large
def saveOutput():
    print("Saving Output")
    file = open("outp", "r")
    lines = file.readlines()
    file.close()
    f = open("SavedOutp.txt", "a")
    f.write(
        "\n"
        + "============================ new run ==========================="
        + "\n"
        + "\n"
    )
    f.writelines(lines)
    f.close


def cleanWorkspace():  # change rm (remove) to del (delete) for windows
    print("CLEANING WORKSPACE")
    commands = ["rm runtp*", "rm out*"]
    for command in commands:
        subprocess.call(command, shell=True)


# ============================

#####################
#  AUTOMATION LOOP  #
#####################
# ============================
csvFile = open(filename)
posCSV = csv.reader(csvFile, delimiter=",", quotechar='"')
keys = next(posCSV)
n = 0

with open(outFile, "a") as file:
    file.write("")
initMCNP()
for row in posCSV:
    replacePos(startFile, row)
    runMCNP(startFile)
    readResults()
    #!! Comment saveOutput out if you don't want it to combine all outputs
    saveOutput()
    cleanWorkspace()
    n += 1
    print("==================")
    print("Run number:", n)
    print("==================")
csvFile.close()
# THIS MAKES A BEEB SOUND WHEN IT'S ALL DONE
# winsound.Beep(500,100)
# =============================
