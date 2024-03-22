from spyre import server
import pandas as pd

regions = {
    1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
    6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
    11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
    16: 'Рівенська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
    21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим'
}


class StockExample (server.App):
    title = "NOAA data vizualization"

    inputs = [{
        "type": "dropdown",
        "label": "NOAA data dropdown",
        "options": [
            {"label": "VCI", "value": "VCI"},
            {"label": "TCI", "value": "TCI"},
            {"label": "VHI", "value": "VHI"}
        ],
        "key": "ticker",
        "action_id": "update_data"
    },
    {
            "type": "dropdown",
            "label": "Оберіть область України",
            "options": [{"label": region_name, "value": str(region_index)} for region_index, region_name in regions.items()],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Оберіть інтервал тижнів",
            "key": "weeks_interval",
            "value": "9-10",
            "action_id": "update_data"
        },
        {
            "type":'slider',
            "label": 'Оберіть рік:',
            "min" : 1981,
            "max" : 2024,
            "key": 'year',
            "action_id" : "update_data"  
        }]
    
    tabs = ["Plot", "Table"]

    controls = [{"type": "hidden", "id": "update_data"}]


    outputs = [{
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        { "type": "table",
            "id" : "table_id",
            "control_id": "update_data",
            "tab" : "Table",
            "on_page_load": True }]

    def getData(self, params): #params is a dictionary containing all of the input values
        region = params['region']
        weeks = params['weeks_interval']
        year = params['year']
        colum = params['ticker']

        df = pd.read_csv("D:\\Mine\\University\\AD\\AD_labs\\lab3\\lab2.csv")  
        df = df[df['Area'] == int(region)]
        start_week, end_week = map(int, weeks.split('-'))
        df = df[(df['Week'] >= start_week) & (df['Week'] <= end_week) & (df['Year'] == year) ]
        df1 = df[['Year', 'Week', colum]]
        return df1

    def getPlot(self, params):
        df = self.getData(params)
        region = int(params['region'])
        weeks = params['weeks_interval']
        year = int(params['year'])
        colum = params['ticker']

        plt_obj = df.plot(x = "Week", y = colum, legend=False, figsize=(15, 5), color='green', linewidth=3)
        plt_obj.grid(linestyle = '--')
        plt_obj.set_xlabel('Week', color='purple', style= 'oblique', fontsize=12)
        plt_obj.set_ylabel(colum, color='purple', style='oblique', fontsize=12)
        plt_obj.set_title(f"Графік {colum} за {year} рік для {weeks} тижнів у обл. {regions[region]}", fontsize=14, color='blue', family='cursive')
        
        max_value = df[colum].max()
        max_position = df[colum].idxmax()
        max_x = df.loc[max_position, 'Week']
        max_y = df.loc[max_position, colum]
        plt_obj.annotate(f'max = {max_value}', xy=(max_x, max_y), xytext=(max_x + 1, max_y + 0.5), 
                        arrowprops=dict(facecolor='black', shrink=0.05))

        fig = plt_obj.get_figure()
        return fig
 

app = StockExample()
#app.launch(port=9093)