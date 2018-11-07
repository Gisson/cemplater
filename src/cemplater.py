#!/usr/bin/env python3
import jinja2
import shutil
from os import listdir
import sys

def superRead(filename):
    contents = ""
    try:
        with open(filename) as f:
            contents = f.read()
    except FileNotFoundError:
        print("File not found "+filename, file=sys.stderr)
    return contents

def parseTemplate(headerFile = "", filename = "", footerFile = "", options = {} ):
    header = superRead(headerFile)
    footer = superRead(footerFile)
    contents = superRead(filename)
    return jinja2.Template(header+contents+footer).render(options) 

def writeResults(contents = "", dest= "" ):
    with open(dest, "w") as f:
        f.write(contents)

def createProject(baseDir = "", destDir = "", options = []):
    optdict = {}
    for i in options:
        print(i)
        optdict[i.split("=")[0]] = i.split("=")[1]
    try:
        os.makedirs(destDir)
    except FileNotFoundError:
        print("Cannot create directory. File not found", file=sys.stderr)
        sys.exit(-1)
    except FileExistsError:
        print("File {0} already exists".format(projectName))
        sys.exit(-1)
    for filename in listdir(baseDir):
        if filename == "header.template" or filename == "footer.template":
            continue
        writeResults(parseTemplate(baseDir+"header.template", baseDir+filename, baseDir+"footer.template", optdict), destDir+filename)
        


if __name__ == '__main__':
    import argparse
    import os
    from pathlib import Path

    supportedLangs = ['C', 'python']

    baseDir = "templates/"

    parser = argparse.ArgumentParser(description = "Project Templater.")
    parser.add_argument('--projectname', metavar='name', type=str, help='Project name', required=True)
    parser.add_argument('--language', metavar='lang', type=str, help='Language to use in the project', choices = supportedLangs, required=True)
    parser.add_argument('--options', metavar='opts', type=str, nargs='+', help='Templating options' )
    parser.add_argument('--templatedir', metavar='tdir', type=str, help='Directory of the templates', default = '/usr/share/templates/') 
    parser.add_argument('--destination', metavar='dest', type=str, help='Directory in which the project will be created', default = str(Path.home())+"/.cemplater/projects/")
    args = parser.parse_args()
    # Get project name
    projectName =  args.projectname
    language = args.language


    baseDir = (args.templatedir if args.templatedir[-1]=="/" else args.templatedir+"/")
    destDir = (args.destination if args.destination[-1]=="/" else args.destination+"/")
    destDir = destDir + (args.projectname if args.projectname[-1]=="/" else args.projectname+"/")
    

    if isinstance(args.options, list):
        createProject(baseDir+language+"/", destDir, args.options)
    else:
        createProject(baseDir+language+"/", destDir)
#    print(parseTemplate(headerFile=baseDir+language+"/"+"header.template", filename = baseDir+language+"/main.c",\
    #footerFile = baseDir+language+"/"+"footer.template"))

#    results = parseTemplate(headerFile="templates/C/header.template", filename = "templates/C/main.c", footerFile = "templates/C/footer")
#    writeResults(results, "testproj/main.c")

