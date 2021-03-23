
[![Welltok Campaign Cost Calculator](https://images.unsplash.com/photo-1594980596870-8aa52a78d8cd?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=925&q=80)](https://user-images.githubusercontent.com/8799954/112210638-51c24f00-8bf1-11eb-84a8-7b88650dbea8.mp4)


# Welltok Campaign Cost Calculator

---

### Basic usage

- The main command is called **campaign_cost.py**

```
./python campaign_cost.py --size AUDIENCE_SIZE --channels "SMS|EM" [--showbreakup]
```

- size helps specify the number of users we want to calculate for
- channels help specify the channels we want to include in the calculation. They should be pipe separated and enclosed in double quotes.
- showbreakup breaks the calculation and shows how the total was calculated

### Utility Command

- Another command called **reload.py** was implemented to show how the design made this tool extensible to changes

```
./python reload.py [--file]
```

- reload command reloads the configuration/cost data into database using config.json by default
- if you want to specify any other configuration file, you can --file option to specify the same

---

### Database Design

- The database consists of four tables :
  - **channels** - we specify channel names and their codes
  - **range** - we 'from' and 'to' to specify closed range interval [from,to]
  - **base_fee** - stores base_fee for a given channel.
  - **trans_fee** - stores the price against the mapping of range and channel.

---

### Other Considerations

- Due to lack of time other unique and foreign key validations are not done on config.json data and I'm leveraging the database error handling for it.
- I've considered the range of user count from `[0, 1 Billion]` which can be easily tweaked

---

#### Demo Videos

- I've included 2 videos namely `Demo.mp4` and `Design.mp4`. The first one shows the utility works and the second one briefly explains the design of code and other considerations. Given more time, it'd have been interesting to draw the UML and ER diagram.
- Design Considerations - https://user-images.githubusercontent.com/8799954/112210736-6ef71d80-8bf1-11eb-8857-7afe92755e95.mp4
---

Email ID : `mohit.kalra@ufl.edu`
Phone : `3523271608`
