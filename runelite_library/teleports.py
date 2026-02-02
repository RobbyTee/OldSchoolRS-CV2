# Write out all the Spellbook teleports and Jewelry teleports with checks here.
# Example: Teleport to Falador and wait for a special tile to appear; return True

# Jewelry will take an input of which teleport you choose from that jewelry
# Jewelry(worn=False)

# TODO: Set verification tiles.

from pyautogui import press
from runelite_library.filters import wait
from runelite_library.interaction import click, right_click
from runelite_library.check_charges import check_charges, log_use
from time import sleep
from too_many_items import Interfaces, Normal_Spellbook, Menu, Jewelry

class TeleportSpells:
    def __init__(self):
        """
        Use this like TeleportSpells().home() instead of initializing
        the class with t = TeleportSpells() then t.home().

        Opens the spellbook interface in __init__
        """
        press(Interfaces.spells_icon)

        
    def home(self) -> bool:
        """
        Return home teleport.
        """
        if not click(wait(template=Normal_Spellbook.home_tele)):
            return False
        else:
            sleep(3)
            return True


    def varrock(self) -> bool:
        """
        Teleports to Varrock.
        """
        if not click(wait(template=Normal_Spellbook.varrock_tele)):
            return False
        else:
            sleep(3)
            return True
        

    def lumbridge(self) -> bool:
        """
        Teleports to Lumbridge.
        """
        if not click(wait(template=Normal_Spellbook.lumby_tele)):
            return False
        else:
            sleep(3)
            return True
        
    
    def falador(self) -> bool:
        """
        Teleports to Falador.
        """
        if not click(wait(template=Normal_Spellbook.falador_tele)):
            return False
        else:
            sleep(3)
            return True
        

    def house(self, outside=False) -> bool:
        """
        Teleports to House.

        :outside: if True, will right click house teleport
        and click "Outside" from the dropdown menu.
        """
        if outside:
            if not right_click(wait(template=Normal_Spellbook.house_tele)):
                return False
            if not click(wait(template=Menu.outside)):
                return False
        else:
            if not click(wait(template=Normal_Spellbook.house_tele)):
                return False
        
        sleep(3)
        return True
    

    def camelot(self) -> bool:
        """
        Teleports to Camelot.
        """
        if not click(wait(template=Normal_Spellbook.camelot_tele)):
            return False
        else:
            sleep(3)
            return True
        

    def ardougne(self) -> bool:
        """
        Teleports to Ardougne.
        """
        if not click(wait(template=Normal_Spellbook.ardy_tele)):
            return False
        else:
            sleep(3)
            return True
        

class TeleportJewlery:
    def __init__(self):
        """
        Right clicks jewelry in inventory, rubs it, then chooses a location.
        """
        pass


    def digsite_pendant(self, location:str) -> bool:
        """
        :location: digsite, fossil_island
        """
        if not right_click(wait(template=Jewelry.digsite_pendant)):
            return False
        if not click(wait(template=Menu.rub)):
            return False
        
        sleep(2)

        if location == "digsite":
            press("1")
        elif location == "fossil_island":
            press("2")
        
        sleep(3)
        return True
        
    
    def explorers_ring(self) -> bool:
        """
        Teleports to the cabbage patch near Draynor
        """
        if not right_click(wait(template=Jewelry.explorers_ring)):
            return False
        if not click(wait(template=Menu.teleport)):
            return False
        
        log_use("explorers_ring")
        
        sleep(3)
        return True
    

    def right_of_dueling(self, location:str) -> bool:
        """
        :location: emirs_arena, castle_wars, ferox_enclave, 
        fortis_colosseum
        """
        if not right_click(wait(template=Jewelry.ring_of_dueling)):
            return False
        if not click(wait(template=Menu.rub)):
            return False
        
        teleports = {
            "emirs_arena": "1",
            "castle_wars": "2",
            "ferox_enclave": "3",
            "fortis_colosseum": "4"
        }
        
        sleep(2)

        if location in teleports.keys():
            press(teleports.get(location))
            sleep(3)
            return True
        else:
            return False


    def skills_necklace(self, location:str) -> bool:
        """
        :location: fishing_guild, mining_guild, crafting_guild,
        cooking_guild, woodcutting_guild, farming_guild
        """
        if not right_click(wait(template=Jewelry.skills_necklace)):
            return False
        if not click(wait(template=Menu.rub)):
            return False
        
        teleports = {
            "fishing_guild": "1",
            "mining_guild": "2",
            "crafting_guild": "3",
            "cooking_guild": "4",
            "woodcutting_guild": "5",
            "farming_guild": "6"
        }

        sleep(2)
        
        if location in teleports.keys():
            press(teleports.get(location))
            sleep(3)
            return True
        else:
            return False