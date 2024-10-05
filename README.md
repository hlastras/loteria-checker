# Quiniela Results Checker

## Overview

This script checks the accuracy of user predictions for the Quiniela, a popular lottery in Spain, based on football match results. Given user bets (`input.txt`) and actual match outcomes (`result.txt`), it calculates how many predictions were correct or incorrect and displays the results in a simple table format. The script includes an option to count errors instead of hits.

## Features

- Compares user predictions against actual match outcomes.
- Calculates the number of correct predictions (hits) or incorrect predictions (errors) for each betting column.
- Outputs a summary of hits or errors and a formatted table of the matches and results.
- Marks unplayed matches with a dash (`-`).

## Usage

### Prerequisites

- Python 3.x

### Running the Script

To execute the script, use the following command in your terminal:

```sh
python quiniela.py input.txt result.txt [--error]
```

- `input.txt`: A file containing user bets.
- `result.txt`: A file containing actual match outcomes.
- `--error`: Optional flag to count and display prediction errors instead of hits.

### Example Input Files

#### `input.txt`

```
1.	2.	3.					
1.	Bayern Munich-Dinamo Zagreb	1	1	1						
2.	Milan-Liverpool	2	X	2						
3.	Sporting C. Portugal-Lille	1	X	1						
4.	Real Madrid-Stuttgart	1	1	1						
5.	Bolonia-Shakhtar Donetsk	X	2	1						
6.	Sparta Praga-Salzburgo	2	X	1						
7.	Celtic-Slovan Bratislava	1	1	1						
8.	Brujas-Borussia Dortmund	2	1	2						
9.	Manch City-Inter de Milán	1	1	1						
10.	PSG-Girona	1	1	1						
11.	Estrella Roja-Benfica	X	2	2						
12.	Feyenoord-B. Leverkusen	X	2	2						
13.	Atalanta-Arsenal	2	X	2						
14.	Mónaco-Barcelona	2	2	2						
15.	At. Madrid- Leipzig	2-0

18 SEP 2024
```

#### `result.txt`

```
1.	Bayern Munich - Dinamo Zagreb	9 - 2	
1
2.	Milan - Liverpool	1 - 3	
2
3.	Sporting C. Portugal - Lille	2 - 0	
1
4.	Real Madrid - Stuttgart	3 - 1	
1
5.	Bolonia - Shakhtar Donetsk	0 - 0	
X
6.	Sparta Praga - Salzburgo	3 - 0	
1
7.	Celtic - Slovan Bratislava	5 - 1	
1
8.	Brujas - Borussia Dortmund	0 - 3	
2
9.	Manch City - Inter De Milán	0 - 0	
X
10.	Psg - Girona	1 - 0	
1
11.	Estrella Roja - Benfica	1 - 2	
2
12.	Feyenoord - B. Leverkusen	0 - 4	
2
13.	Atalanta - Arsenal	0 - 0	
X
14.	Mónaco - Barcelona	2 - 1	
1
P-15	At. Madrid - Leipzig	2 - 1	
2-1
```

### Example Output

#### Hits Mode (Default)

```
Bet 1: 8 hits
Bet 2: 7 hits
Bet 3: 10 hits

No. Teams                         1   2   3
---------------------------------------------
1   Bayern Munich-Dinamo Zagreb   x   x   x
2   Milan-Liverpool               x       x
3   Sporting C. Portugal-Lille    x       x
4   Real Madrid-Stuttgart         x   x   x
5   Bolonia-Shakhtar Donetsk      x
6   Sparta Praga-Salzburgo                x
7   Celtic-Slovan Bratislava      x   x   x
8   Brujas-Borussia Dortmund      x       x
9   Manch City-Inter de Milán
10  PSG-Girona                    x   x   x
11  Estrella Roja-Benfica             x   x
12  Feyenoord-B. Leverkusen           x   x
13  Atalanta-Arsenal                  x
14  Mónaco-Barcelona               
15  At. Madrid- Leipzig           -   -   -
```

#### Errors Mode (`--error` Flag)

```
Bet 1: 4 fails
Bet 2: 4 fails
Bet 3: 1 fails

No. Teams                         1   2   3
---------------------------------------------
1   Bayern Munich-Dinamo Zagreb       
2   Milan-Liverpool                   x
3   Sporting C. Portugal-Lille        
4   Real Madrid-Stuttgart             
5   Bolonia-Shakhtar Donetsk          x   x
6   Sparta Praga-Salzburgo        x       
7   Celtic-Slovan Bratislava          
8   Brujas-Borussia Dortmund          x
9   Manch City-Inter de Milán     
10  PSG-Girona                        
11  Estrella Roja-Benfica         x       
12  Feyenoord-B. Leverkusen       x       
13  Atalanta-Arsenal              x   x   
14  Mónaco-Barcelona              -   -   -
15  At. Madrid- Leipzig           
```
