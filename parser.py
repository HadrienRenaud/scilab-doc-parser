



#=======================================================================================================================
# Imports
#=======================================================================================================================

import re


#=======================================================================================================================
# Regex
#=======================================================================================================================

RE_FUN_DECLARATION = re.compile(r"^function (?P<syntax>(\[\s*(?P<arg_out>(\w+,\s*)*\w+)\s*\]\s*=\s*)?(?P<fun_name>\w+)\s*\(\s*(?P<arg_in>(\w+,\s*)*\w*)\s*\))\s*$")
RE_DOCSTRING = re.compile(r"$\s+//.*")


#=======================================================================================================================
# Function parse
#=======================================================================================================================





#=======================================================================================================================
# Function fileParse
#=======================================================================================================================

def fileParse(source, options):
    """Parse un fichier.
        :param source: 
    """"
    
#=======================================================================================================================
# Function funParse
#=======================================================================================================================


def funParse(source, options):
    """Parse une fonction.
        :param source: la fonction en question
        :type source: list of strings
        
        :param options: les options pour le parsage
        :type options: dictionary
        
        :return: la documentation de la fonction
        :rtype: list of strings
    """
    
    # On commence par récupérer la docstring et la déclaration de la fonction
    docString = []
    
    i = 0;
    test_re_fun_declaration = False
    test_re_docstring = True
    
    while (i < source.length() and not test_re_fun_declaration):
        if (RE_FUN_DECLARATION.match(source[i]) is not None):
            test_re_fun_declaration = True
            docString.append(l)
        else:
            i = i + 1
    
    while (i < source.length() and test_re_docstring):
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

