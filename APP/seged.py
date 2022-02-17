def dictzip(szoveg):
    sorok = szoveg.strip().split('\n')
    mezonevek = sorok[0].strip().split('\t')+['sor']
    rekordok = list(map(lambda sor : dict(zip(mezonevek, sor.strip().split('\t')+[sor])), sorok[1:]))
    return rekordok
