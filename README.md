# Epistemic Logic Playground #

This README documents presentes the current state of our project and explains how to actually view the current state.

### Current State ###

#### Back End ####
Currently the back end can only handle formulas in K<sub>(m)</sub>. To extend the model checker to S5<sub>(m)</sub> we only need to be able to compute the reflexive-transitive closure of a set of states. To extend that to S5EC<sub>(m)</sub> we only need to add the truth definitions of the operators E and C. The server for the interaction with the frontend is fully set up. 

#### Front End ####


#### Report ####
The report is partly written, see `code/front/index.hmtl` anything we still want to add is shown with a todo

### How do I get set up? ###
Currently there is no interaction between the front and the back end. The most recent version of the necessary code can be downloaded from downloads.

#### Back End ####
Go to the folder `back` run the following command:

```
#!bash
pip install -r requirements
```

To start the server run the following command:

```
#!bash
gunicorn app
```
After running this command you get output that looks like this:

```
#!bash
2015-03-20 20:57:03 +0100] [63203] [INFO] Starting gunicorn 19.3.0
[2015-03-20 20:57:03 +0100] [63203] [INFO] Listening at: http://127.0.0.1:8000 (63203)
[2015-03-20 20:57:03 +0100] [63203] [INFO] Using worker: sync
[2015-03-20 20:57:03 +0100] [63206] [INFO] Booting worker with pid: 63206	
```


The adress that the server is listening at should be used to communicate with the server in this command:
   
```
#!bash    
http POST 127.0.0.1:8000/valuate < test_request.json 
```

The file `test_request.json` contains a json object representing an example request. One cane edit this file 

#### Front End ####
Go to the folder `front` and run the following command:

```
#!bash    
http-server .
```

Open the presented addres in a browser. Note that if the file `./front/index.html` is simply opened in a browser the LaTeX in the page will not be evaluated.