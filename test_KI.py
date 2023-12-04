# Import von allen Funktionen:
import functions_pandas
import pandas as pd
import datetime

from sklearn import svm
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score



# Einlesen der Daten
def getdataframe():

    # Servo Daten (Servo = 57)
    servo = functions_pandas.savetxtaspandas(ordner='test_data_KI/20231016__Laser_INA219_50Hz_Servo_ZR')

    servo_zsm = pd.concat(servo, ignore_index=True)

    servo_zsm['Klasse'] = 57

    # Schritt Daten (Schritt = 88)

    schritt = functions_pandas.savetxtaspandas(ordner='test_data_KI/20231016__Laser_INA219_50Hz_Schritt_ZR')

    schritt_zsm = pd.concat(schritt, ignore_index=True)

    schritt_zsm['Klasse'] = 88

    # beide dataframes zusammenführen
    data = pd.concat([servo_zsm, schritt_zsm], ignore_index=True)

    return data

data = getdataframe()

Merkmal_2 = 'Timestamp[ms]'
Merkmal_3 = 'Position[mm]'

# Hier beginnt der KI Alg.:
#Daten aufteilen:
X = data[['Strom[mA]', Merkmal_2, Merkmal_3]] #Features
y = data['Klasse'] #Labels

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Erstellen von SVM-Modellen mit verschiedenen Kernen
svm_linear = svm.SVC(kernel='linear')
svm_poly = svm.SVC(kernel='poly', degree=3)  # Polynom-Kern dritten Grades
svm_rbf = svm.SVC(kernel='rbf')  # RBF-Kern
svm_sigmoid = svm.SVC(kernel='sigmoid')


current_time = datetime.datetime.now().time()

print('--- Start Modelle an Trainingsdaten anpassen: - ' + str(current_time) + ' ---')

# Modelle an die Trainingsdaten anpassen
svm_linear.fit(X_train, y_train)
svm_poly.fit(X_train, y_train)
svm_rbf.fit(X_train, y_train)
svm_sigmoid.fit(X_train, y_train)
# k-NN
k = 3  # Anzahl der Nachbarn
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(X_train, y_train)
# Decision tree
dt_classifier = DecisionTreeClassifier()
dt_classifier.fit(X_train, y_train)


# Vorhersagen treffen
y_pred_linear = svm_linear.predict(X_test)
y_pred_poly = svm_poly.predict(X_test)
y_pred_rbf = svm_rbf.predict(X_test)
y_pred_sigmoid = svm_sigmoid.predict(X_test)
y_pred_knn = knn.predict(X_test)
y_pred_decisiontree = dt_classifier.predict(X_test)

# Genauigkeiten bewerten
accuracy_linear = accuracy_score(y_test, y_pred_linear)
accuracy_poly = accuracy_score(y_test, y_pred_poly)
accuracy_rbf = accuracy_score(y_test, y_pred_rbf)
accuracy_sigmoid = accuracy_score(y_test, y_pred_sigmoid)
accuracy_knn = accuracy_score(y_test, y_pred_knn)
accuracy_decisiontree = accuracy_score(y_test, y_pred_decisiontree)

# Ausgabe der Genauigkeiten
print(f"Genauigkeit (Linearer Kern): {accuracy_linear}")
print(f"Genauigkeit (Polynom-Kern): {accuracy_poly}")
print(f"Genauigkeit (RBF-Kern): {accuracy_rbf}")
print(f"Genauigkeit (Sigmoid-Kern): {accuracy_sigmoid}")
print(f"Genauigkeit (k-NN): {accuracy_knn}")
print(f"Genauigkeit (decision tree): {accuracy_decisiontree}")


current_time = datetime.datetime.now().time()
print('Ende: - ' + str(current_time) + ' ---')
