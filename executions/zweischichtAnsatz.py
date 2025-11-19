"""
@Name: apso_finalerAnsatz_B
@Autor: Yann Rutschke
@E-Mail: yann.rutschke@student.kit.edu
@Created: 31.08.2023
@Description: Use an apso which is parallelized over the population. The parameter vector is calculated in two time
              here: first the dimension reduction model is used. Then the results are used in the model with 17 para-
              meters. This program is using two different reference drive (Seg3 and spezSeg3).
"""
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize
import numpy as np
from pymoo.core.problem import Problem
import csv
import matlab.engine
import pandas as pd

class MyProblem(Problem):


    # statischen Variablen die für die parallele Ausführung und die Verwendung von verschiedene Modelle benötigt werden.
    static_n_pop = 0
    static_case = 0
    static_xSimRefArray = 0
    static_n_var = 17
    static_xl = [100000*0, 1500000000*0, 1000*0, 100000*0, 100000000*0, 500*0, 250*0, 100000*0, 200000000*0, 0.00029*0, 0.075, 1*0, 200000*0, 0.97, 55/24*0.99, 0.019, 0.00451*0]    #-100% Abweichung nur W.Grad auf 0.9
    static_xu = [100000*2, 1500000000*2, 1000*2, 100000*2, 100000000*2, 500*2, 250*2, 100000*2, 200000000*2, 0.00029*2, 0.076, 1*2, 200000*2, 0.98, 55/24, 0.02, 0.00451*2]     #+100% Abweichung nur W.Grad auf 1
    # static_n_var, static_xl und static_xu werden überschrieben.

    def __init__(self, **kwargs):
        super().__init__(n_var=self.__class__.static_n_var,
                         n_obj=1,
                         xl=np.array(self.__class__.static_xl),
                         xu=np.array(self.__class__.static_xu),
                         var_type=float,
                         **kwargs)


    def _evaluate(self, x, out, *args, **kwargs):


        # Hier ist x eine Matrix der größe (n_pop,17)
        x = x.tolist()      # numpy.array wird hier zu einer Liste einer List umgewandelt. Einträge sind Float.

        # Für jeden Fall gibt es ein anderes simulinkModell und eine andere Anzahl an Abtastpunkte.
        # Gleiches gilt mit der Startposition. Achtung: 'Stoptime' muss noch in den Modelle eingestellt werden
        # und ist gleich: stop Time = 0,002*(n_abtastpunkte-1)
        if self.__class__.static_case == 1:
            n_abtastpunkte = 2001
            eng.assignin('base', 'start_position', matlab.double(-50), nargout=0)
            simulinkModell = 'xAchse_Sim_GR_GA_nR_seg3_17V'

        elif self.__class__.static_case == 2:
            n_abtastpunkte = 2001
            eng.assignin('base', 'start_position', matlab.double(-50), nargout=0)
            simulinkModell = 'xAchse_Sim_GR_GA_nR_SpezSeg4_17V'

        # Parallele Version final
        # Erzeugen simulinkSimulationInputArray und durchfuehren der parallele Simulation

        matlab_matrix = matlab.double(x)
        eng.workspace['iN'] = eng.simulinkSimulationInputArray(matlab_matrix, self.__class__.static_n_pop, simulinkModell)
        eng.workspace['aut'] = eng.parsim(eng.workspace['iN'], 'TransferBaseWorkspaceVariables', 'on')

        xSimS = np.empty((self.__class__.static_n_pop, n_abtastpunkte))

        for i in range(0, self.__class__.static_n_pop):

            xSim = eng.getxSim(eng.workspace['aut'], i+1)
            xSim = np.squeeze(xSim)
            xSimS[i] = xSim - np.squeeze(self.__class__.static_xSimRefArray)

        out["F"] = np.sum(abs(xSimS), axis=1)


def new_referenceDrive(case, x_l, x_u):
    """
            Write the csv data file for the examined case. Here two case are present 1 with the model with dimension .
            reduction and one with the model with 17 parameters.

                Parameters
                ----------
                case : int
                    Defines which model is used.
                    case = 1 : Model 17 Parameters with Seg3
                    case = 2 : Model 17 parameter with spezSeg3
                x_l : double list
                    Defines lower bound of the parameter vector
                x_u : double list
                    Defines upper bound of the parameter vector


                Returns
                -------
                void : a csv file is written

                See Also
                --------
                Examples
                --------
                #>>> new_referenceDrive(2)



                """
    #---------Berechnung von xSimRef-----------------

    c = matlab.double(vector=[100000, 1500000000, 1000, 100000, 100000000, 500, 250, 100000, 200000000, 0.00029, 0.076,
                              1, 200000, 0.98, 55/24, 0.02, 0.00451])
    eng.assignin('base', 'c', c, nargout=0)

    # Für finalerAnsatz_A gibt es in der Realität keine Unterscheidung zwischen den Referenz-Modelle da die gleiche
    # Referenzfahrt verwendet werden. In finalerAnsatz_B wird dieser Abschnitt tatsächlich witig sein.

    if case == 1:
        eng.assignin('base', 'start_position', matlab.double(-50), nargout=0)
        eng.sim("xAchse_Sim_GR_GA_nR_seg3_17V.slx")

    elif case == 2:
        eng.assignin('base', 'start_position', matlab.double(-50), nargout=0)
        eng.sim("xAchse_Sim_GR_GA_nR_SpezSeg4_17V")

    xSimRef = np.array(eng.workspace['x_Sim'])
    xSimRefArray = xSimRef.reshape(1, xSimRef.size)

    with open("apso_100proz_zweischicht_Seg3_SpezSeg3_Fall_{}.csv".format(case), "w", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        titel = ["Variable1", "Variable2", "Variable3", "Variable4", "Variable5", "Variable6", "Variable7",
                     "Variable8", "Variable9", "Variable10", "Variable11", "Variable12", "Variable13", "Variable14",
                     "Variable15", "Variable16", "Variable17", "beste Fitness", "Zeit"]

        if case == 2:
            titel = ["Variable1", "Variable2", "Variable3", "Variable4", "Variable5", "Variable6", "Variable7",
                     "Variable8", "Variable9", "Variable10", "Variable11", "Variable12", "Variable13", "Variable14",
                     "Variable15", "Variable16", "Variable17", "beste Fitness", "Zeit"]



        for i in range(1, n_gen + 1):  # Fitnessverlauf für Dataframe
            titel.append("Fitnessverlauf{}".format(i))

        writer.writerow(titel)

        i = 0



        while i < 10:
            MyProblem.static_n_pop = n_pop
            MyProblem.static_case = case
            MyProblem.static_xSimRefArray = xSimRefArray
            MyProblem.static_xl = x_l
            MyProblem.static_xu = x_u

            if case == 1 or case == 2:
                MyProblem.static_n_var = 17
            #else:
                #MyProblem.static_n_var = 17

            res = minimize(problem=MyProblem(),
                           algorithm=algorithm,
                           termination=("n_gen", n_gen),
                           eliminate_duplicates=True,
                           verbose=True,
                           save_history=True)
            print('res: ', res)
            print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
            print("Time:", res.exec_time)
            val = [e.opt.get("F")[0] for e in res.history]
            data = np.append(res.X, res.F)
            data1 = np.append(data, res.exec_time)
            data2 = np.append(data1, val)
            writer.writerow(data2)
            i += 1

#--------Speicherort der Simulink-Modelle-----------

eng = matlab.engine.start_matlab()
path = r"C:\Users\mnadmin\masterarbeitYR\testArea_Hauptmodul3"   # Pfad für xAchse_Sim_GR_GA_17V.slx
eng.addpath(path, nargout=0)

#-----Problem Variables-----

n_gen = 40      # Anzahl der Generationen
n_pop = 50      # Populationsgröße

#-------Untersuchten Algorithmus-----------

algorithm = PSO(pop_size=n_pop, adaptive=True)


#------Durchführe der Optimierung und Speichern in csv-Datei---------

eng.parpool()   # Starten paralleles Pool

# Durchführen Versuch mit Dimensionsreduktion
x_L= [100000*0, 1500000000*0, 1000*0, 100000*0, 100000000*0, 500*0, 250*0, 100000*0, 200000000*0, 0.00029*0, 0.075, 1*0, 200000*0, 0.97, 55/24*0.99, 0.019, 0.00451*0]    #-100% Abweichung nur W.Grad auf 0.9
x_U = [100000*2, 1500000000*2, 1000*2, 100000*2, 100000000*2, 500*2, 250*2, 100000*2, 200000000*2, 0.00029*2, 0.076, 1*2, 200000*2, 0.98, 55/24, 0.02, 0.00451*2]


new_referenceDrive(1, x_L, x_U)

df_apso_DimRed = pd.read_csv("apso_100proz_zweischicht_Seg3_SpezSeg3_Fall_1.csv")
df_apso_DimRed = df_apso_DimRed.drop(df_apso_DimRed.loc[:, 'beste Fitness':'Fitnessverlauf{}'.format(n_gen)].columns,
                                     axis=1)
df_apso_DimRed.loc['mean'] = df_apso_DimRed.mean()

# Berechnung der Massen
staender_Daempfung = (df_apso_DimRed['Variable1'].loc['mean'].copy())
staender_Steifigkeit = (df_apso_DimRed['Variable2'].loc['mean'].copy())
staender_Masse = (df_apso_DimRed['Variable3'].loc['mean'].copy())
spindel_Daempfung = (df_apso_DimRed['Variable4'].loc['mean'].copy())
spindel_steifigkeit = (df_apso_DimRed['Variable5'].loc['mean'].copy())
spindelgehaeuse_Masse = (df_apso_DimRed['Variable6'].loc['mean'].copy())
spindel_Masse =(df_apso_DimRed['Variable7'].loc['mean'].copy())
kgt_Daempfung =(df_apso_DimRed['Variable8'].loc['mean'].copy())
kgt_Steifigkeit =(df_apso_DimRed['Variable9'].loc['mean'].copy())
kgt_traegheitsmoment = df_apso_DimRed['Variable10'].loc['mean'].copy()
leitspindel_viskReib = df_apso_DimRed['Variable11'].loc['mean'].copy()
riemen_Daempfung =(df_apso_DimRed['Variable12'].loc['mean'].copy())
riemen_Steifigkeit =(df_apso_DimRed['Variable13'].loc['mean'].copy())
getriebe_wirkungsgrad = df_apso_DimRed['Variable14'].loc['mean'].copy()
getriebe_uebersetzung = df_apso_DimRed['Variable15'].loc['mean'].copy()
spindelsteigung = df_apso_DimRed['Variable16'].loc['mean'].copy()
motor_traegheitsmoment = df_apso_DimRed['Variable17'].loc['mean'].copy()

getriebe_wirkungsgrad_U = getriebe_wirkungsgrad+(getriebe_wirkungsgrad*0.01)

if getriebe_wirkungsgrad_U > 1:
    getriebe_wirkungsgrad_U = 1

# Neue Parametervektoren, besonders angenomenne gute Parameter aus erste Ref.Fahrt Seg3 mit 0.1% Abweichung, restliche Abweichung 100%
x_L = [(staender_Daempfung*0.9), 0, (staender_Masse*0.9), 0, 0,
       0, 0, 0, 0,
       0, 0.075, (riemen_Daempfung*0.9),
       0, 0.97,
       55/24*0.99, 0.019,  0]

x_U = [ (staender_Daempfung*1.1), 1500000000*2, (staender_Masse*1.1),100000*2, 100000000*2,
        500*2, 250*2, 100000*2, 200000000*2,
        0.00029*2, 0.076, (riemen_Daempfung*1.1),
        200000*2, 0.98,
        55/24, 0.02, 0.00451*2 ]


new_referenceDrive(2, x_L, x_U)

eng.quit()