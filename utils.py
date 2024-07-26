from io import StringIO
from html.parser import HTMLParser
import re

def getIndexes(df, value):
    # Empty list
    listOfPos = []

    # isin() method will return a dataframe with
    # boolean values, True at the positions   
    # where element exists
    result = df.isin([value])

    # any() method will return
    # a boolean series
    seriesObj = result.any()

    # Get list of column names where
    # element exists
    columnNames = list(seriesObj[seriesObj == True].index)

    # Iterate over the list of columns and
    # extract the row index where element exists
    for col in columnNames:
        rows = list(result[col][result[col] == True].index)

        for row in rows:
            listOfPos.append((row, col))

    # This list contains a list tuples with
    # the index of element in the dataframe
    return listOfPos




class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()



def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data().replace('*', '').replace('#', '')




def spread_choices_by_list(df, column_name, unique_answers):
    # Create a regex pattern from the unique answers
    pattern = '|'.join(re.escape(answer) for answer in unique_answers)
    
    # Function to split the string by the unique answers
    def split_by_answers(s):
        return re.findall(pattern, s)
    
    # Apply the split function to the specified column and explode
    df_expanded = df.assign(**{column_name: df[column_name].apply(split_by_answers)}).explode(column_name)
    
    return df_expanded



UNIQUE_ANSWERS = {
    '12':['Коррупция',
          'Ортиқча хужжатлар талаб қилиш (бюрократия)',
          'Таниш-билишчилик',
          'Ходимлар малакаси етарли эмас',
          'Хизмат вазифасини суистеъмол қилиш',
          'Норматив хужжатлар ижроси таъминланмайди',
          'Текширувлар сони кўп',
          'Мурожаат ва муаммолар ўз вақтида ҳал қилинмайди',
          'Кўп ҳисобот сўралади',
          'Бошқа']
}