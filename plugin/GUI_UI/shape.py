class parts:
    def UI_set(self, data):
        data.new_territory("main")
        data.edit_territory_size("main", x=100, y=100)
        data.edit_territory_position("main", x=10, y=100)
        print(data.get_territory_contact("main"))

        return data
