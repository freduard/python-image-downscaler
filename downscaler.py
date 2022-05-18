from genericpath import exists
import cv2
import os

images = []
subDirs = []
directoriesSkipped = 0;

# CONSOLE COLORS
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue

cDir = os.getcwd();
scale = 0.25;

#FUNCTIONS
def italicText(string):
    return "\x1B[3m" + string + "\x1B[0m";
    
def resizeImg(image):
    img = cv2.imread(image);
    height = int(img.shape[0] * scale);
    width = int(img.shape[1] * scale);
    dimension = (width, height);
    resize = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA);
    
    cv2.imwrite(image.replace(cDir, cDir + "/downscaled"), resize);
    print(G + "[+] " + W + "Resized " + str(resize.shape) + ": " + image.replace(cDir, ""));

def scanDirectory(path):
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".jpg"):
                images.append(os.path.join(root, file));
        
        if("/downscaled/" not in os.path.join(root, file)):
            subDirs.append(os.path.join(root, file).replace(cDir, cDir + "/downscaled").replace(file, ""));

def createDirectories():
    global directoriesSkipped;

    for dir in subDirs:
        if(exists(dir)):
            directoriesSkipped += 1;
        else:
            os.mkdir(dir);
            print(G + "[+]" + W + " Directory " + italicText(dir) + " created successfully!");

    if(directoriesSkipped > 0):
        print(O + "[!]" + W + " Skipped creating " + O + str(directoriesSkipped) + W + " directories, because they already exist. Images will be replaced instead.");

def main():
    print("[#] Parsing all files & directories...")
    scanDirectory(dir);

    print("[#] Recreating original directories & path tree...")
    createDirectories();

    print("[#] Downscaling all images found...");
    for img in images:
        resizeImg(img);

#FIRST EXECUTABLES
dir = input(B + "[i] " + W + "Enter directory " + italicText("e.g. /my/example/path") + " (leave empty for current): ");
if(dir == ""):
    print(G + "[+] " + W + "User input left empty, using " + italicText(cDir) + " as directory.");
    dir = cDir;
else:
    print(G + "[+] " + W + "Using " + italicText(dir) + " as directory.\n");

scalePercentage = input(B + "[i] " + W + "Enter scale percentage " + italicText("e.g. 0.00 - 1.00") + " (leave empty for 0.25): ");
if(scalePercentage == ""):
    print(G + "[+] " + W + "User input left empty, using " + italicText(str(scale)) + " as scale percentage.");
else:
    print(G + "[+] " + W + "Using " + italicText(str(scale)) + " as scale percentage.");

main();
