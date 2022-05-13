import PIL as pil
from PIL import Image


def print_list(l):
    print()
    for el in l:
        print(el)
    print()


 # les fonctions savings et loading on été prise dans les TDs
def saving(matPix, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(matPix),nbrLine(matPix)))
    for i in range(nbrLine(matPix)):
        for j in range(nbrCol(matPix)):
            toSave.putpixel((j,i),matPix[i][j])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return mat

def decode_Hamming74(b): # Done in class
    c1 = b[4] != (b[0] + b[1] + b[3])%2
    c2 = b[5] != (b[0] + b[2] + b[3])%2
    c3 = b[6] != (b[1] + b[2] + b[3])%2
    if c1 and c2 and c3:
        b[3] = (b[3] + 1) % 2
    elif c1 and c2:
        b[0] = (b[0] + 1) % 2
    elif c1 and c3:
        b[1] = (b[1] + 1) % 2
    elif c2 and c3:
        b[2] = (b[2] + 1) % 2
    return [b[0], b[1], b[2], b[3]]

# les fonctions nbrCol et nbrLine on été prise dans les TDs
# on utilise pas ces 2 fonctions, mais elles sont là...
def nbrCol(l):
    return len(l[0])
def nbrLine(l):
    return len(l)


def rotate_right(l, n=1):

    def rotate(l):
        rotated = []
        for i in range(len(l[0])):
            rotated.append([])
            for j in range(len(l)):
                rotated[i].append(l[len(l)-1-j][i])
        return rotated

    new_l = rotate(l)

    for _ in range(n-1): new_l = rotate(new_l)

    return new_l


def rotate_left(l, n=1):

    def rotate(l):
        rotated = []
        for i in range(nbrLine(l)):
            rotated.append([])
            for j in range(nbrCol(l)):
                rotated[i].append(l[j][len(l[0])-1-i])
        return rotated

    new_l = rotate(l)

    for _ in range(n-1): new_l = rotate(new_l)

    return new_l


def get_portion_of_mat(mat, start_x, start_y, end_x, end_y):
    l = []
    if start_x<=end_x and start_y<=end_y:
        for i in range(start_y, end_y):
            l.append(mat[i][start_x:end_x])

    return l


def correct_sens_QR(QR):
    global folder_path

    corner_filename = "coin.png"
    corner_top_left = loading(folder_path + corner_filename)
    corner_top_right = rotate_right(corner_top_left)
    corner_bottom_left = rotate_left(corner_top_left)

    part_top_left = get_portion_of_mat(QR, 0,0,len(corner_top_left[0]), len(corner_top_left))
    part_top_right = get_portion_of_mat(QR, len(QR)-len(corner_top_right[0]),0, len(QR),len(corner_top_right))
    part_bottom_left = get_portion_of_mat(QR, 0, len(QR)-len(corner_bottom_left), len(corner_bottom_left[0]), len(QR[0]))

    cond1 = part_top_left == corner_top_left
    cond2 = part_top_right == corner_top_right
    cond3 = part_bottom_left == corner_bottom_left

    counter = 4
    while not (cond1 and cond2 and cond3) and counter < 4:
        counter += 1
        QR = rotate_right(QR)

        part_top_left = get_portion_of_mat(QR, 0,0,len(corner_top_left[0]), len(corner_top_left))
        part_top_right = get_portion_of_mat(QR, len(QR)-len(corner_top_right[0]),0, len(QR),len(corner_top_right))
        part_bottom_left = get_portion_of_mat(QR, 0, len(QR)-len(corner_bottom_left), len(corner_bottom_left[0]), len(QR[0]))

        cond1 = part_top_left == corner_top_left
        cond2 = part_top_right == corner_top_right
        cond3 = part_bottom_left == corner_bottom_left

    return QR


def get_blocks(QR,n_blocks):

    def cut_list_in_4(l):
        new_l = []

        for i in range(len(l)):
            for j in range(0,len(l[i]),len(l[i])//4):
                new_l.append(l[i][j:j+len(l[i])//4])

        return new_l


    n_lines = n_blocks
    n_lines += 1 if n_lines%2==1 else 0

    start_x, start_y = len(QR)-14, len(QR[0])-n_lines

    l = get_portion_of_mat(QR, start_x, start_y, len(QR),len(QR[0]))
    # print_list(l)
    
    def reverse_list_in_list(l):
        for i in range(len(l)):
            temp = l[i]
            temp.reverse()
            l[i] = temp
        return l

    l.reverse()
    l = reverse_list_in_list(l)


    l_2blocks = []
    count = 0

    l_blocks_2order = []
    for i in range(0,len(l),2):
        if count%2 == 1:
            part_b1 = [l[i][0:7], l[i+1][0:7]]
            part_b2 = [l[i][7:14], l[i+1][7:14]]
        else:
            l_tmp1 = l[i]
            l_tmp1.reverse()

            l_tmp2 = l[i+1]
            l_tmp2.reverse()

            part_b1 = [l_tmp1[0:7], l_tmp2[0:7]]
            part_b2 = [l_tmp1[7:14], l_tmp2[7:14]]

        count += 1
        l_blocks_2order.extend([part_b2,part_b1])
        

    # print_list(l_blocks_2order)

    # rearrange elements
    l_blocks = []
    for i in range(len(l_blocks_2order)):
        l_blocks.append([])
        for j in range(len(l_blocks_2order[i][0])):
            l_blocks[i].extend([l_blocks_2order[i][0][6-j], l_blocks_2order[i][1][6-j]])

    # print_list(l_blocks)

    return l_blocks[:n_blocks]



def filter_QR(QR):
    ctrl_bit1 = QR[22][8]
    ctrl_bit2 = QR[23][8]
    ctrl_tuple = (ctrl_bit2, ctrl_bit1) # yes, reversed

    filtered = []
    for i in range(len(QR)):
        filtered.append([])
        for j in range(len(QR[i])):
            filtered[i].append(QR[i][j]^ctrl_tuple[(i+j)%2])

    return filtered

def total_decode(blocks):
    sentence = ""
    for block in blocks:
        characterBits = decode_Hamming74(block[:7]) + decode_Hamming74(block[7:len(block)])
        
        characterBits.reverse()
        s = ""
        for b in characterBits: s += str(b)


        # print(s, int(s,2), chr(int(s,2)))

        sentence += chr(int(s,2))

    return sentence


def get_results(QR):

    def get_number_of_blocks(QR):
        b = ""
        for k in range(12,17):
            b += str(QR[k][0])

        n_blocks = int(b,2)

        return n_blocks

    n_blocks = get_number_of_blocks(QR) # move at line 212 if needed after filter


    QR = correct_sens_QR(QR)
    # print_list(QR)
    QR = filter_QR(QR)

    blocks = get_blocks(QR, n_blocks)

    # if QR!= QR: print_list(QR)
    # print_list(QR)

    print("Result: ", total_decode(blocks))


    # print("\nControl b:")
    # print(QR[22][8], "# position = QR[22][8]")
    # print(QR[23][8], "# position = QR[23][8]")




folder_path = "Exemples/"

# Si vous êtes sur windows et que vous rencontrer une erreur de chemin d'accès,
# merci de supprimer les lignes avec """ ci-dessous
# ( = elenver le fait que ça soit en commentaire)
# Mais il n'y a pas de raison pour laquelle ça ne fonctionnerait pas! :D
"""
import os
# in a cmd, cd = path, and "> tmp" saved returned command in "tmp" file
os.system('cd > tmp')
# path is the main folder path
path = open('tmp', 'r').read().replace('\\', '/').replace('\n','') + "/"
folder_path = path + "Exemples/"
"""

QR_damier_filename = "qr_code_damier_ascii.png"
QR_filename = "qr_code_ssfiltre_ascii.png"
QR_rotated_filename = "qr_code_ssfiltre_ascii_rotation.png"
QR_ssfiltre_num_filename = "qr_code_ssfiltre_num.png"
l_QR = [QR_damier_filename, QR_filename, QR_rotated_filename, QR_ssfiltre_num_filename]


for QR in l_QR:
    print("\n" + QR_ssfiltre_num_filename)
    QR = loading(folder_path + QR_filename)
    get_results(QR)

input()
