# /bin/bash

# Remove the existing data
hdfs dfs -rm -r /amazon_review
hdfs dfs -rm -r /amazon_review_wordcount
hdfs dfs -mkdir -p /amazon_review

# Download the data
review_categories=(
    All_Beauty Amazon_Fashion Appliances Arts_Crafts_and_Sewing Automotive Baby_Products Beauty_and_Personal_Care
    Books CDs_and_Vinyl Cell_Phones_and_Accessories Clothing_Shoes_and_Jewelry Digital_Music Electronics
    Grocery_and_Gourmet_Food Handmade_Products Health_and_Household Health_and_Personal_Care Home_and_Kitchen 
    Industrial_and_Scientific Kindle_Store Magazine_Subscriptions Movies_and_TV Musical_Instruments Office_Products
    Patio_Lawn_and_Garden Pet_Supplies Software Sports_and_Outdoors Subscription_Boxes Tools_and_Home_Improvement
    Toys_and_Games Video_Games Unknown
)

for category in ${review_categories[@]}; do
    echo "Downloading $category"
    wget https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_2023/benchmark/0core/rating_only/${category}.csv.gz
    gunzip ${category}.csv.gz
    hdfs dfs -put ${category}.csv /amazon_review
    rm ${category}.csv
done