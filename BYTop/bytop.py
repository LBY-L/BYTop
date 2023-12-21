import platform, sys, psutil, os, signal, re
from time import sleep

#BLACK = u"\u001b[30m"
#WHITE = u"\u001b[37m"
#RED = u"\u001b[31m"
#YELLOW = u"\u001b[33m"
#GREEN = u"\u001b[32m"
#CYAN = u"\u001b[36m"
#BLUE = u"\u001b[34m"
#PURPLE = u"\u001b[35m"

RESET = u"\u001b[0m"

# STATUS
STATUS_TITLE = u"\u001b[33m"
KERNEL = u"\u001b[33m"
SYSTEM = u"\u001b[36m"
UPTIME = u"\u001b[31m"
CPU = u"\u001b[35m"

# PROGRESS BARS
BARS = u"\u001b[33m"

# RAM
RAM_TITLE = u"\u001b[31m"
PERCENTAJE = u"\u001b[36m"

# CPU
CPU_TITLE = u"\u001b[34m"
THREADS = u"\u001b[32m"

def up(position=int):
    return u"\u001b[" + str(position) + "A"

def sigint_handler(signum, frame):
    sys.stdout.write(up(SpaceOfElm)) # Goes up and starts erasing
    sys.stdout.write(("\n" + " " * os.get_terminal_size().columns) * SpaceOfElm)
    sys.stdout.write(up(SpaceOfElm + 1)) # Goes up and ends
    print(" " * (os.get_terminal_size().columns + 1) + RESET) # Print exit for more beauty
    exit()
signal.signal(signal.SIGINT, sigint_handler)

def skipAnsi(text=str):
    # Uses a regular expresions for substract the ansi
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
    
def RamStatus():
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

def main():
    global width
    width = os.get_terminal_size().columns # Terminal width *Neded for future calculations*
    CPU = CPUStatus() # Skipping bugs XD
    global SpaceOfElm  # Skipping bugs XD
    
    # Making space in the screen
    SpaceOfElm = 6 + len(CPU) + 1 
    sys.stdout.write("\n" * SpaceOfElm)
    while True:
        width = os.get_terminal_size().columns
        # Gets the dashes of the main()
        Ram = RamStatus()
        Components = PCcomponents()
        CPU = CPUStatus()
        
        # The really final print
        sys.stdout.write(up(SpaceOfElm)) # Move up
        
        for i in range(len(Components)):
            print(Components[i] + Ram[i])
        
        print("\n".join(CPU))
        print("QUIT: ^C")
        sleep(1) # Less epilepsy

if __name__ == "__main__":
    main()