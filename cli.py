def q_one():
    print("Great! I will ask you a series of questions, please answer as truthfully as you can.")
    print("If you wash your face and don?t apply any products, how does your skin behave 30 minutes after?")
    print("A. It feels dry")
    print("B. It feels calm, smooth, and soft")
    print("C. It feels uneven (oily in some parts and dry on the other parts)")
    print("D. It feels shiny and oily")
    answer = input().upper()
    while ord(answer) < 65 or ord(answer) > 68:
        answer = input("Sorry, I didn't get that. Please try again.\n").upper()
    return answer

def q_two():
    print("What does your skin typically look like at the end of the day?")
    print("A. My forehead and nose are very shiny and oily but my cheeks are matte.")
    print("B. Crazy oily.")
    print("C. Tight or splotchy. Like the desert. I need to put moisturizer on ASAP!")
    print("D. Dull and tired. It feels mostly dry.")
    print("E. My complexion is only slightly oily at the end of the day.")
    print("F. I have some redness and irritation when exposed to skincare products or other environmental factors.")
    print("G. It looks normal. Not overly dry or oily.")
    answer = input().upper()
    while ord(answer) < 65 or ord(answer) > 71:
        answer = input("Sorry, I didn't get that. Please try again.\n").upper()
    return answer

def q_three():
    print("Describe your pores.")
    print("A. My pores are large, visible, and sometimes clogged all over my face.")
    print("B. Depends on where they are on my face. My pores are medium to large around my T-zone.")
    print("C. Small to medium-sized. My pores are small and not visible.")
    print("D. They seem to change with the day. My pores are visible but small.")
    answer = input().upper()
    while ord(answer) < 65 or ord(answer) > 68:
        answer = input("Sorry, I didn't get that. Please try again.\n").upper()
    return answer

def q_four():
    print("How frequently do you have breakouts or active acne lesions?")
    print("A. Frequent")
    print("B. Seldom")
    answer = input().upper()
    while answer != "A"  and answer != "B":
        answer = input("Sorry, I didn't get that. Please try again.\n").upper()
    return answer

def q_five():
    print("Have you ever had a sunburn or noticed pigmentation changes after sun exposure?")
    print("A. Yes")
    print("B. No")
    answer = input().upper()
    while answer != "A"  and answer != "B":
        answer = input("Sorry, I didn't get that. Please try again.\n").upper()
    return answer


def start():
    answer = input("Hello, <name>! I am the Scire Technology Bot.\nIf you'd like me to assess your skin type, press S. Otherwise, press C to quit.\n").upper()

    while answer != "S" and answer != "C":
        answer = input("Sorry, I didn't get that. Please try again.\n").upper()
    return answer

def assessment(skin_type, acne_prone, sun_sensitive):
    print("Thank you, <name> for answering the questions!\nHere's your assessment:")
    print("Skin Type: " + skin_type)
    print("Acne Prone: " + acne_prone)
    print("Sun-Sensitive: " + sun_sensitive)
    print("If you have any more questions or need further assistance, feel free to ask!")


# Main
answer = start()

if answer == "S" or answer == "s":
    answer = q_one()
    
    if answer == "A":
        answer = q_two()
        if answer == "C" or answer == "D":
            answer = q_three()
            skin_type = "Dry"

        elif answer == "G":
            answer = q_three()
            skin_type = "Normal"

        elif answer == "A" or answer == "B" or answer == "E":
            answer = q_three
            skin_type = "Combination"
        
        elif answer == "F":
            answer = q_three()
            skin_type = "Sensitive"

    elif answer == "B":
        answer = q_two()
        if answer == "B":
            answer = q_three()
            if answer == "A":
                skin_type = "Oily"
            else:
                skin_type = "Normal"
        
        elif answer == "C" or answer == "D":
            answer = q_three()
            if answer == "B":
                skin_type = "Combination"
            else:
                skin_type = "Dry"

        elif answer == "A" or answer == "E":
            answer = q_three()
            skin_type = "Combination"

        elif answer == "F":
            answer = q_three()
            skin_type = "Sensitive"
    
    elif answer == "C":
        answer = q_two()
        if answer == "F":
            answer = q_three()
            skin_type = "Sensitive"
        elif answer == "B":
            answer = q_three()
            if answer == "A" or answer == "B":
                skin_type = "Oily"
            elif answer == "C" or answer == "D":
                skin_type = "Combination"
        else:
            answer = q_three()
            skin_type = "Combination"
    
    elif answer == "D":
        answer = q_two()
        if answer == "F":
            answer = q_three()
            skin_type = "Sensitive"
        elif answer == "A" or answer == "E":
            answer = q_three()
            skin_type = "Combination"
        elif answer == "G":
            answer = q_three()
            if answer == "A" or answer == "B":
                skin_type = "Oily"
            else:
                skin_type = "Combination"
        else:
            answer = q_three()
            skin_type = "Oily"
    

    answer = q_four()
    if answer == "A":
        acne_prone = "Acne Prone"
    else:
        acne_prone = "Not Acne Prone"

    answer = q_five()
    if answer == "A":
        sun_sensitive = "Sun Sensitive"
    else:
        sun_sensitive = "Not Sun Sensitive"
    
    assessment(skin_type, acne_prone, sun_sensitive)

else:
    print("That's okay! If you change your mind, I'm here to help")
    


