import easygui as eg 
import pickle

itemlist = list()
in_list = list()
in_list.append(3)
in_list.append(8)
itemlist.append(1)
itemlist.append(in_list)
dict_save = {'lista_estados':'hola', 'lista_trans':'hola2', 'sprites_estados':'hola3',
					 'sprites_trans':'hola_4'}
#rint(itemlist)
extension = ["*.txt"]


archivo_o = eg.fileopenbox(msg="Abrir archivo",
                         title="Control: fileopenbox",
                         default='',
                         filetypes=extension)

with open(archivo_o, 'rb') as fp:
	iteml= pickle.load(fp)

for con in iteml['sprites_conexion']:
	print(con)