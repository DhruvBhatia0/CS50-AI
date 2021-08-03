import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        0 Administrative, an integer
        1 Administrative_Duration, a floating point number
        2 Informational, an integer
        3 Informational_Duration, a floating point number
        4 ProductRelated, an integer
        5 ProductRelated_Duration, a floating point number
        6 BounceRates, a floating point number
        7 ExitRates, a floating point number
        8 PageValues, a floating point number
        9 SpecialDay, a floating point number
        10 Month, an index from 0 (January) to 11 (December)
        11 OperatingSystems, an integer
        12 Browser, an integer
        13 Region, an integer
        14 TrafficType, an integer
        15 VisitorType, an integer 0 (not returning) or 1 (returning)
        16 Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    labels = []
    evidence = []
    months = ['Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sep','Oct','Nov','Dec']
    with open(filename) as file:
        content = list(csv.reader(file))
        content.pop(0)
        for row in content:
            temp = []
            temp.append(int(row[0]))
            temp.append(float(row[1]))
            temp.append(int(row[2]))
            temp.append(float(row[3]))
            temp.append(int(row[4]))
            temp.append(float(row[5]))
            temp.append(float(row[6]))
            temp.append(float(row[7]))
            temp.append(float(row[8]))
            temp.append(float(row[9]))
            temp.append(months.index(row[10]))
            temp.append(int(row[11]))
            temp.append(int(row[12]))
            temp.append(int(row[13]))
            temp.append(int(row[14]))
            if row[15] == 'Returning_Visitor':
                temp.append(1)
            else:
                temp.append(0)
            if row[16] == 'FALSE':
                temp.append(0)
            else:
                temp.append(1)
            if row[17] == 'FALSE':
                labels.append(0)
            else:
                labels.append(1)
            
            evidence.append(temp)
    return((evidence,labels))

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    return KNeighborsClassifier(n_neighbors=3).fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    count_true,count_false,predict_true,predict_false = 0,0,0,0
    for i in range(len(labels)):
        if labels[i] == 0:
            count_false+=1
            if predictions[i] == 0:
                predict_false += 1
        else:
            count_true += 1
            if predictions[i] == 1:
                predict_true += 1
    
    sensetivity = predict_true/count_true
    specificity = predict_false/count_false
    return (sensetivity, specificity)


if __name__ == "__main__":
    main()
