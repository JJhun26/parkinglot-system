from datetime import datetime

members = {
    '37바4821' : {
        'name' : 'kim',
        'discount' : 80,
    },
    '92가1034' : {
        'name' : 'park',
        'discount': 50,
    },
    '15나7749' : {
        'name' : 'lee',
        'discount' : 0,
    }
}

seats = [['♿', '♿', '♿', '⬛', '⬜', '🔋', '🔋', '🔋', '⬜', '⬜'],
         ['⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬛', '⬜', '⬜'],
         ['⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜'],
         ['⬜', '⬜', '⬛', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜', '⬜']]

occupied = {
    '25가1049' : {
        'position' : 'A4',
        'entrance' : '2025-04-04 17:30'
    },
    '53바5029' : {
        'position' : 'B1',
        'entrance' : '2025-07-15 18:30'
    },
    '10나5829' : {
        'position' : 'B8',
        'entrance' : '2025-01-13 19:30'
    },
    '90바2819' : {
        'position' : 'D3',
        'entrance' : '2025-05-12 20:30'
    }
    
}

special_position = [0, 1, 2, 5, 6, 7]

def alphabet_to_number(text):
    return ord(text.upper()) - 65

while True:
    run = input("Enter 'exit' to quit the system: ")
    if run == 'exit':
        break
    
    in_out = input("Enter in or out(1: in, 2: out): ")
    if in_out == '1':
        print(seats)
        
        restart = 0
        desire_pos = input("Enter your desired position(Ex: A5): ")
        desire_pos0 = alphabet_to_number(desire_pos[0])
        desire_pos1 = int(desire_pos[1])-1   
        for i in special_position:
            if (desire_pos0 == 0) and (desire_pos1==i):
                dis_or_elec = input("Are you disabled or have an electric vehicle?(d: disabled, e: electric, b: both, n:none): ")
                if dis_or_elec == 'n':
                    print("Invalid position")
                    restart +=1
                    break
                elif dis_or_elec == 'd':
                    if (desire_pos1 == 5) or (desire_pos1 == 6) or (desire_pos1 == 7):
                        print("Position for electric vehicles")
                        restart +=1
                        break
                elif dis_or_elec == 'e':
                    if (desire_pos1 == 0) or (desire_pos1 == 1) or (desire_pos1 == 2):
                        print("Position for disabled")
                        restart +=1
                        break
        if restart>=1:
            continue
                    
        if seats[desire_pos0][desire_pos1] == '⬛':
                print("Selected position is already occupied")
                empty_pos = []
                for i in range(len(seats)):
                    for j in range(len(seats[i])):
                        if seats[i][j] != '⬛':
                            empty_pos.append(f"{chr(i+65)}{j+1}")
                            if len(empty_pos)>=3:
                                break
                    if len(empty_pos)>=3:
                        break
                print(f"{empty_pos}is recommended")                
        else:
            seats[desire_pos0][desire_pos1] = '⬛'
            print("Successfully selected")
                
        car_num = input("Enter your car number(Ex: 12다1234): ")
        in_time = input("Enter your entrance time(YYYY-MM-DD HH:MM): ")
        
        occupied[car_num] = {
            'position' : desire_pos,
            'entrance' : in_time
        }
        print(seats)
        print(occupied)
            
    elif in_out == '2':
        car_num = input("Enter your car number(Ex: 12다1234): ")
        if car_num not in occupied:
            print("Invalid car number")
            continue
        print(occupied[car_num])
        
        out_time = input("Enter your out time(YYYY-MM-DD HH:MM)")
        in_dt = datetime.strptime(occupied[car_num]['entrance'], "%Y-%m-%d %H:%M")
        out_dt = datetime.strptime(out_time, "%Y-%m-%d %H:%M")
        diff = out_dt - in_dt
        
        total_30mins, _ = divmod(diff.total_seconds(), 1800) 
        if car_num in members:
            discount = members[car_num]['discount']
        else:
            discount = 0
            
        total_price = (total_30mins-1)*3000
        print(f"Your total price is {int(total_price)}won.")
        
        out_position = occupied[car_num]['position']
        out_pos1 = ord(out_position[0])-65
        out_pos2 = int(out_position[1])
        
        seats[out_pos1][out_pos2] = '⬜'
        print(seats)
        
        
    