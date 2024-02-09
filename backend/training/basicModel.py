import keras
from keras import layers, callbacks, regularizers
import matplotlib.pyplot as plt
import numpy as np

MinDelta = 0.01
Epochs = 1000
Patience = 20
Batch_size = 1000
Test_batch = Batch_size
fileToStoreModel = "../FinalModel.keras"
fileToStorePlot = "loss_acc_graph.png"
# # For Testing
# Epochs = 20
# Patience = 5
# Batch_size = 1000
# Test_batch = Batch_size
# fileToStoreModel = "TestModelForPlotting.keras"
# fileToStorePlot = "loss_acc_graph_test.png"

def get_uncompiled_model():
    model = keras.models.Sequential()
    model.add(layers.Dense(64, input_shape = (784,)))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(64))
    model.add(layers.Activation('relu'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(10))
    model.add(layers.Activation('softmax'))
    return model


def get_compiled_model():
    model = get_uncompiled_model()
    model.compile(
        optimizer = keras.optimizers.Adam(learning_rate = 1e-3),
        loss = keras.losses.SparseCategoricalCrossentropy(),
        metrics = [keras.metrics.SparseCategoricalAccuracy()],
    )
    model.summary()
    return model

model = get_compiled_model();

(image_train, label_train), (image_test, label_test) = keras.datasets.mnist.load_data()

# Preprocess the data (these are NumPy arrays)
image_train = image_train.reshape(60000, 784).astype("float32") / 255
image_test = image_test.reshape(10000, 784).astype("float32") / 255

label_train = label_train.astype("float32")
label_test = label_test.astype("float32")


# First 10,000 samples for validation
x_val = image_train[:10000]
y_val = label_train[:10000]
image_train = image_train[10000:]
label_train = label_train[10000:]

# Early Stopping To prevent overfitting
earlystopping = callbacks.EarlyStopping(
    min_delta = MinDelta,
    monitor = "val_loss",
    mode = "min",
    patience = Patience,
    restore_best_weights = True,
)

print("Using fit model on training data")
history = model.fit(
    image_train,
    label_train,
    batch_size = Batch_size,
    epochs = Epochs,
    validation_data = (x_val, y_val),
    callbacks = [earlystopping]
)
print(history.history)

y = len(history.history['loss'])
t = np.linspace(1, y, y)


plt.figure ( figsize = ( 10, 10 ) )
plt.subplot ( 1, 1, 1 )
plt.plot (t, history.history['loss'], color = 'r', label = 'Loss', linewidth = 1 )
plt.scatter (t, history.history['val_loss'], c = 'b', label = 'Val Loss')
plt.plot (t, history.history['sparse_categorical_accuracy'], color = 'r', label = 'Sparse Accuracy', linewidth = 1 )
plt.scatter (t, history.history['val_sparse_categorical_accuracy'], c = 'b', label = 'Val Accuracy')
plt.xlabel ( 'Epoch' )
plt.ylabel ( 'Loss X Accuracy' )
plt.title ( 'Training Loss and Validation Loss Function' )
plt.grid ( True )
plt.legend ( loc = 'best' )
# plt.show()

plt.savefig(fileToStorePlot, dpi = 150)

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")
results = model.evaluate(image_test, label_test, batch_size = Test_batch)
print("test loss, test acc:", results)

model.save(fileToStoreModel)
del model