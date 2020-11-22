
# <center> Udacity Open Street Map Udacity Project </center>
<center>by Emma Chandler</center>

## <center>Table of Contents</center>

### 1. Overview and Summary of the Project
This project is a part of a Data Management and Data Analysis degree with Western Governors University as well as part of the Data Analysis Nanodegree. The purpose of this project is to use data munging techniques such as assessing the quality of the data for validity, accuracy, completeness, consistency and uniformity as applied to a portion of the OpenStreetMap data. Additionally, SQL will be used to store, query and aggregate the OpenStreetMap data. 

The map area that was chosen for this project is from Pittsburgh, Pennsylvaia. This map area has a variety of outdoor spaces, metropolitan regions and urban areas that provide a wealth of data and information. This project will aim to correct user-generated data and then resubmitting it to OpenStreetMap to improve their data. 

### 2. Overview of the Data

The size of the Pittsburgh data file is 52.7MB. 

The number of unique users, number of nodes, number of ways, and special types of nodes is programmatically discussed below. 

### 3.  Data Processing & Auditing
As the data was processed and audited a few issues surfaced that can be cleaned programatically. Below is a description of a few main issues that were discovered while exploring the data.  

Issue 1: Street Names

As with any region of the world, sometimes the street names are not uniform since there are many ways to write and abbreviate many common words used for streets. For example, North, N, and N. all have the same meaning but each one can be seen in the data set. In order to address this issue, we will map all possibilities to one uniform outcome. 

Issue 2: Zip Codes

In conducting research for this project, one of the issues that could arise is that of uniform zip codes. Most areas use the standard 5 digit zip code, however, some entries in the data can show a 9 digit zip code that includes 4 additional numbers added onto the end of original 5 with a hyphen. This data set contains multiple entries that utilize the 9 digit zip format while most are written in the 5 digit format. 

Issue 3: Phone Numbers

When exploring the data, a standard format for phone numbers was lacking. Some numbers included the country code of 1 at the beginning of the number while others didn't. Some phone numbers had parentheses around the area code but others just had the area code followed by a dash and then the rest of the phone number. This was programmatically cleaned and all phone numbers were given a standard format. 

Issue 4: State Codes

This data set was taken from a busy region of Pittsburgh and there was some lack of uniformity in how the state was represented. Entries in the data contained 5 different possibilities, one of which was a zip code. All entries were changed to be 'PA' instead other versions that were found in the data. 

### 4. Ideas For Additional Improvement

Idea for Improvement 1: Website Validation

In the OpenStreetMap XML file, there are websites listed for some businesses. An application that mines the data for those websites and then checks that those websites are still valid and applicable to that business would be helpful. This idea is discussed below. 


## Overview of the Data

The data used for this project is from Pittsburgh, Pennsylvania. In order to process the data, we needed to accomplish a few tasks first. Each task is outlined below. 

### Step 1: Iterative parsing

We first find the top level tags in the data set and creates a dictionary. Then the code counts the number of times that tag is seen in the code. This code comes from the Udacity Data Wrangling case study (mapparser.py). The output of that code is below:


```python
{'bounds': 1,
 'member': 71828,
 'meta': 1,
 'nd': 2805425,
 'node': 2335976,
 'note': 1,
 'osm': 1,
 'relation': 3350,
 'tag': 958712,
 'way': 388187}
```

### Step 2: Checking K Tags

Next, we ran some code to check the k tags in the XML to see if they have any characters we won't be able to process (tags.py). The output of that code is found below. 


```python
{'lower': 628479, 'lower_colon': 320183, 'other': 10049, 'problemchars': 1}
```

It looks like we have one character we are not able to process.

### Step 3: Additional Data Exploration

The size of the data file for Pittsburgh OpenStreetMap Data is 52.7MB. 

**Number of Nodes**

The following query was used to find the number of nodes in the data file:

SELECT COUNT(*) FROM nodes;

A total of 2,335,976 nodes were found in this data set. 

**Number of Ways**

The following query was used to find the number of ways in the data file:

SELECT COUNT(*) FROM ways;

A total of 388,187 ways were found in this data set. 

**Top 10 Amenities**

The following query was used to find the top 10 amenities in the data file:

SELECT value, count(*) AS counter FROM nodes_tags WHERE key = "amenity" GROUP BY value ORDER BY counter DESC LIMIT 10;


| Amenity          | Count |
|------------------|-------|
| restaurant       | 477   |
| place_of_worship | 429   |
| school           | 334   |
| waste_basket     | 216   |
| bench            | 216   |
| fast_food        | 158   |
| library          | 135   |
| post_box         | 127   |
| cafe             | 97    |
| parking          | 92    |

**Number of Users**

The following query was used to find the total number of unique users who submitted data to this data set. 
 
SELECT COUNT(DISTINCT uid) FROM
(SELECT DISTINCT uid FROM nodes UNION SELECT DISTINCT uid FROM ways);

This led to 2549 unique users who submitted data to this data set.

**Largest Religion**

Just for fun, let's find the top religion in the area using the following query. 

SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='place_of_worship') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC;

We find that the top religion in the region in Christian with 393 nodes.

**Most Popular Cuisine**

Finally, let's find the most popular cuisine in this region using this query:

SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='restaurant') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='cuisine'
GROUP BY nodes_tags.value
ORDER BY num DESC;

Here's the top 5:

| Cuisine Type     | Count |
|------------------|-------|
| pizza            | 59    |
| american         | 36    |
| italian          | 20    |
| chinese          | 18    |
| mexican          | 14    |


##  Data Processing & Auditing

Once we have assessed the situation with the OpenStreetMap data, we can now process and audit the data. 

### Issue 1: Audit and Processing Street Names

The following query was run to investigate street names:

SELECT value FROM nodes_tags WHERE key = "street" limit 20;

Many of the street names and were in formats that were acceptable but some uniformity could be had. Here are a few examples:

* The abbreviations 'Av.', 'Ave', and 'Ave.' can call be see in this data set. Each of these will be programmatically changed to the word 'Avenue'. 
* The abbreviation 'Bldg' was found but so was the abbreviation 'Brdg'. At first, I assumed these needed to be mapped to the same word but a quick google search found that there is a Swindell Bridge. So all 'Bldg' will get mapped to 'Building' and 'Brdg' will get mapped to 'Bridge'.
* Another interesting human data entry error was when the word 'DRive' was found in the dataset. This will be mapped to the word 'Drive'.

These issues and many more were programmatically fixed (auditstreetnames.py).

### Issue 2: Processing and Auditing State Name

The following query was run to investigate state names:

SELECT DISTINCT value FROM nodes_tags WHERE key = "state" LIMIT 20;

This query yields 5 possibilities for the state name: '15219', 'PA', 'Pa', 'Pennsylvania' and 'pa'. A quick google search revealed that 15219 is a zip code for Pittsburgh, PA. We will do a similar mapping to one uniform output by mapping every possibility to PA since this is the state abbreviation and because this is what shows up most often in the data. 

These issues and many more were programmatically fixed (auditstatenames.py).

### Issue 3: Processing and Auditing Zip Codes

The following query was run to investigate zip codes:

SELECT value FROM nodes_tags WHERE key = "postcode" LIMIT 20;

This query yeilds postal codes from Pittsburgh, PA in both the 5 digit format and the 9 digit format. We will clean all of these data points so that they each conform to the 5 digit zip code format. Additionally, there were some other anomalies in the zip code data. For example, the code 14233 shows up in the XML file and a quick google search shows that this code is from Buffalo, NY. I was unsure about how to handle this issue so it was left unchanged. Additionally, the postal code 151363 occurred once in the XML file. This code doesn't conform to the 5 digit or 9 digit format of traditional postal codes. In order to clean this data point, we truncated it to the first 5 digits as we did with all postal codes in the 9 digit format. 

These issues and many more were programmatically fixed (auditzip.py).

### Issue 4: Processing and Auditing Phone Numbers

The following query was run to investigate phone numbers:

SELECT value FROM nodes_tags WHERE key = "phone" LIMIT 20;

This query yeilds some interesting results such as phone numbers formatted as 412-328-2077 as well as phone numbers formats like +1 412 322 2424 with many other possibilities in between. Clearly this field in the data needs some work. My code will put all phone numbers into this format: +{country code} {area code} {7 digit number with a dash between the third and fourth digit}  

These issues and many more were programmatically fixed (auditphonenumbers.py).

##  Additional Ideas for Improvement

In the OpenStreetMap XML file, there are websites listed for some businesses. It would be convenient to have a program that mines the data for those websites and then checks that those websites are still valid and applicable to that business. 

We can query these websites with the following query in SQL:

SELECT value FROM nodes_tags WHERE key = "website"; 

Here are the first 5 results from this query:

* http://www.tazzadoro.net
* http://www.beverlyheights.org/
* bridgecitypgh.com
* https://www.pts.edu
* http://www.st-elizabeth.org/

The resulting websites look legitimate but more digging would be needed to tell if they are in fact legitimate websites.

Benefits: Applications that use OSM data can have up-to-date information for each business with a website. This information could benefit smaller businesses that don't have the time or resources to check that their business information is accurate on the internet. This could be one way to support small and local businesses. 

Issues: The main issues I can see when investigating websites for validity is the time it would take a computer to find the website in the XML, load the website, somehow check that the website works and is actually from that business (machine learning possibly), and then remove bad websites. This is a computationally expensive process. Additionally, there's the issue of what to do if you are directed to an invalid website. Do we remove that website? Do we look for the correct one and replace it? Do we contact business owners? All of these topics should be discussed if something like this is to be built.

##  Conclusion

We conducted a thorough investigation of OpenStreetMap data from Pittsburgh, Pennsylvania. We explored aspects of the data such as the number of ways and nodes that were found in the data, the number of users who contributed to the data, and some unique facts about the region related to amenities and religion. During our exploration, we found some inconsistencies with the data entry in multiple fields such as street names, zip codes, state abbreviation and phone numbers. These inconsistencies were cleaned and changed to a uniform entry in the data. We also explored possibilities to further clean and create value in the data. 

##  Resources

1. Udacity Data Wrangling Case Study
2. https://github.com/yudataguy/udacity-data-analyst-nanodegree/tree/master/data-wrangling - Used code examples to help load data from cvs files into database files
