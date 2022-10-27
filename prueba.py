import pandas as pd


workbook = pd.ExcelFile("Cursos-DB.xlsx")
df = pd.read_excel(workbook, "Empleados")
superdick= {"pene":8, "toro":2, "lala":56, "meme": 45, "consizo": 33, "nada que ver": 99, "lista infinita": 22, "sigue la joda": 33}



def Ancho_Columna(df):
    len_col = {"": 0}
    for column in df:
        headcount = 0
        col_element_list = df[column]
        charcount = 0
        headuppcount = 0
        headlowcount = 0
        for character in str(column):
            if character.isupper() or character.isnumeric():
                headuppcount += 2
            elif character.islower():
                headlowcount += 1
        headcount = headuppcount + headlowcount

        for element in col_element_list:
            uppernumcount = 0
            lowercount = 0
            charcount_temp = 0

            for character in str(element):
                if character.isupper() or character.isnumeric():
                    uppernumcount += 2
                elif character.islower():
                    lowercount += 1
            charcount_temp = lowercount + uppernumcount
            if charcount_temp > charcount:
                charcount = charcount_temp
        if headcount > charcount:
            headict = {column: headcount}
            len_col |= headict
        else:
            charcountdict = {column: charcount}
            len_col |= charcountdict

    return len_col


print(Ancho_Columna(df))
