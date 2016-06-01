"""
Srishti Jindal (13258365)
01 June 2016

This system permits individuals to hire things.

for example, employ a thing, give back a thing, and include new things.

The Default perspective is rundown all things. For including new things there is a pop up window.

This has been created by python and kivy as GUI.

git hub repository:
"""






from kivy.app import App
from kivy.app import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class itemhire(App):
    def __init__(self, **kwargs):
        super(itemhire, self).__init__(**kwargs)
        input_file = open("items.csv","r")
        self.status_text = ""
        self.mode = '1'
        self.itemToHire = []
        self.itemToReturn = []
        self.itemlist = []
        for line in input_file:
            self.itemlist.append(line.strip().split(","))
        input_file.close()

    def build(self):
        self.root = Builder.load_file("SrishtiJindalA2.kv")
        self.create_item_buttons()
        return self.root

    def create_item_buttons(self):
        """

        :return: None
        """
        self.root.ids.itemBox.clear_widgets()
        for item in self.itemlist:
            # create a button for each item entry
            temp_button = Button(text=item[0])
            temp_button.bind(on_release=self.press_entry)
            # add the button to the "itemBox" using add_widget()
            if(item[3]=="in"):
                temp_button.background_color = 0,1,4,2
            else:
                temp_button.background_color = 2,6,2,2
            self.root.ids.itemBox.add_widget(temp_button)

    def press_entry(self, instance):
        """
        Handler for pressing entry buttons
        :param instance: the Kivy button instance
        :return: None
        """
        # update status text
        itemname = instance.text
        if self.mode == '1':
            for item in self.itemlist:
                if item[0]== itemname:
                    self.root.ids.statusLabel.text = item[0] + "," + item[1] + "," + str(item[2]) + "," + item[3]
                    # set button state
                     #instance.state = "down"
        elif self.mode =='2':
            for item in self.itemlist:
                if item[0] ==itemname:
                    if item[3] == 'in':
                        if item not in self.itemToHire:
                            instance.state = 'down'
                            self.itemToHire.append(item)
                        else:
                            instance.state = 'normal'
                            self.itemToHire.remove(item)
                    elif item[3] == 'out':
                        pass

        elif self.mode =='3':
            for item in self.itemlist:
                if item[0] == itemname:
                    if item[3] == 'out':
                        if item not in self.itemToReturn:
                            instance.state = 'down'
                            self.itemToReturn.append(item)
                        else:
                            instance.state = 'normal'
                            self.itemToReturn.remove(item)
                    elif item[3] == 'out':
                        pass
    def press_clear(self):
        """
        Clear any buttons that have been selected (visually) and reset status text
        :return: None
        """
        # use the .children attribute to access all widgets that are "in" another widget
        for instance in self.root.ids.itemBox.children:
            instance.state = 'normal'
        self.status_text = ""

    def press_add(self):
        """
        Handler for pressing the add button
        :return: None
        """
        self.status_text = "Enter details for new item entry"
        # this opens the popupn
        self.root.ids.popup.open()

    def press_save(self, added_name, added_description , added_cost):
        """
        Handler for pressing the save button in the add entry popup - save a new entry to memory
        :param added_name: name text input (from popup GUI)
        :param added_description: description text input
        :param added_cost: cost text input (string)
        :return: None
        """
        newItem = [added_name,added_description,added_cost,"in"]
        self.itemlist.append(newItem)

        # change the number of columns based on the number of entries (no more than 5 rows of entries)
        self.root.ids.itemBox.cols = 2
        # add button for new entry (same as in create_item_buttons())
        temp_button = Button(text=newItem[0])
        temp_button.bind(on_press=self.press_entry)
        temp_button.background_color = 0,1,4,2
        self.root.ids.itemBox.add_widget(temp_button)
        # close popup
        self.root.ids.popup.dismiss()
        self.clear_fields()

    def clear_fields(self):
        """
        Clear the text input fields from the add entry popup
        If we don't do this, the popup will still have text in it when opened again
        :return: None
        """
        self.root.ids.addedName.text = ""
        self.root.ids.addedDescription.text = ""
        self.root.ids.addedCost.text = ""

    def press_cancel(self):
        """
        Handler for pressing cancel in the add entry popup
        :return: None
        """
        self.root.ids.popup.dismiss()
        self.clear_fields()
        self.status_text = ""

    def press_list(self):
        self.mode = '1'

    def press_hire(self):
        self.mode = '2'
    def press_return(self):
        self.mode = '3'

    def press_confirm(self):
        print(self.itemToHire)
        for each in self.itemToHire:
            hiring = [each[0], each[1], each[2], 'out']
            self.itemlist.remove(each)
            self.itemlist.append(hiring)
        for each in self.itemToReturn:
            returning = [each[0], each[1], each[2], 'in']
            self.itemlist.remove(each)
            self.itemlist.append(returning)
        self.create_item_buttons()
        self.press_clear()
        self.itemToHire = []
        self.itemToReturn = []
def return_item(list_of_items):

    new_list_of_items = list_of_items
    length_of_list = len(list_of_items)
    error_marker = 0
    while error_marker == 0:
        try:
            choice = int(input("Enter the number of an item to return: "))
            error_marker = 1
        except ValueError:
            print("Invalid input, enter a number")
            error_marker = 0

    while (choice > length_of_list) or (choice < 0):
        error_marker3 = 0
        while error_marker3 == 0:
            try:
                choice = int(input("Invalid item number: "))
                error_marker3 = 1
            except ValueError:
                print("Invalid input, enter a valid number")
                error_marker3 = 0

    checked_item = list_of_items[choice]
    while (checked_item[3]) != 'out':
        print("That item is not on hire")
        error_marker2 = 0
        while error_marker2 == 0:
            try:
                choice = int(input("Enter a valid number: "))
                error_marker2 = 1
            except ValueError:
                choice = input("Invalid input, enter a number")
                error_marker2 = 0

        while (choice > length_of_list) or (choice < 0):
            print("Invalid item number: ")
            error_marker4 = 0
            while error_marker4 == 0:
                try:
                    choice = int(input("Enter a valid number: "))
                    error_marker4 = 1
                except ValueError:
                    choice = input("Invalid input, enter a number")
                    error_marker4 = 0

        checked_item = list_of_items[choice]

    print("{} returned".format(checked_item[0]))

    checked_item[3] = "in"

itemhire().run()