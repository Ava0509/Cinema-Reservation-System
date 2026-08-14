#one-time execution
"""
layout = (['A',12], ['B',12], ['C',12], ['D',12],
          ['E',10], ['F',10], ['G',10], ['H',10],
          ['I',8], ['J',8], ['K',8], ['L',8])

with open("sample_data.sql","a") as file:
    for screen in range(1,11):
        for row, seats in layout:
            if row in ('A','B','C','D'):
                category = 1
            elif row in ('E','F','G','H'):
                category = 2
            else:
                category = 3
                
            for seat in range(1, seats+1):
                seat_number = f"{row}{seat}"
                file.write(f"insert into Seats(ScreenID, Seat_Number, CategoryID)"
                           f"values ({screen}, '{seat_number}', {category});\n")

""