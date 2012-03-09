import os, sys
from threading import Thread
from time import sleep
from django.core import serializers

def is_scantailor():
    ''' 
    this crude function checks to see if scantailor is installed
    '''
    
    # can somebody fill in non-windows paths? 3-2-2012
    result = False
    
    if sys.platform == 'win32': #Windows
        dirs = [
               'c:/Program Files/Scan Tailor/',
               'c:/Program Files (x86)/Scan Tailor/',
               ]
    elif sys.platform == 'darwin': # OsX
        dirs = ['',]
    elif sys.platform == 'linux2': #Ubuntu Linux
        dirs = ['',]
    
    #if one of these paths exists, assume scan tailor is installed
    for dir in dirs:
        if os.path.isdir(dir):
            result = True
            
    return result

def get_drives():
    '''     
    http://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-drive-letters-in-python
    '''
    import string
    from ctypes import windll
    import time
    import os
    #time.sleep(1) # for good measure
    
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    return set(drives)

def get_mountpoint(request):
    '''
    Sorry, this is windows-only currently 3-6-2012 Sean Wingert Paper Upgrade Project
    Sean's post here: http://stackoverflow.com/questions/1968539/how-to-detect-flash-drive-plug-in-in-windows-using-python/9578439#9578439
    '''
    before = request.session['mounted_before']
    after = request.session['mounted_after']
    drives = after - before
    delta = len(drives)
    result = 'Could not autodetect drive. Please enter manually'

    if (delta):
        for drive in drives:
            if os.system("cd " + drive + ":/DCIM") == 0: # try DCIM 
                result = drive + ':\\DCIM\\'
            elif os.system("cd " + drive + ":/") == 0: # otherwise root
                result = drive + ':\\'
    else:
        result = "Unable to autodetect path"
    return result

def project_path():
    return os.path.join(os.path.dirname(__file__),'projects')

def create_project_dirs(cleaned_data):
    ''' create the project dirs, return True or False for validation '''
    title = cleaned_data.get('title', '')
    main = cleaned_data.get('path', '').replace('\\','/')
    sub  = os.path.join(main,title).replace('\\','/')
    sub_exists = os.path.isdir(sub)
    
    if sub_exists:
        pass
    else:
        try: # creating
            os.makedirs(sub, 0777)
        except:
            return False
    return True

def import_pages(Temp, src, dst, card='left'):
    ''' copy and rename from card to computer '''
    import os
    import shutil
    
    try:
        files = os.listdir(src.replace('\\','/')) # eg 'e:/dcim'
    except:
        return '[{"error": "This directory does not exist."}]' # JSON syntax
    
    types = ('jpg', 'jpeg', 'tif', 'tiff', 'png', 'jp2')
    inc_by = 2
    n = 0 # page number
    tasks  = []
    
    if card == 'left':
        n=1
    elif card == 'right':
        n=2
    elif card == 'both':
        n=1
        inc_by = 1
        
    for item in files:
        i = item.split('.')
        ext = i[-1] # -1 returns last part
        if ext.lower() in types:
            ns = '%(#)04d' % {'#':n} # num as string
            spath = src + os.sep + item
            renamed = ns + os.extsep + ext
            dpath = dst + os.sep + renamed
            task = "shutil.copy2('" + spath + "', '" + dpath + "')"
            n += inc_by
            output = "copied " + str(item) + " as " + renamed
            tasks.append([spath,dpath,output,task])
    
    if not len(tasks):
        return '[{"error":"No images found!"}]'
    
    total = len(tasks) 
    i     = 1
    for spath, dpath, output, log in tasks:
        try:
            t = Temp.objects.all().delete() # delete temp entries
            p  = round((float(i)/float(total))*100) # percent complete
            t  = Temp(p=output,k=i,v=p,m=total).save()
            shutil.copy2(spath, dpath)
            #sleep(.2)
            if i == total:
                sleep(1) # allows second thread to see 100 percent complete
            i += 1
        except:
            return '[{"error":"An error occurred during copying and renaming"}]' # JSON syntax
    t = Temp.objects.all().delete() # delete temp entries
    return '[{"success": "Import succeeded"}]' # JSON syntax


if __name__ == '__main__':
    drive = get_usb()
    print drive
    