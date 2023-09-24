def color_sheme(request):
    #http://colormind.io/bootstrap/
    color_sheme = {
        "lightShades_color" : "#F3F1EF",
        "lightAccent_color" : "#74777B",
        "mainBrand_color" : "#857E9F",
        "darkAccent_color" : "#74516E",
        "darkShades_color": "#2A283D",
    }
    breakpoint = {'500px'}

    """
    color_sheme = {
        "lightShades_color" : "#F3EFEA",
        "lightAccent_color" : "#39CDCE",
        "mainBrand_color" : "#8476E9",
        "darkAccent_color" : "#777696",
        "darkShades_color": "#1E4299",
    }"""
    return color_sheme

def breakpoint(request):
    breakpoint = {'breakpoint' : '600px',
                  'minWidth' : '400px'}
    return breakpoint
