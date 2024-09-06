
class CountResult:
    def __init__(self, PR, ConvertDamage, soldierDamage, damage, probability, effect):
        self.PR = PR
        self.ConvertDamage = ConvertDamage
        self.soldierDamage = soldierDamage
        self.damage = damage
        self.probability = probability
        self.effect = effect


def CritBlade(soldierDamage, damage, probability, crit):
    if ((damage == 0 or 2 <= damage <= 10) and 20 <= probability <= 40 and
            150 <= crit <= 180):

        if(soldierDamage == 0):
            soldierDamage = 7
            soldierKind = "1等獵人"
        else:
            soldierKind = "同等士兵"

        if(damage == 0):
            attackMax = (soldierDamage) * (1 + 0.8 * 0.4) 
            attackMini = (soldierDamage) * (1 + 0.5 * 0.2)
        else:
            attackMax = (10 + soldierDamage) * (1 + 0.8 * 0.4) 
            attackMini = (2 + soldierDamage) * (1 + 0.5 * 0.2)

        Point = (attackMax - attackMini) / 100
        R = (damage + soldierDamage) * (1 + probability * (crit - 100) / 10000)
        ConvertDamage = f"約為{soldierKind}裝備+{round((damage + soldierDamage) * (1 + probability * (crit - 100) / 10000) - soldierDamage, 1)}的鐵劍噢"
        PR = (R - attackMini) / Point
        OutputPR = f"PR：{int(PR)}"
        
        soldierDamage = f"\n士兵攻擊力：{soldierDamage}"
        damage = f"\n裝備攻擊力：{damage}"
        probability = f"\n爆擊機率：{probability}%"
        crit = f"\n爆擊效果：{crit}%"
        
        if PR == 100:
            Result = CountResult("咩選裝備", ConvertDamage, soldierDamage, damage, probability, crit)
        else:
            Result = CountResult(OutputPR, ConvertDamage, soldierDamage, damage, probability, crit)
        return Result
    else:
        return CountResult(None, None)


def QiankunSaber(soldierDamage, damage, probability, BonusDamage):
    if ((damage == 0 or 2 <= damage <= 7) and 20 <= probability <= 50 and
            50 <= BonusDamage <= 100):
        print("Values are within valid range.")
        
        if(soldierDamage == 0):
            soldierDamage = 7
            soldierKind = "1等獵人"
        else:
            soldierKind = "同等士兵"

        if(damage == 0):
            attackMax = (soldierDamage) * (1 + 1 * 0.5 * 2)
            attackMini = (soldierDamage) *(1 + 0.5 * 0.2 * 2)
        else:
            attackMax = (7 + soldierDamage) * (1 + 1 * 0.5 * 2)
            attackMini = (2 + soldierDamage) *(1 + 0.5 * 0.2 * 2)

        Point = (attackMax - attackMini) / 100
        R = (damage + soldierDamage) * (1 + probability * BonusDamage * 2 / 10000)
        ConvertDamage = f"約為{soldierKind}裝備+{round((damage + soldierDamage) * (1 + probability * (BonusDamage - 100) / 10000) - soldierDamage, 1)}的鐵劍噢"
        PR = (R - attackMini) / Point
        OutputPR = f"PR：{int(PR)}"

        soldierDamage = f"\n士兵攻擊力：{soldierDamage}"
        damage = f"\n裝備攻擊力：{damage}"
        probability = f"\n擴散機率：{probability}%"
        BonusDamage = f"\n擴散效果：{BonusDamage}%"

        if PR == 100:
            print("PR is 100, setting special equipment result.")
            Result = CountResult("咩選裝備", ConvertDamage, soldierDamage, damage, probability, BonusDamage)
        else:
            print("PR is 100, setting special equipment result.")
            Result = CountResult(OutputPR, ConvertDamage, soldierDamage, damage, probability, BonusDamage)
        return Result
    else:
        print("Invalid values, returning None.")
        return CountResult(None, None)
