
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from keras.models import Model
from keras.utils import to_categorical
from tensorflow.keras.layers import LSTM, Dense, GRU, Dropout, Flatten, SimpleRNN, Bidirectional
from keras.optimizers import Adam
from sklearn.impute import SimpleImputer
from keras.regularizers import l2
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, multilabel_confusion_matrix, confusion_matrix
from keras.models import load_model

# loading data from csv

data = pd.read_csv("final_dataset.csv")
# data.head()


def prepare_sequences(d, time_steps):
    sequences = []
    labels = []

    for i in range(len(d) - time_steps):
        seq = data.iloc[i:i+time_steps][['score', 'completed',
                                         'max_correct_questions', 'questions_correct', 'topics']].values
        label = data.iloc[i+time_steps]['performance_category']
        sequences.append(seq)
        labels.append(label)

    return np.array(sequences), np.array(labels)


# preprocessing data
X, y = prepare_sequences(data, 7)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# one-hot encoding the labels
y_train = to_categorical(y_train, num_classes=5)
y_test = to_categorical(y_test, num_classes=5)


def test_model(model):

    y_pred = model.predict(X_test)
    print("Shape of y_pred:", y_pred.shape)

    return y_pred


def generate_minibatches(X, y, batch_size):
    total_samples = X.shape[0]
    while True:
        for i in range(0, total_samples, batch_size):
            X_batch = X[i:i + batch_size]
            y_batch = y[i:i + batch_size]
            yield X_batch, y_batch


def create_and_run_GRU(X_train, y_train, X_test, y_test, batch_size=32, epochs=20):
    # Define the GRU model
    model = Sequential()
    model.add(GRU(units=50, activation='relu', input_shape=(
        X_train.shape[1], X_train.shape[2]), return_sequences=True))
    model.add(GRU(units=50, activation='relu', return_sequences=True))
    model.add(GRU(units=50, activation='relu'))
    model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
    model.add(Dense(5, activation='softmax'))

    optimizer = Adam(clipvalue=0.5)
    model.compile(optimizer=optimizer,
                  loss='categorical_crossentropy', metrics=['accuracy'])

    # Generate minibatches for training data
    train_minibatch_generator = generate_minibatches(
        X_train, y_train, batch_size)

    # Calculate steps per epoch for training data
    train_steps_per_epoch = len(X_train) // batch_size

    # Train the model using fit_generator
    history = model.fit_generator(train_minibatch_generator, epochs=epochs,
                                  steps_per_epoch=train_steps_per_epoch, validation_data=(X_test, y_test))

    # Save the trained model
    model.save('trained_gru_model.h5')

    return history, model


def evaluate_model(y_pred, gru_hist):
    # evaluating the model

    y_pred_classes = np.argmax(y_pred, axis=1)
    y_pred_classes = to_categorical(y_pred_classes, num_classes=5)

    y_test_classes = y_test.astype(int)

    accuracy = accuracy_score(y_test_classes, y_pred_classes)
    print(f'Accuracy: {accuracy:.4f}')

    precision = precision_score(
        y_test_classes, y_pred_classes, average='weighted')
    print(f'Precision: {precision:.4f}')

    recall = recall_score(y_test_classes, y_pred_classes, average='weighted')
    print(f'Recall: {recall:.4f}')

    f1 = f1_score(y_test_classes, y_pred_classes, average='weighted')
    print(f'F1 Score: {f1:.4f}')

    y_test_indices = np.argmax(y_test_classes, axis=1)
    y_pred_indices = np.argmax(y_pred_classes, axis=1)

    conf_matrix = confusion_matrix(y_test_indices, y_pred_indices)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.title('Confusion Matrix')
    plt.show()

    plt.plot(gru_hist.history['accuracy'], label='Training Accuracy')
    plt.plot(gru_hist.history['val_accuracy'], label='Test Accuracy')
    plt.title('GRU Model Training and Test Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()


# gru_hist, GRU_model = create_and_run_GRU(X_train, y_train, X_test, y_test)

# gru_pred = test_model(GRU_model)
# evaluate_model(gru_pred, gru_hist)

# this creates a sequence for predicting the student's performance category


def prepare_input_sequences(input_data, time_steps):
    sequences = []

    # Iterate over each row in the input data
    for i in range(len(input_data) - time_steps + 1):
        seq = input_data.iloc[i:i+time_steps][['score', 'completed',
                                               'max_correct_questions', 'questions_correct', 'topics']].values
        sequences.append(seq)

    return np.array(sequences)


def classify_performance(input_dataframe):

    # Prepare input sequences
    input_sequences = prepare_input_sequences(input_dataframe, 7)

    # load trained model
    GRU_model = load_model('trained_gru_model.h5')

    # Make predictions using the trained GRU model
    predictions = GRU_model.predict(input_sequences)

    # Convert predictions to class labels
    predicted_labels = np.argmax(predictions, axis=1)

    # Display predicted labels
    print("Predicted labels:", predicted_labels)

    if predicted_labels == 0:
        return "poor"
    elif predicted_labels == 1:
        return "good"

# to run this code:
# classify_performance(input_data_frame)
