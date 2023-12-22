import platform, psutil, os, signal, re
from os import get_terminal_size
from sys import stderr, stdout
from .cli import cli
from time import sleep

def up(position=int):
    return u"\u001b[" + str(position) + "A"

def sigint_handler(signum, frame):
    echo(up(SpaceOfElm) + 
         ("\n" + " " * get_terminal_size().columns) * SpaceOfElm +
         up(SpaceOfElm + 1) +
         " " * (get_terminal_size().columns + 1) + RESET) # Goes up and starts erasing
    exit()
signal.signal(signal.SIGINT, sigint_handler)

def skipAnsi(text=str):
    ansiEscape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]') # IDK Chat GPT gives me it
    noAnsi = ansiEscape.sub('', text)
    return len(noAnsi)

def dashes(text=str, width=int, title=str):
    lines = text.splitlines() # Split by \n
    newWidth = width - skipAnsi(title) # Calculates the width for the title and styling
    # Makes the dash/box
    res = ['┌' + title + '─' * newWidth + '┐']
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width + (len(s) - skipAnsi(s))] + '│') # Add spaces without ANSI characters
    res.append('└' + '─' * width + '┘')
    return res

def PCcomponents():
    # Get Cpu Brand
    with open('/proc/cpuinfo', 'r') as f:
        cpuinfo = f.readlines()[4][13:].strip()
    
    # Format Uptime
    with open('/proc/uptime', 'r') as f:
        uptimeSeconds = float(f.readline().split()[0])
    uptime = str(int(int(uptimeSeconds//60)//60)) + " h " + str(int(uptimeSeconds//60) - int(int(uptimeSeconds//60)//60)*60 ) + " m"
    
    linuxDistro = platform.freedesktop_os_release()["NAME"] + " " + platform.uname()[4]  # Get linux distro
    kernel = platform.uname()[2] # Get Kernel
    
    # Returns the dash
    res = dashes(f"{SYSTEM}System:{RESET} {linuxDistro} \n{KERNEL}Kernel:{RESET} {kernel} \n{UPTIME}Uptime:{RESET} {uptime} \n{CPU}CPU:{RESET} {cpuinfo}", width//2-2, title=f"|{STATUS_TITLE} PC STATUS {RESET}|")
    return res
    
def RAMStatus():
    # Ram %, Used Ram, System Ram
    PerRam = psutil.virtual_memory()[2]
    UsedRam = round(psutil.virtual_memory()[3]/1000000000, 2)
    SysRam = round(psutil.virtual_memory()[0]/1000000000)
    
    More = str(UsedRam) + "G/" + str(SysRam) + "G" # Shows the used ram and the system ram
    BarWidth = width//2 - 4 - len(More) # Gets the progresbar width
    ramDis = int((int(PerRam)/100) * BarWidth) 
    Len = BarWidth - ramDis
    # Returns the dash
    res = dashes(f"{PERCENTAJE}{str(PerRam)}%{RESET}\n" + "[" + BARS + '■' * ramDis + RESET + " " * Len + More + "]" + "\n \n \n", width//2-2, title=f"|{RAM_TITLE} RAM {RESET}|")
    return res

def CPUStatus():
    # Shows the threads
    cpu_usage = psutil.cpu_percent(interval=0, percpu=True)
    CpuUsage = []
    for i, usage in enumerate(cpu_usage):
        CpuUsage.append(usage)
    
    Columns = 3 # Number of colums that will showing
    
    bars = ""
    for i in range(len(CpuUsage)):
        More = str(CpuUsage[i]) + "%" # Show the thread %
        BarWidth = width//Columns - 3 - len(More) - len(str(i)) - 1 # Calculates the progress bar with Columns variable
        CpuDis = int((int(CpuUsage[i])/100) * BarWidth) # The times by the ■ will be multiplied
        Len = BarWidth - CpuDis # Blank Spaces
        # Threads an cores
        Threads = psutil.cpu_count(logical=True)
        Cores = psutil.cpu_count(logical=False)
        
        # Final printing
        if i == 0:
            bars = bars + " " + str(Cores) + " Cores " + str(Threads) + " Threads" 
        if i % Columns != 0:
            bars = bars + " " + f"{THREADS}{str(i)}{RESET}" + "[" + BARS + '■' * CpuDis + RESET + " " * Len + More + "]"
        else:
            bars = bars + "\n " + f"{THREADS}{str(i)}{RESET}" + "[" + BARS + '■' * CpuDis + RESET + " " * Len + More + "]"
            
    # Return the dash
    res = dashes(bars, width-2, title=f"|{CPU_TITLE} CPU {RESET}|")
    return res

def load(): # Loader
    data = cli()
    # Aliases
    global echo, echoErr
    echoErr = stderr.write
    echo = stdout.write
    # PC STATUS
    global STATUS_TITLE, KERNEL, SYSTEM, UPTIME, CPU, BARS, RAM_TITLE, PERCENTAJE, CPU_TITLE, THREADS, RESET
    RESET = "\u001b[0m"
    STATUS_TITLE = data["STATUS_TITLE"]
    KERNEL = data["KERNEL"]
    SYSTEM = data["SYSTEM"]
    UPTIME = data["UPTIME"]
    CPU = data["CPU_MODEL"]
    
    # BARS
    BARS = data["PROGRESS_BARS"]
    
    # RAM
    RAM_TITLE = data["RAM_TITLE"]
    PERCENTAJE = data["PERCENTAJE"]
    
    # CPU
    CPU_TITLE = data["CPU_TITLE"]
    THREADS = data["THREADS"]
    
    global width
    width = get_terminal_size().columns # Terminal width *Neded for future calculations*
    
    global SpaceOfElm  # Skipping bugs XD
    SpaceOfElm = 6 + len(CPUStatus()) + 1 # Prepares space  

def main():
    load() # Loads the esencial values
    
    echo("\n" * SpaceOfElm) # Makes space in the screen
    while True:
        
        if SpaceOfElm+1 >= get_terminal_size().lines: # Comprobates the screen height size
            echoErr(up(SpaceOfElm) + "ERROR: The terminal isn't hight enough!") 
            exit()

        # Gets the dashes
        global width
        width = get_terminal_size().columns # Re calculates the screen width
        Ram = RAMStatus()
        Components = PCcomponents()
        CPUStats = CPUStatus()
        
        # The really final print

        echo(up(SpaceOfElm)) # Move up

        for i in range(len(Components)):
            print(Components[i] + Ram[i])

        print("\n".join(CPUStats) + "\nQUIT: ^C")
        sleep(0.7) # Less epilepsy
