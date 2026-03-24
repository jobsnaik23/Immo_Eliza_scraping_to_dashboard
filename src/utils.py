def get_province(postcode):
    try:
        pc = int(postcode)
        if 1000 <= pc <= 1299: return 'Brussels'
        if 1300 <= pc <= 1499: return 'Walloon Brabant'
        if 1500 <= pc <= 1999 or 3000 <= pc <= 3499: return 'Flemish Brabant'
        if 2000 <= pc <= 2999: return 'Antwerp'
        if 3500 <= pc <= 3999: return 'Limburg'
        if 4000 <= pc <= 4999: return 'Liège'
        if 5000 <= pc <= 5999: return 'Namur'
        if 6000 <= pc <= 6599 or 7000 <= pc <= 7999: return 'Hainaut'
        if 6600 <= pc <= 6999: return 'Luxembourg'
        if 8000 <= pc <= 8999: return 'West Flanders'
        if 9000 <= pc <= 9999: return 'East Flanders'
    except:
        return 'Unknown'
    return 'Unknown'