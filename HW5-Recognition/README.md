train_1000_10.zip 10×10 obrazy, 20 tříd, 50 vzorů pro každou.
train_1000_28.zip 28×28 obrazy, 10 tříd, 100 vzorů pro každou
train_700_28.zip 28×28 obrazy, 10 tříd, různé počty vzorů pro třídy (počet kanálů obrázků v datasetu byl opraven)

```sh
>> python3.8 knn.py -h
usage: knn.py [-h] (-k K) [-o filepath] train_path test_path

Learn and classify image data with a k-NN classifier.

positional arguments:
train_path   path to the training data directory
test_path    path to the testing data directory

optional arguments:
-h, --help   show this help message and exit
-k K         number of neighbours (if k is 0 the code may decide about proper K by itself)
-o filepath  path (including the filename) of the output .dsv file with the results
```

