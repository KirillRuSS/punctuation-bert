from dataset import Dataset
from model import Model

data = Dataset()
model = Model()

seg_input = np.zeros((len(data.validation_outputs), 512))

model.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(
    [data.train_inputs, data.train_masks, seg_input],
    data.train_outputs,
    validation_data=([data.validation_inputs, data.validation_masks, seg_input], data.validation_outputs),
    epochs=1,
    batch_size=32
)