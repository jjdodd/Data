# Normalized Data Design Ideas for the Following Dataset:

Source Data:
---
<img src="screenshots/source_data.png" alt="file:///Users/jakedodd/Data/school/csci260/A2-normalize/unnormalized_data.png">

> Immediately we can see that the 'First Name' column and 'Amount Donated' column betray the 1NF format.  

>Without succinct clarification from the original author of the given dataset, <br> there are a few pieces
>of data that, to be able to better format, may require <br>some potentially presumptuous solutions.
> >I am going to assume that Kim and Karl donated their 3500 total equally in separate $1750 donations each
> for now.
> > > This is purely an assumption, but would likely only effect the accountants who <br> want specific check
> values if found invalid, although without a payment-form-<br>atomic-value, or specific request for this feature its probably best not to scope <br>creep the parameters.

> Reformat any non-atomic cells (separate cells with multiple values) and define primary key {Donator ID}

# Normalized Data —> 1NF: "The Key..."

---
> Reformat any non-atomic cells (separate cells with multiple values) and define primary key {Donator ID}

## Table 1: <br> <span style="background-color: dodgerblue;"> DonatorID,</span> First Name, Last Name, Street Address, City, State Zip, Help Kids, Provide Book <br> <p style="color: dodgerblue;"> Primary Key:</p> <span style="background-color: dodgerblue;"> DonatorID
| <span style="background-color: dodgerblue;"> DonatorID | First Name | Last Name | Amount | Street Address | City           | State and Zip | Help Kids | Provide Books |
|:-----------:|:-----------|:----------|-------:|:--------------:|----------------|:-------------:|:---------:|:-------------:|
|      1      | Karl       | Castleton | $ 1750 | 1100 North Ave | Grand Junction |   CO 81501    |     ✅     |       ✅       |
|      2      | Kim        | Castleton | $ 1750 | 1100 North Ave | Grand Junction |   CO 81501    |     ✅     |       ✅       |
|      3      | Bob        | Doe       | $ 1000 | 1200 North Ave | Grand Junction |   CO 81502    |     ❌     |       ✅       |
|      4      | Karen      | Doe       | $ 2000 | 1200 North Ave | Grand Junction |   CO 81502    |     ✅     |       ✅       |
|      5      | Jane       | Doe       |  $ 500 | 1200 Texas Ave | Grand Junction |   CO 81502    |     ✅     |       ❌       |

# Normalized Data —> 2NF: "...The Whole Key...."

---
> From our current 1NF normalization, each person now has a unique ID, attributed <br> to their 
> atomic values removing  redundancies in last
> name but there are still multiples <br> for each street address, city, and state zip.

>To avoid confusing donation-sourcing, assign every donation by household its own <br> unique ID as well. 
 
>Finally add a bridge to connect Donations to Donators (Junction Table <br> composed 
> of two new Composite Keys.)

## Table 1: <br> <span style="background-color: dodgerblue;"> DonatorID,</span> First Name, Last Name, Street Address, City, State and Zip <br> <p style="color: dodgerblue;"> Primary Key:</p> <span style="background-color: dodgerblue;"> DonatorID

---
| <span style="background-color: dodgerblue;"> DonatorID  | First Name     | Last Name | Street Address |      City      | State and Zip |
|:------------:|:---------------|:----------|:--------------:|:--------------:|:-------------:|
|      1       | Karl           | Castleton | 1100 North Ave | Grand Junction |   CO 81501    |
|      2       | Kim            | Castleton | 1100 North Ave | Grand Junction |   CO 81501    |
|      3       | Bob            | Doe       | 1200 North Ave | Grand Junction |   CO 81502    |
|      4       | Karen          | Doe       | 1200 North Ave | Grand Junction |   CO 81502    |
|      5       | Jane           | Doe       | 1200 Texas Ave | Grand Junction |   CO 81502    |

---
## Table 2: <br><span style="background-color: dodgerblue;"> DonationID,</span> Donation Amount, Help for Kids, Book Provisions <br> <p style="color: dodgerblue;"> Primary Key: </p> <span style="background-color: dodgerblue;"> DonationID</span>

| <span style="background-color: dodgerblue"> Donator ID | Amount Donated | Help Kids | Provide Books |        
|:------------------------------------------------------:|:--------------:|:---------:|:-------------:|
|                           D1                           |     $3500      |     ✅     |       ✅       |
|                           D2                           |     $3000      |     ✅     |       ✅       |
|                           D3                           |      $500      |     ✅     |       ❌       |

>Donations are now dependant on donation ID.
---
## Table 3: <p style="color:yellow;"> Junction Table </p> <p style="color: dodgerblue;"> Composite Keys: </p> <span style="background-color: dodgerblue"> Donation ID, Donator ID </p>

| <span style="background-color: dodgerblue"> Donation ID | <span style="background-color: dodgerblue"> Donator ID |
|:-----------:|:------------------------------------------------------:|
|     D1      |                           1                            |
|     D1      |                           2                            |
|     D2      |                           3                            |
|     D2      |                           4                            |
|     D3      |                           5                            |
> Any donation ID now always references a specific person ID, even if multiple people <br>
> contributed from the same household.

# Normalized Data —> 3NF: "...And Nothing but the Key, So Help Me Codd"
> Remove Transitive Dependencies:
> > Transitive Dependencies occur when a change in the data might cascade into <br> changing multiple
> > data points for one or any number of different tables.

> City column, and State Zip column aren't being used currently to source any other the data points, <br> 
> from other tables, and City/State can all appear more than once on the table as a function of zipcode <br>
> so I converted them into their own table to reduce the amount of transitive dependencies on Zip in Table 1.


## Table 1: <br> <span style="background-color: dodgerblue;"> DonatorID,</span> First Name, Last Name, Street Address, and <span style="background-color: green;"> Zip <br> </span><p style="color: dodgerblue;"> Primary Key:</p> <span style="background-color: dodgerblue;"> DonatorID <br> </span> <p style="color: green;"> Foreign Key: <br> </p> <span style="background-color: green;"> Zip
| <span style="background-color: dodgerblue"> Donator ID | First Name | Last Name | Street Address |   <span style="background-color: green;"> Zip    |
|:------------------------------------------------------:|:-----------|:----------|:--------------:|:-----:|
|                           1                            | Karl       | Castleton | 1100 North Ave | 81501 |
|                           2                            | Kim        | Castleton | 1100 North Ave | 81501 |
|                           3                            | Bob        | Doe       | 1200 North Ave | 81502 |
|                           4                            | Karen      | Doe       | 1200 North Ave | 81502 |
|                           5                            | Jane       | Doe       | 1200 Texas Ave | 81502 |

## Table 2: <br><span style="background-color: dodgerblue;"> DonationID,</span> Donation Amount, Help for Kids, Book Provisions <br> <p style="color: dodgerblue;"> Primary Key: </p> <span style="background-color: dodgerblue;"> DonationID,</span> 
|  <span style="background-color: dodgerblue"> Donation ID  | Amount Donated | Help Kids | Provide Books |        
|:--:|:--------------:|:---------:|:-------------:|
| D1 |     $3500      |     ✅     |       ✅       |
| D2 |     $3000      |     ✅     |       ✅       |
| D3 |      $500      |     ✅     |       ❌       |

## Table 3: <br><p style="color:yellow;">Junction Table</p><p style="color: dodgerblue;"> Composite Keys: </p> <span style="background-color: dodgerblue"> Donation ID, Donator ID
| <span style="background-color: dodgerblue;"> Donation ID </span> | <span style="background-color: dodgerblue"> Donator ID |
|:----------------------------------------------------------------:|:------------------------------------------------------:|
|                                D1                                |                           1                            |
|                                D1                                |                           2                            |
|                                D2                                |                           3                            |
|                                D2                                |                           4                            |
|                                D3                                |                           5                            |

## Table 4:<br>City, State, <span style="background-color: dodgerblue;"> Zip </span><br> <p style="color: dodgerblue;"> Primary Key:</p> <span style="background-color: dodgerblue;"> Zip </span>  
| City           | State  | <span style="background-color: dodgerblue;"> Zip </span> |
|:---------------|:------:|---------------------------------------------------------:|
| Grand Junction |   CO   |                                                    81501 |
| Grand Junction |   CO   |                                                    81502 |

> Now, if a donator address changes, or a new doner from a different city is added to the database<br>
> their City and State are linked to Zip, which is now a foreign key for Table 1 in 3NF there is no need for multiple address changes, if a new or old donator address is appended to the data. 

> NOTE: I am beginning to see how this process could go on for a very long time, especially if a given database
> has tons of differing parameters.

