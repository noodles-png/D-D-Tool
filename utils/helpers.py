import os

def get_asset(filename):
    return os.path.join(os.path.dirname(__file__), "..", "assets", filename)

def get_modifier(value):
    """ Returns the calculated modifier based on the ability score """
    value = int(value)
    modifier = round((value - 10) // 2)
    return modifier

def get_prof_bonus(level):
    """ Returns the proficiency bonus based on character level """
    level = int(level)
    prof_bonus = (level // 4) + 1
    return prof_bonus

def get_spell_dc(prof_bonus, stat_modifier):
    """ Returns the spell difficulty check
     Args:
         prof_bonus: proficiency bonus calculated from get_prof_bonus
         stat_modifier: Ability score modifier calculated from get_modifier
     Returns:
         spell_dc: integer
     """
    spell_dc = 8 + prof_bonus + stat_modifier
    return spell_dc

