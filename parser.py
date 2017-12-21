



#=======================================================================================================================
# Imports
#=======================================================================================================================

import re
import os.path as pa
from os import listdir, mkdir
from shutil import copy2

#=======================================================================================================================
# Regex
#=======================================================================================================================


RE_CONTINUATION = re.compile(r"\s*\.\.\s*")
RE_FUN_DECLARATION = re.compile(r"^function (?P<syntax>(\[\s*(?P<arg_out>(\w+,\s*)*\w+)\s*\]\s*=\s*)?(?P<fun_name>\w+)\s*\(\s*(?P<arg_in>(\w+,\s*)*\w*)\s*\))\s*$")
RE_DOCSTRING = re.compile(r"\s+\/\/\s*(?P<content>(.*\w)?)\s*")
RE_FUN_END = re.compile(r"endfunction\s*")

DEST_RETURN = "__return__"


#=======================================================================================================================
# Function defaultOptions
#=======================================================================================================================

def defaultOptions():
    options = {
        "extensions_in": [".sci"],
        "extension_out": ".rst",
    }
    return options

#=======================================================================================================================
# Function parse
#=======================================================================================================================

def parse(source, dest=None, options=None):
    """
        :param source: la path vers la source.
            Si c'est un dossier, on crée récursivement une documentation.
            Si c'est un fichier, on appelle directement fileParse.
        :type source: string
        
        :param dest: la destination.
            Si c'est None et que source est un dossier, on crée dans le directory parent un dossier source-doc qui 
            contiendra la documentation.
        :type dest: string
        
        :param options: les options pour le parsage
        :type options: dictionary
     """
     
    # si les options ne sont pas précisées
    if (options is None):
        options = defaultOptions()
     
    # On traite le cas ou c'est un fichier
    if (pa.isfile(source)):
        return fileParse(source, dest, options)
    
    # cas étrange
    if (not (pa.exists(source) and pa.isdir(source))):
        print("Erreur : source n'existe pas")
        return 1
        
        
    # Cas ou c'est un dossier.
    
    # Si dest==None
    if (dest is None):
        parent, nom = pa.split(source)
        if pa.exists(pa.join(parent, nom + "-doc")):
            i = 1
            while pa.exists(pa.join(parent, nom + "-doc" + str(i))):
                i += 1
            dest = pa.join(parent, nom + "-doc" + str(i))
        else:
            dest = pa.join(parent, nom + "-doc")
                
    # Traitement de la destination
    if (not pa.exists(dest)):
        print("Creation de dest : {}".format(dest))
        mkdir(dest)     
    elif (not pa.isdir(dest)):
        print("parser.py WARNING parse dest is not a directory")
        return 1
    
    # Traitement général
    names = listdir(source)
    # Pour chaque élément de source
    for name in names:
        newSource = pa.join(source, name)
        # si c'est une dossier, alors on le parse
        if (pa.isdir(newSource)):
            parse(newSource, pa.join(dest, name, options))
        # si c'est un fichier ".sci"
        elif (name[-4:] in options["extensions_in"]):
            fileParse(newSource, pa.join(dest, name[:-4] + options["extension_out"]), options)
        else:
            copy2(newSource, pa.join(dest, name))
     
    
            
     

#=======================================================================================================================
# Function fileParse
#=======================================================================================================================

def fileParse(source, dest=None, options=None):
    """Parse un fichier.
        :param source: le path vers le fichier source.
        :type source: str
        
        :param options: les options pour le parsage
        :type options: dictionary
        
        :param dest: le path vers le fichier destination.
            Par défaut, si source vaut ``/path/to/sourceDir/source.sci`` alors dest vaut 
            ``/path/to/sourceDir/source.rst``.
            De même si dest vaut DEST_RETURN alors on retourne le résultat sans l'écrire.  
        :type dest: str
        
        Parse un fichier.
    """
    
    # Valeur par défaut de dest
    if (dest is None):
        dest = source[:-3] + "rst"
    
    # Lecture du fichier source
    with open(source, "r") as fSource:
        content = fSource.read()
    
    # On récupère ses lignes
    lines = parseContinuations(content).split("\n")
    
    # On initialise les positions du début et de la fin de chaque fonction
    indexes_b = []
    indexes_e = []
    
    # On récupère le début et la fin de chaque fonction
    for i,l in enumerate(lines):
        if (RE_FUN_DECLARATION.fullmatch(l) is not None):
            indexes_b.append(i)
        elif (RE_FUN_END.fullmatch(l) is not None):
            indexes_e.append(i)
    
    # On parse chaque fonction
    res = []
    for begin, end in zip(indexes_b, indexes_e):
        print("funParse appelé avec lignes de {begin} à {end}".format(begin=begin, end=end))
        res += funParse(lines[begin:end], options)    
        res.append("\n")
    
    # On retourne le résultat si demandé
    if (dest==DEST_RETURN):
        return "\n".join(res)
    
    # On écrit dans le fichier destination
    with open(dest, "w") as fDest:
        for l in res:
            fDest.write(l + "\n")

    return 0

# Fonction auxilliaire        
def parseContinuations(content):
    """Replace the continuation marks by spaces."""
    return RE_CONTINUATION.sub(" ", content)



#=======================================================================================================================
# Function funParse
#=======================================================================================================================


def funParse(source, options):
    """
        :param source: la fonction en question
        :type source: list of strings
        
        :param options: les options pour le parsage
        :type options: dictionary
        
        :return: la documentation de la fonction
        :rtype: list of strings
        
       Parse une fonction. 
    """
    
    # On commence par récupérer la docstring et la déclaration de la fonction
    docString = []
    
    i = 0;
    test_re_fun_declaration = False
    test_re_docstring = True
    
    while (i < len(source) and not test_re_fun_declaration):
        if (RE_FUN_DECLARATION.fullmatch(source[i]) is not None):
            print("funParse : fun declaration trouvé à la ligne {}".format(i))
            test_re_fun_declaration = True
            docString.append(source[i])
        i = i + 1
    
    while (i < len(source) and test_re_docstring):
        if (RE_DOCSTRING.fullmatch(source[i]) is not None):
            docString.append(source[i])
            i = i + 1
        else:
            print("Docstring non trouvé à la ligne {} : {}".format(i, source[i]))
            test_re_docstring = False
    
    print(" -- begin : docString --")
    for l in docString:
        print(l)
    print(" -- end : docString --\n\n")
    
    return docParse(docString, options)




#=======================================================================================================================
# Function docParse
#=======================================================================================================================


def docParse(source, options):
    
    m = RE_FUN_DECLARATION.match(source.pop(0))
    if (m is None):
        return 1
    
    decl = ".. function:: {}({})".format(m.group("fun_name"), m.group("arg_in"))
    syntaxe = "   :syntaxe: {}".format(m.group("syntax"))
    
    res = [decl, "   ", syntaxe, "   "]
    
    cat = ""
    
    for l in source:
        # on récupère le contenu
        m = RE_DOCSTRING.match(l)
        if (m is None):
            print("docParse : pas de docString trouvé sur la ligne : {}".format(l))
            continue
        content = m.group("content")
        
        # Ligne vide => nouvelle catégorie
        if (content == ""):
            cat = ""
        
        # Arguments
        elif (content in ["Arguments", "Arguments :", "Argument"]):
            cat = "Arguments"
        elif (cat == "Arguments"):
            words = content.split()
            if len(words) >= 2 and words[1] == ":":
                words.pop(1)
            res.append("   :param {}: {}".format(words[0], " ".join(words[1:])))
            res.append("   :type {}: Inconnu".format(words[0]))
            res.append("   ")
        
        # Voir aussi
        elif (content in ["Voir aussi", "See also", "Voir aussi :", "See also :"]):
            cat = "seealso"
            res.append("   .. seealso::")
        elif (cat == "seealso"):
            res.append("`{}`_".format(content))
        
        # Attention
        elif (content in ["Attention", "Warning", "Attention:", "Warning:"]):
            cat = "warning"
            res.append("   .. attention::")
        elif (cat == "warning"):
            res.append(content)
       
        # Auteur
        elif (content in ["Fonctions utilisees :", "Fonctions utilisées"]):
            cat = "appelle"
            res.append("   :appelle:")
        elif (cat == "appelle"):
            res.append("    * " + content)
        
        # Syntax
        elif (content in ["Syntax", "Syntaxe"]):
            pass
        
        # Si on connait pas
        else:
            res.append("   " + content)
        
        
    return res

