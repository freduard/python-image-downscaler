from genericpath import exists, isdir
from re import L
import cv2
import os

images = []
subDirectories = []
directoriesSkipped = 0;

# CONSOLE COLORS
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear'); # A way to clear the console.
cDir = os.getcwd(); # Set cDir to the current working directory.
scale = 0.25;

#FUNCTIONS
def italicText(string): # This function simply makes any text output as italic to the console.
    return "\x1B[3m" + string + "\x1B[0m";
    
def resizeImage(image):
    img = cv2.imread(image); # Reading the image from file path.
    height = int(img.shape[0] * scale); # Scaling the image's height by scale value.
    width = int(img.shape[1] * scale); # Scaling the image's width by scale value.
    dimension = (width, height); # Putting the height & width together.
    resize = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA); # Compiling everything into one value which we can use to make the image.
    
    cv2.imwrite(image.replace(iDir, os.path.join(iDir, "downscaled")), resize); # Writes an image file to a specified path with specified settings which is given by resize.
    print(G + "[+] " + W + "Resized " + str(resize.shape) + ": " + image.replace(iDir, os.path.join(iDir, "downscaled")));

def scanDirectory(path):
    for root, _, files in os.walk(path): # I have no idea how these 2 for loops work.
        for file in files:
            if(file.endswith(".jpg") and "/downscaled/" not in os.path.join(root, file)): # If image doesn't have /downscaled/ in it's path, we add it to images[].
                images.append(os.path.join(root, file));
        
        if("/downscaled/" not in os.path.join(root, file)): # If sub-directory doesn't have /downscaled/ in it's path, we add it to subDirectories[].
            subDirectories.append(os.path.join(root, file).replace(file, "").replace(iDir, os.path.join(iDir, "downscaled")));

def createDirectories():
    global directoriesSkipped;

    for subDir in subDirectories:
        if(exists(subDir)): # If a directory in subDirs already exists, add 1 to directoriesSkipped so we can display it later.
            directoriesSkipped += 1;
        else: # Otherwise, make a new directory.
            os.mkdir(subDir);
            print(G + "[+]" + W + " Directory " + italicText(subDir) + " created successfully!");

    if(directoriesSkipped > 0): # If directoriesSkipped is above 0, we display a message saying we skipped X amount of directories.
        print(O + "[!]" + W + " Skipped creating " + O + str(directoriesSkipped) + W + " directories, because they already exist. Images will be replaced instead.");

def userPathInput():
    global iDir;

    iDir = str(input(B + "[i] " + W + "Enter directory " + italicText("e.g. /my/example/path") + " (leave empty for current): ")); # Saves userinput into iDir
    if(iDir == ""): # If iDir was left empty by the user, use cDir.
        print(G + "[+] " + W + "User input left empty, using " + italicText(cDir) + " as directory.");
        iDir = cDir;
    else:
        if(isdir(iDir)):
            if(iDir[-1] == "/" or iDir[-1] == "\\"): # If iDir has a slash or backslash at the end, this will remove it so scanDirectory() works properly.
                iDir = iDir[:-1]
            print(G + "[+] " + W + "Using " + italicText(iDir) + " as directory.\n");      
        else:
            print(R + "[!]" + O + " Directory " + W + italicText(iDir) + O + " is invalid.");
            userPathInput();

def userScaleInput():
    global scale;

    iScale = input(B + "[i] " + W + "Enter scale percentage " + italicText("e.g. 0.00 - 1.00") + " (leave empty for 0.25): ");
    if(iScale == ""):
        print(G + "[+] " + W + "User input left empty, using " + italicText(str(scale)) + " as scale percentage.");
    else:
        try:
            scale = float(iScale);
            print(G + "[+] " + W + "Using " + italicText(iScale) + " as scale percentage.\n");
        except:
            print(R + "[!] " + W + italicText(iScale) + O + " is invalid.\n");
            userScaleInput();

def main():
    clearConsole();

    userPathInput();
    userScaleInput();

    print("[#] Parsing all files & directories...")
    scanDirectory(iDir);

    print("[#] Recreating original directories & path tree...")
    createDirectories();

    print("[#] Downscaling all images found...");
    for img in images:
        resizeImage(img);

clearConsole();
main();
