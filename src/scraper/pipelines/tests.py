import re

#sample_string = "Suspect in New Jersey councilwomanâs slaying indicted on murder, weapons charges whatever          "
#print("1: " + sample_string, len(sample_string))
#sample_string = sample_string.strip(" ").strip("r").strip("e").strip("v")
# sample_string = sample_string.strip("e")
# sample_string = sample_string.strip("v")
#print("2: " + sample_string, len(sample_string))


headline = (''' 
        
        
           By: 
           
           
           
             Joe Moeller 
            ,  KTNV Staff ''' )


headline = re.sub('\\s+',' ', headline)
print(headline)