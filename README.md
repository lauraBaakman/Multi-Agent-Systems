# Epistemic Logic Playground #

The README document gives the [defintion of the API](#api) and explains how to [run our project locally](#run).

<a name="api"></a>
## API ##
The API defines the following JSON endpoints:

* [valuate](#apiValuate)
* [logics](#apiLogics)

<a name="apiValuate"></a>
### /valuate ###
* POST
* Request
    {
        "state": "sc",
        "formula": "K_1 M_2 p <-> q",
        "model": {
            "states": [
                {
                    "id": "sa",
                    "vals": [true, true, false]
                }
            ],
            "propositions": ["p","q","r"],
            "relations": [
                ["sa","1","sa"]
            ],
            "logic": "T"
        }
    }
* Returns
    - 202: 
        {
            "truth_value": 
            "motivation":
            "model":
        }
        * truth_value is a boolean
        * motivation is the motivation as html.
        * model is the (updated) model in the same format as in the request.
    - 400: With a error title and message, if there is an error when evaluation or parsing.
    - 500: With a error title and message, if something else goes wrong.

<a name="apiLogics"></a>
### /logics ###
* GET
* Request
* Returns
    - 200:
        {
            "logics":
        }
        * logics is a list of strings with the names of logics that are accepted in POSTs to valuate.

<a name="run"></a>
### How to run the Epistemic Logic Playground ###
Since we use a REST API for the communcation between the [back-end](#back) [front-end](#front) one needs to set-up those two components seperately. The most recent version of the code can be downloaded from downloads.

<a name="back"></a>
#### Back End ####
The Python dependencies are installed using `pip`, [installation instructions for PIP are can be found here](https://pip.pypa.io/en/latest/installing.html). Once `pip` is intstalled go to the folder `back` and run the following command:

```
pip install -r requirements
```

To start the server run the following command in the folder `back`:

```
gunicorn app -b 127.0.0.1:8000
```

<a name="front"></a>
#### Front End ####
The easiest way to run the front end is with http-server, [installation instructions can be found here](https://www.npmjs.com/package/http-server). Once `http-server` is installed go to the folder `front` and run the following command:

```
http-server .
```

This should result in something like the following output:

```
Starting up http-server, serving . on: http://0.0.0.0:8080
Hit CTRL-C to stop the server
```

Open the presented addres, `http://0.0.0.0:8080` in the case above, in a browser. Note that if the file `./front/index.html` is simply opened in a browser the LaTeX in the page will not be evaluated, nor will the modelchecker work.