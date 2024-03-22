import os
import time
import sys
import diskimage_builder
import getpass

## FORMAT TERMINAL WINDOW SIZE
sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=20, cols=61))

## CLEAR TERMINAL
def clearT():
    os.system('clear')
    return()

## FIND DRIVES
def find_drives():
    clearT()
    os.system('lsblk > output.txt')
    with open('output.txt','r') as f:
        Lines = f.readlines()
        for line in Lines:
            print(line.strip())
    return()

## SELECT DRIVE
def select_drive():
    clearT()
    while(1):
        find_drives()
        drive = input('The drives above were found on your computer.\nPlease select a drive or enter 0 to quit.\n>>')
        if(drive == '0'):
            return(drive)

        with open('output.txt','w+') as f:
            Lines = f.readlines()
            for line in Lines:
                if line.startswith(drive):
                    print(line.strip())

        clearT()
        os.system('cat output.txt')
        print(drive)
        ## Check to see if the drive is correct
        YorN = input('Does this look right?(Y/n)').replace(" ","")
        if YorN.lower() == 'n':
            clearT()
            print("Shoot, let's try that again then!")
            time.sleep(1)
        elif YorN.lower() == 'y':
            clearT()
            print("Next step!")
            time.sleep(1)
            return(drive)
        else:
            clearT()
            print("Your input is not handled by this program. Please try again...")
            time.sleep(2)

## SH0W DRIVE
def show_drives():
    clearT()
    os.system('cat output.txt')
    return()

## WARNING
def warning():
    while(counter < 5):
        clearT()
        time.sleep(.5)
        print('██╗    ██╗ █████╗ ██████╗ ███╗   ██╗██╗███╗   ██╗ ██████╗ ')
        print('██║    ██║██╔══██╗██╔══██╗████╗  ██║██║████╗  ██║██╔════╝ ')
        print('██║ █╗ ██║███████║██████╔╝██╔██╗ ██║██║██╔██╗ ██║██║  ███╗')
        print('██║███╗██║██╔══██║██╔══██╗██║╚██╗██║██║██║╚██╗██║██║   ██║')
        print('╚███╔███╔╝██║  ██║██║  ██║██║ ╚████║██║██║ ╚████║╚██████╔╝')
        print(' ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ')
        time.sleep(.5)
        counter = counter + 1
    return()

## WIPE DRIVE
def wipe_drive(drive):
    counter = 0
    warning()
    input('Warning...Preparing to shred /dev/'+drive+'. Press enter to continue')
    time.sleep(3)
    os.system('sudo shred -v /dev/'+drive)
    time.sleep(3)                                                          
    return()

## Mount DISK (CURRENTLY BROKEN)
def mount_disk(drive):
    os.system('sudo mkdir -p /media/'+getpass.getuser()+'/'+drive)
    os.system('sudo mount -o loop /media/'+getpass.getuser()+'/'+drive)
    return()

## UNMOUNT DISK (CURRENTLY BROKEN)
def unmount_disk(drive):
    clearT()
    with open('output.txt','r') as f:
        Lines = f.readlines()
        for line in Lines:
            if line.startswith(drive)  or line.startswith('├─'+drive) or line.startswith('└─'+drive):
                time.sleep(2)
        YorN = input('Does this drive look correct?')
        if YorN.lower() == 'y':
            
            print(line[33:])
    return()

## CLONE DRIVE (IN PROGRESS)
def clone_drive(drive1,drive2):
    bs = input('BS size?')
    print(os.path.getsize('/dev/'+drive1))
    print(os.path.getsize('/dev/'+drive2))
    os.system('sudo dd if=/dev/'+drive1+' of=/dev/'+drive2+' bs='+bs+' conv=noerror,sync status=progress')
    return()

## FORMAT DISK ## DON'T WORK
def format_disk(drive):
    while(1):
        print('What file system type would you like?')
        driveType = input('1) ext4\n2) FAT32\n3) NTFS\n>>')
        if driveType == '1':
            driveType = 'ext4'
            os.system('sudo mkfs -t '+driveType+' /dev/'+drive)
            quit()
        elif driveType == '2':
            driveType = 'FAT32'
            os.system('sudo mkfs -t '+driveType+' /dev/'+drive)
            quit()
        elif driveType == '3':
            driveType = 'NTFS'
            os.system('sudo mkfs -t '+driveType+' /dev/'+drive)
            quit()
        else:
            print('Invalid type!!')
    return()

## IMAGE DISK
def imager(drive,iso_file):
    print(drive+" "+iso_file)
    YorN = input('Does this look correct?').replace(" ","")
    clearT()
    if YorN.lower() == 'y':
        print('Total File Size: ')
        print(os.path.getsize(iso_file.replace("'","").replace(" ","")))
        sizeFile = float(os.path.getsize(iso_file.replace("'","").replace(" ","")))/1000000000
        print(str(sizeFile)+' GB')
        os.system('sudo dd if='+iso_file+' of=/dev/'+drive+' oflag=direct status=progress')
        time.sleep(5)
    return(YorN)

## MAIN LOOP
while(1):
    clearT()
    clearT()
    print('███████╗      ██╗███╗   ███╗ █████╗  ██████╗ ███████╗██████╗ ')
    print('██╔════╝      ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝██╔══██╗')
    print('███████╗█████╗██║██╔████╔██║███████║██║  ███╗█████╗  ██████╔╝')
    print('╚════██║╚════╝██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝  ██╔══██╗')
    print('███████║      ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗██║  ██║')
    print('╚══════╝      ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝')
    print("Please keep the terminal the same size to preserve\nthe formatting.If this is your first time using this tool,\ntry finding drives first to create the output file\n")
    userSelection = input('What would you like to do?\n1) Wipe Drive\n2) Clone Drive\n3) Image Drive\n4) Find Drives\n5) Format Disk\n6) Mount Drive\n7) Unmount Drive \n99) Quit\n>>')

    match int(userSelection):
        case 1:
            drive = select_drive()
            if drive != '0':
                wipe_drive(drive)
                find_drives()
                show_drives()

        case 2:
            drive1 = select_drive()
            if drive1 != '0':
                print('Now, select second drive.')
                time.sleep(2)
                drive2 = select_drive()
                if drive2 != '0':
                    clone_drive(drive1,drive2)
                    find_drives()
                    show_drives()

        case 3:
            clearT()
            iso_file = input('Please enter the path of the iso file (Drag and drop)\n>>')
            find_drives()
            show_drives()
            drive = input('Which Drive?\n>>')
            clearT()
            YorN = imager(drive,iso_file)
            if YorN.lower() == 'n':
                print('sorry try again!')
            time.sleep(2)

        case 4:
            find_drives()
            clearT()
            time.sleep(1)
            os.system('cat output.txt')
            input('Drives stored into the outputfile. Press enter to continue...')
        
        case 5:
            drive = select_drive()
            if drive != '0':
                format_disk(drive)
                find_drives()
                show_drives()
        case 6:
            drive = select_drive()
            if drive != '0':
                mount_disk(drive)
                time.sleep(2)

        case 7:
            drive = select_drive()
            if drive != '0':
                unmount_disk(drive)
                time.sleep(2)

        case 99:
            clearT()
            quit()