import pyecharts.options as opts
from pyecharts.charts import BMap
from pyecharts.commons.utils import JsCode
import spider

for i in range(0, 7):
    date_list, weather_list = spider.get_data()
    weather_list = weather_list[i]
    china_map = BMap(init_opts=opts.InitOpts(width="1400px", height="800px"), is_ignore_nonexistent_coord=True).add(
        type_="effectScatter",
        series_name="temperature",
        data_pair=weather_list,
        symbol_size=10,
        effect_opts=opts.EffectOpts(),
        label_opts=opts.LabelOpts(formatter="{a}", position="right", is_show=False),
        itemstyle_opts=opts.ItemStyleOpts(color="#00F5FF"),
    )

    china_map.add_schema(
        baidu_ak="tiALGwQmhrUISdDd5URUILWN0Ttw8eLF",
        center=[104.114129, 37.550339],
        zoom=5,
        is_roam=True,
        map_style={
            "styleJson": [
                {
                    'featureType': 'water',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                },
                {
                    'featureType': 'land',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#f3f3f3'
                    }
                },
                {
                    'featureType': 'railway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                },
                {
                    'featureType': 'highway',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#fdfdfd'
                    }
                },
                {
                    'featureType': 'highway',
                    'elementType': 'labels',
                    'stylers': {
                        'visibility': 'off'
                    }
                },
                {
                    'featureType': 'arterial',
                    'elementType': 'geometry',
                    'stylers': {
                        'color': '#fefefe'
                    }
                },
                {
                    'featureType': 'arterial',
                    'elementType': 'geometry.fill',
                    'stylers': {
                        'color': '#fefefe'
                    }
                },
                {
                    'featureType': 'poi',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                },
                {
                    'featureType': 'green',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                },
                {
                    'featureType': 'subway',
                    'elementType': 'all',
                    'stylers': {
                        'visibility': 'off'
                    }
                },
                {
                    'featureType': 'manmade',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                },
                {
                    'featureType': 'local',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                },
                {
                    'featureType': 'arterial',
                    'elementType': 'labels',
                    'stylers': {
                        'visibility': 'off'
                    }
                },
                {
                    'featureType': 'boundary',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#fefefe'
                    }
                },
                {
                    'featureType': 'building',
                    'elementType': 'all',
                    'stylers': {
                        'color': '#d1d1d1'
                    }
                },
                {
                    'featureType': 'label',
                    'elementType': 'labels.text.fill',
                    'stylers': {
                        'color': '#999999'
                    }
                },
            ]
        }
    )
    china_map.set_global_opts(
        title_opts=opts.TitleOpts(
            title=date_list[i] + '全国温度展示',
            subtitle='日期:' + date_list[i],
            pos_left="left",
            title_textstyle_opts=opts.TextStyleOpts(color="#FF6A6A"),
        ),
        tooltip_opts=opts.TooltipOpts(trigger="item", formatter=JsCode(
            "function(params){return params.data.name+'<br/>'+params.data.value[2];}"))
    )

    china_map.render("./全国温度展示" + date_list[i] + '.html')
