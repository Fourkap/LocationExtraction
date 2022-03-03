import subprocess
import os

path_to_pdf = os.path.abspath('C:\Inferno.pdf')
# I am testing this on my Windows Install machine
path_to_acrobat = os.path.abspath('C:\Program Files (x86)\Adobe\Reader 10.0\Reader\AcroRd32.exe')

# this will open your document on page 12
process = subprocess.Popen([path_to_acrobat, '/A', 'page=12', path_to_pdf], shell=False, stdout=subprocess.PIPE)
process.wait()
