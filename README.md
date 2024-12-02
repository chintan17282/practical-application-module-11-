# Prepration

It was noticed a waste majority of data was null, thus building a meaningful model may be challanging. 

```bash
manufacturer     4.133714
model            1.236179
condition       40.785232
cylinders       41.622470
fuel             0.705819
transmission     0.598763
drive           30.586347
size            71.767476
type            21.752717
```

Additionally it was noticed that VIN Number shared was actual VIN number and it roghtly mapped to Car's details when checked for random sample.  Reference `https://vpic.nhtsa.dot.gov`

Thus an ETL Job was written to fetch the details of all Cars whose VIN was provided to run on Google Cloud's Dataflow to fetch details of all VIN

**Script Reference**: `etl\enrich_vehicle.py`

**To Run the script** 

```bash	
python -m temp.py \
--input datavehicles.csv \
--output practical-application-module-11/practical_application_II_starter/data/vehicles_output \
--runner DirectRunner
```

#### - 01_enrich.ipynb 

This is the file used to enrich the vehicle already given data with enriched data. The output of which was persised in `data/vehicles_v2.csv`. Only static information of the Vehicle was pulled and <u>not</u> the variable features

Below is the stats after enrichment

```bash 
manufacturer     3.33
model            1.26
condition       38.11
cylinders       16.41
fuel             0.10
transmission     0.48
VIN             38.60
drive           26.46
size            71.46
type            15.90
```



# Approach

<img src="images/Flowchart.svg" style="zoom:100%;" />

### Cleaning

<img src="images/Cleaning.svg" style="zoom:80%;" />

- After dropping column `VIN` we had `29649` unique model. Feature, `model` is a free text with almost 30K unique values. This will not be contributing to modeling. Thus the column `model` was dropped too.
- `1171` duplicates were dropped
- There were `75` columns with missing `manufacturer`, `condition`, `cylinders`, `fuel` and `transmission`which were dropped
- There were `2425` columns with missing `manufacturer`, `condition`, `cylinders`, `drive` and `type` which were also dropped 
- Cosmetric Changes were done as follows
  - `state`, `region`and `manufacturer` were uniformly modified o have TitleCase

### EDA 

<img src="images/EDA.svg" style="zoom:75%;" />

- `25199` records which is `6.86%` of all data had `price` less then equal to 0. Similarly `1582`which is `0.43%` had `odometer` less then equal to 0. All these idenified records were dropped.
- Additionally there were `1901` records which had `price` and `odometer` less than 1000, we will not be considering those records.
- Outliers were removed by individually using `IQR` for `price` and `odometer` which removed approx `21644` (`~7%`)  records.
- Pattern of Price and Odometer were as follows 

<img src="images/price_count_kdeplot.png" style="zoom:75%;" />

<img src="images/odometer_count_kdeplot.png" style="zoom:75%;" />



- Each of the parameters were individually analyzed to see thr pattern and distribution

| Diagram                                                      |                                                         |
| ------------------------------------------------------------ | ------------------------------------------------------- |
| <img src="images/transmission_count.png" style="zoom:50%;" /> | <img src="images/transmission.png" style="zoom:50%;" /> |
| <img src="images/fuel_count.png" style="zoom:50%;" />        | <img src="images/fuel.png" style="zoom:50%;" />         |
| <img src="images/cylinders_count.png" style="zoom:75%;" />   | <img src="images/cylinder.png" style="zoom:75%;" />     |
| <img src="images/title_status_count.png" style="zoom:75%;" /> | <img src="images/title_status.png" style="zoom:75%;" /> |
| <img src="images/type_count.png" style="zoom:75%;" />        | <img src="images/type.png" style="zoom:75%;" />         |
| <img src="images/drive_count.png" style="zoom:75%;" />       | <img src="images/drive.png" style="zoom:75%;" />        |
| <img src="images/paint_color_count.png" style="zoom:75%;" /> | <img src="images/paint_color.png" style="zoom:75%;" />  |

- The Output of EDA is persisted in `vehicles_v3.csv`.



# Comparision of Models



| Model      | Description  | Training MSE | Test MSE|
| ----------- | ----------- |--|--|
| 1 | Transformation + Linear Regression                           | 38181229.52403128 | 38075772.29807217 |
| 2 | Transformation + <br>PolynomialFeature (all fields) + <br>Linear Regression | 23762515.4827903 | 24927248.450849023 |
| 3 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>Linear Regression | 35454226.46229427 | 35323206.23269257 |
| 4 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>SequentialFeatureSelector (15 features)<br>Linear Regression | 40621101.505078465 | 40581119.91222496 |
| 5 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>SequentialFeatureSelector (20 features)<br/>Linear Regression | 39202495.23184522 | 39090014.52399856 |
| 6 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>SequentialFeatureSelector (30 features)<br/>Linear Regression | 37303420.38294286 | 37126532.58778653 |
| 7 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>SelectFromModel(Lasso())<br/>Linear Regression | 35465551.2312093 | 35327202.025824144 |
| 8 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>Lasso (20 features) | 35481125.61269196 | 35351191.26094681 |
| 9 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>SelectFromModel(Lasso(), max_features=75)<br/>Linear Regression | 35864312.200730674 | 35748186.65240281 |
| 10 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>Ridge (default alpha) | 35454726.4658569 | 35324613.363171615 |
| 11 | Transformation + <br/>PolynomialFeature (4 fields) + <br/>Ridge (alpha=10) | 35462355.35987914 | 35329028.7862134 |



# Models

### Model 1

##### Transformation + Linear Regression

#### Steps

```mermaid
graph LR
A(Column Transform) -->B(Determine Polynomial Feature Degreee)
B --> C{Degree}
A(Column Transform) -->D(Polynomial Feature) 
D --> E(LinearRegression)

```

```bash
* SimpleImputer and then OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color'
* Plain OneHotEncoder on 'manufacturer','state'
* OrdinalEncoder on 'condition' and 'cylinders'
* StandardScaler and the PolynomialFeatures on 'year', 'odometer'
```

#### Line Plot of 200 Sample points

<img src="images/PolynomialFeatures_Degree_2_lineplot.png" style="zoom:100%;" />

---

### Model 2

##### Transformation + PolynomialFeature (all fields) + Linear Regression

```bash
1. Transformation    
* SimpleImputer -> OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color' 
* Plain OneHotEncoder on 'manufacturer','state'
* OrdinalEncoder on 'condition' and 'cylinders' 
* StandardScaler and the PolynomialFeatures on 'year', 'odometer'
2. Apply PolynomialFeatures(degree=2) on all the transformed fields    
3. LinearRegression
```





<img src="images/PolynomialFeatureson_All_Fields_lineplot.png" style="zoom:100%;" />

---

### Model 3

##### Transformation + PolynomialFeature (4 fields) + Linear Regression

```bash
1. Transformation    
* SimpleImputer -> OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color' 
* Plain OneHotEncoder on 'manufacturer','state'
* OrdinalEncoder -> PolynomialFeatures (degree=2) on 'condition' and 'cylinders' in respective parallel   
  pipeline
* StandardScaler and the PolynomialFeatures on 'year', 'odometer'
2. LinearRegression
```

<img src="images/PolynomialFeatureson_4_Fields_lineplot.png" style="zoom:100%;" />

---

### Model 4

##### Transformation + PolynomialFeature (4 fields) + SequentialFeatureSelector (15 features) + Linear Regression

```bash
1. ColumnTransformation<br>
- OrdinalEncoder > PolynomialFeature (degree=2) on 'cylinders' and 'condition' on separate pipelines 
- SimpleImputer > OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color' in a pipeline
- StandardScaler > PolynomialFeatures (degree=2) on ['year', 'odometer']           
2. SequentialFeatureSelector (n_features_to_select=15)
3. LinearRegression
```

<img src="images/SequentialFeatureSearch_15Fields_lineplot.png" style="zoom:100%;" />

---

### Model 5

##### Transformation + PolynomialFeature (4 fields) + SequentialFeatureSelector (20 features) + Linear Regression

```
1. ColumnTransformation<br>
- OrdinalEncoder > PolynomialFeature (degree=2) on 'cylinders' and 'condition' on separate pipelines 
- SimpleImputer > OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color' in a pipeline
- StandardScaler > PolynomialFeatures (degree=2) on ['year', 'odometer']           
2. SequentialFeatureSelector (n_features_to_select=20)
3. LinearRegression
```

<img src="images/SequentialFeatureSearch_20Fields_lineplot.png" style="zoom:100%;" />

---

###  Model 6 

#####  Transformation + PolynomialFeature (4 fields) + SequentialFeatureSelector (30 features) + Linear Regression

```bash
1. ColumnTransformation<br>
- OrdinalEncoder > PolynomialFeature (degree=2) on 'cylinders' and 'condition' on separate pipelines 
- SimpleImputer > OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color' in a pipeline
- StandardScaler > PolynomialFeatures (degree=2) on ['year', 'odometer']           
2. SequentialFeatureSelector (n_features_to_select=30)
3. LinearRegression
```

<img src="images/SequentialFeatureSearch_30Fields_lineplot.png" style="zoom:100%;" />

---

### Model 7

##### Transformation + PolynomialFeature (4 fields) + SelectFromModel(Lasso) + Linear Regression

```bash
1. ColumnTransformation<br>
- OrdinalEncoder > PolynomialFeature (degree=2) on 'cylinders' and 'condition' on separate pipelines 
- SimpleImputer > OneHotEncoder on 'transmission','fuel', 'type', 'drive', 'paint_color' in a pipeline
- StandardScaler > PolynomialFeatures (degree=2) on ['year', 'odometer']           
2. SelectFromModel(Lasso)
3. LinearRegression
```

<img src="images/SelectFromModel_Lasso_lineplot.png" style="zoom:100%;" />



---

### Model 8

##### Transformation + PolynomialFeature (4 fields) + Lasso

<img src="images/Lasso_lineplot.png" style="zoom:100%;" />

### Model 9

##### Transformation + PolynomialFeature (4 fields) + SelectFromModel(Lasso(), max_features=75) + Linear Regression

<img src="images/SelectFromModel_Lasso_75_lineplot.png" style="zoom:100%;" />

### Model 10

##### Transformation + PolynomialFeature (4 fields) + Ridge (default alpha)

<img src="images/Ridge_alpha_1_lineplot.png" style="zoom:100%;" />

### Model 11

##### Transformation + PolynomialFeature (4 fields) + Ridge (alpha=10)

<img src="images/Ridge_ap=lpha_10_lineplot.png" style="zoom:100%;" />