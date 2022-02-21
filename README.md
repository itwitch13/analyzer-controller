DevController is an application dedicated for remote instrument control and automation of microwave measurements.

The application provides a graphic user interface in a form of a configuration panel consisting of three main tabs. The user can remotely manipulate devices, i.e. spectrum analyzer and signal generator, among others changing parameters (frequency, IF filter bands, etc.), changing the operating mode of devices, generating large amounts of data analyzed by the system, presenting the result of activities in the form of an interactive graph, etc.

The application architecture relies on the MVC design pattern (model-view-controller), using the signal and slots mechanism. Actions performed by the user result in sending a signal, which is then handled by a controller appropriate for a given signal type.

DevController also provides analysis of user input in .csv and .png format, where after appropriate processing the data is presented on a chart. The graph can be manipulated by the user, which increases the convenience as well as the speed of the signal analysis. Additionally, thanks to the external PyQtGraph library, the application has been enriched with data export: a graph in the .png form and the current device configuration.
