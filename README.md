# WolfOfWalmart
Large scale Walmart inventory analytics

## Installation

``` {.sourceCode .bash}
$ pip install -r requirements.txt
```

## How to use

-v Determines how verbose the output is

-o determines the destination of the csv file

-a determines if it should only find items in stock (Seting -a 1 for in stock only, leave default for everything)

-t determines how many threads to use

-i determines the skus to search (leave deafult for all, takes text files and strings as inputs)

-s determines which store to search (Leave default for all)


## Examples

### Search for every item that is in stock at Walmart store #2265

```bash

python searchByStore.py -s 2265 -o 2265.csv -a 1 -v 2

```

### Search for every chromecast in the united states

```bash

python searchByStore.py -i 435188866 -o chromecast.csv -v 2

```

### Pull the full inventory of every walmart store in the united states (in-stock and out of stock) (200,000,000+ items)

```bash

python searchByStore.py -o literallyEverything.csv -v 2

```
