



#=======================================================================================================================
# Imports
#=======================================================================================================================

import re


#=======================================================================================================================
# Regex
#=======================================================================================================================


RE_CONTINUATION = re.compile(r"\s*\.\.\s*")
RE_FUN_DECLARATION = re.compile(r"^function (?P<syntax>(\[\s*(?P<arg_out>(\w+,\s*)*\w+)\s*\]\s*=\s*)?(?P<fun_name>\w+)\s*\(\s*(?P<arg_in>(\w+,\s*)*\w*)\s*\))\s*$")
RE_DOCSTRING = re.compile(r"$\s+//.*")
RE_FUN_END = re.compile(r"endfunction\s*")


#=======================================================================================================================
# Function parse
#=======================================================================================================================





#=======================================================================================================================
# Function fileParse
#=======================================================================================================================

def fileParse(source, dest=None, options):
    """Parse un fichier.
        :param source: le path vers le fichier source.
        :type source: str
        
        :param options: les options pour le parsage
        :type options: dictionary
        
        :param dest: le path vers le fichier destination.
            Par défaut, si source vaut ``/path/to/sourceDir/source.sci`` alors dest vaut 
            ``/path/to/sourceDir/source.rst``.
        :type dest: str
        
        Parse un fichier.
    """"
    
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
        res += funParse(lines[begin:end])    
    
    # On écrit dans le fichier destination
    with open(dest, "w") as fDest:
        for l in res:
            fDest.write(l + "\n")


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
        if (RE_FUN_DECLARATION.match(source[i]) is not None):
            test_re_fun_declaration = True
            docString.append(l)
        else:
            i = i + 1
    
    while (i < len(source) and test_re_docstring):
        if (RE_DOCSTRING.match(l) is not None):
            i = i + 1
            docString.append(l)
        else
            test_re_docstring = False
    
    return docParse(docString, options)




#=======================================================================================================================
# Function docParse
#=======================================================================================================================




def docParse(source, options):
    return source

