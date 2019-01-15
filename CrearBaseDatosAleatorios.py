# -*- coding: utf-8 -*-
"""
Created on Tue May 08 13:28:22 2018

@author: jose.lopeze
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

variables=['Sujeto', 'Edad', 'Talla', 'Peso', 'Sexo', 'Entreno', 'AlturaCMJ', 'AlturaSJ']


"""
df=pd.DataFrame(columns=['nº', 'Grupo', 'Repetidas', 'Medida'], index=range(n*len(grupos)*len(repetidas)))

for grupo in range(len(grupos)):
    for repet in range(len(repetidas)):
        for sujeto in range(n):
            print(sujeto, grupo, repet)
            df.iloc[grupo*len(repetidas)*n + repet*n + sujeto, 0]= sujeto
            df.iloc[grupo*len(repetidas)*n + repet*n + sujeto, 1]= grupo
            df.iloc[grupo*len(repetidas)*n + repet*n + sujeto, 2]= repet
"""         


N = 14
G = ['Entrenado', 'No entrenado', 'Control'] #grupos
R = ['pre', 'post'] #medidas repetidas
S = ['Hombre', 'Mujer'] #sexo

np.random.seed(2)
mediaVar1 = [[[40, 27, 25], [45, 30, 25]], [[33, 20, 21], [35, 25, 21.8]]] #orden: [chicos[pre][post]][chicas[pre][post]]
SDVar1 =     [[[2.6, 3.4, 3.6], [2, 3.9, 4.2]], [[2.8, 4.2, 4.7], [2.4, 4.1, 4.5]]]
 
mediaVar2 = [[[34, 15, 14], [37, 21, 14]], [[25, 10, 11], [30, 16, 10]]] #orden: [chicos[pre][post]][chicas[pre][post]]
SDVar2 = [[[3.5, 6.3, 6.6], [3.2, 5.4, 6.7]], [[3.9, 7.2, 7.7],[3.5, 7.01, 7.7]]]
 

numSujeto = np.array([i+1 for i in range(N)]*(len(G)*len(R)*2))
sexo= np.concatenate([np.array([s]*N*len(G)*len(R)) for s in S])
mediasVar1 = np.concatenate([np.repeat(value, N) for value in mediaVar1])
SDsVar1 = np.concatenate([np.repeat(value, N) for value in SDVar1])
datosVar1 = np.random.normal(mediasVar1, scale=SDsVar1, size=N*len(G)*len(R)*2)

mediasVar2 = np.concatenate([np.repeat(value, N) for value in mediaVar2])
SDsVar2 = np.concatenate([np.repeat(value, N) for value in SDVar2])
datosVar2 = np.random.normal(mediasVar2, scale=SDsVar2, size=N*len(G)*len(R)*2)


iv1 = np.concatenate([np.array([g]*N) for g in G]*len(R)*2) #factor prepost
iv2 = np.concatenate([np.array([r]*(N*len(G))) for r in R]*2) #factor grupo


datosEdad = np.random.normal(19, 4, size=N*len(G)*len(R)*2)#(mediasEdad, scale=SDsEdad, size=N*len(G)*len(R))

datosTalla = np.random.normal(1.8, 0.5, size=N*len(G)*len(R)*2)

datosMasa =np.random.normal(69, 10, size=N*len(G)*len(R)*2)

 
dfTabla=pd.DataFrame([numSujeto, datosEdad, datosTalla, datosMasa, sexo, iv1, iv2, datosVar1, datosVar2]).T
dfTabla.columns=['nº', 'Edad', 'Talla', 'Masa', 'Sexo', 'Grupo', 'Prepost', 'HCMJ', 'HSJ']
dfTabla.describe()
#from statsmodels.graphics.factorplots import interaction_plot  
#fig = interaction_plot(dfTabla['Prepost'], dfTabla['Grupo'], dfTabla['dependiente'],
#             colors=['red', 'blue', 'green'], markers=['D','^', '*'], ms=10)
#


colVar=['r','g','b']
sns.set_style({'lines.solid_capstyle': u'round',
               'lines.linewidth': 1,
               'lines.markersize': 10})

rc={'axes.labelsize': 'x-large', 'xtick.labelsize': 'large'}
with sns.plotting_context(rc=rc):  
    graycolors = sns.mpl_palette('Greys_r', 4)
    g = sns.factorplot(x='Prepost', y='HSJ', hue='Grupo', col='Sexo', data=dfTabla, ci='sd',
                               kind='point', capsize=.05, dodge=True, legend=False, palette=graycolors, size=6, aspect=.75)#1hue="Instrument", col="Skill", 
    g.set_titles('{col_name}', fontweight='bold') #para que ponga como título Walk y Run, no skill = walk...    
    g.set_axis_labels('', ) #quita el título general del eje X, ponía "position", pero parecía que se refería solo al del medio
    
    plt.legend(loc='best')


#guarda los datos
unidadDisco = 'F:'
carpetaOriginal = r'\Docencia\UMH\Asignaturas\Cursos\2018-SeminarioProgramacionAnalisisDatos\ArchivosEjemplos\BasesDatosEjemplos'

writer = pd.ExcelWriter(unidadDisco+carpetaOriginal+'\BaseDatosInvento.xlsx')#, engine='xlsxwriter')

dfTabla.to_excel(writer, sheet_name='Datos', index=False)

#Edad
mediasEdad = [[22, 19, 28], [19, 21, 20]] #orden: [[chicos][chicas]]
SDEdad = [[2.6, 3.4, 3.6], [2, 3.9, 4.2]]

mediasTalla = [[1.91, 1.77, 1.78], [1.78, 1.63, 1.62]] #orden: [[chicos][chicas]]
SDTalla = [[0.1, 0.3, 0.4], [0.2, 0.3, 0.3]]

mediasMasa = [[76, 78, 75], [58, 55, 56]] #orden: [[chicos][chicas]]
SDMasa = [[1.5, 2.3, 2.1], [0.8, 1.5, 1.2]]


dfDescrip=pd.DataFrame()

for h,sexo in enumerate(S):
    for i, grupo in enumerate(G):
        print(sexo, grupo, mediasEdad[h][i])
        dfDescrip['E'+sexo+grupo]=np.random.normal(mediasEdad[h][i], SDEdad[h][i], size=N)
        dfDescrip['T'+sexo+grupo]=np.random.normal(mediasTalla[h][i], SDTalla[h][i], size=N)
        dfDescrip['M'+sexo+grupo]=np.random.normal(mediasMasa[h][i], SDMasa[h][i], size=N)
dfDescrip.to_excel(writer, sheet_name='Descrip', index=False)
#mediasEdad = np.concatenate([np.repeat(value, N) for value in mediasEdad])
#SDsEdad = np.concatenate([np.repeat(value, N) for value in SDEdad])



writer.save()
